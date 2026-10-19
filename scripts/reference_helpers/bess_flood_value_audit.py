#!/usr/bin/env python3
"""Audit source-derived BESS value allocations and explicit repair-policy examples.

Research only: no runtime curve, automatic ingress inference, or annual metrics.
Read the original PVSCM text inputs; never execute the accompanying Excel macros.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs/extra/discussion/bess_damage/evidence"
RAW = ROOT / "data/bess/raw_flood_review_r3"
PINS = {
    "pvscm_2024.zip": "96247a16611b5548c96b1a431bcd51d9d5e113f8f4ef54fb2ffdbcec0cbf315e",
    "pvscm_2024/UPV 2024Q1.txt": "fd65a854a2e6bee8384081ebaa40abf2f56e160fff624092d9a9e1608ea9d496",
    "pvscm_2024/PVSCM 2024.xlsm": "58c59866e8b00acb938333dd818ff20aba1815ab9e6f166e6422654fc20e41a9",
    "sungrow_sbs050.pdf": "51d18a00286753b6e71d8d38fac8fe9daef6112bc6eb9c0677edf90e5103a2d0",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def conditional_replacement(value: float, *, affected_fraction: object) -> float | None:
    """Explicit policy arithmetic; unknown affected share never defaults to one."""
    if not isinstance(affected_fraction, (float, int)) or isinstance(affected_fraction, bool):
        return None
    if not math.isfinite(affected_fraction) or not 0 <= affected_fraction <= 1:
        return None
    return value * affected_fraction


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hazard-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    for name, digest in PINS.items():
        assert sha(RAW / name) == digest, f"Research source changed: {name}"
    reference = args.hazard_repo.resolve() / "docs/plans/_cross_cutting/bess_conus"
    reference_pins = json.loads((reference / "verification/reference_checks.json").read_text())["sha256"]
    for name, digest in reference_pins.items():
        assert sha(reference / name) == digest, f"Reference changed: {name}"
    inputs = {}
    for line_no, line in enumerate((RAW / "pvscm_2024/UPV 2024Q1.txt").read_text().splitlines(), 1):
        if "=" in line and not line.startswith("="):
            key, value = line.split("=", 1)
            if key.startswith(("ESS.", "Factors.")):
                inputs[key] = (line_no, value.split("\\"))
    cell = float(inputs["ESS.Li-Ion Cells"][1][2])
    packs = float(inputs["ESS.Battery Packs"][1][2])
    shell = float(inputs["ESS.Enclosure"][1][2])
    tariff = float(inputs["Factors.Tariff301"][1][3])
    # These two values are explicitly printed in the pinned source comments/formula.
    assert inputs["ESS.Li-Ion Cells"][1][4] == "=D10*(1+0.034+Tariff301)"
    assert "70% battery management, 30% thermal management" in inputs["ESS.Battery Packs"][1][5]
    general_duty, management_fraction = .034, .70
    with (reference / "reference_budget.csv").open() as stream:
        budget = {r["row_id"]: float(r["included_usd"]) for r in csv.DictReader(stream)}
    with (reference / "layout.csv").open() as stream:
        layout = list(csv.DictReader(stream))
    count = sum(r["group_id"] == "battery_enclosures" for r in layout)
    enclosure = budget["battery_cabinets"] / count
    total = sum(budget.values())
    allocations, tests = [], []

    def check(name: str, actual: object, expected: object) -> None:
        ok = math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-8) if isinstance(expected, float) else actual == expected
        assert ok, (name, actual, expected)
        tests.append({"check_id": name, "actual": actual, "expected": expected, "result": "PASS"})

    check("source_cell_base", cell, 75.)
    check("source_management_thermal_base", packs, 25.)
    check("source_composite_base", shell, 20.)
    check("source_tariff", tariff, .25)
    check("reference_enclosure_count", count, 80)
    check("reference_enclosure_value", enclosure, 1050000.)
    check("reference_whole_plant_value", total, 109800000.)
    cases = {}
    for basis, cell_input in [("MMP_related_allocation", cell * (1 + general_duty + tariff)),
                              ("MSP_allocation_sensitivity", cell)]:
        amounts = {"cells": cell_input, "battery_management": packs * management_fraction,
                   "thermal_management": packs * (1 - management_fraction),
                   "enclosure_racks_fire_suppression": shell}
        denominator = sum(amounts.values())
        values = {group: enclosure * amount / denominator for group, amount in amounts.items()}
        cases[basis] = values
        check(basis + "_reference_preserved", sum(values.values()), enclosure)
        check(basis + "_fleet_preserved", sum(values.values()) * count, budget["battery_cabinets"])
        check(basis + "_shares_sum", sum(amount / denominator for amount in amounts.values()), 1.)
        for group, amount in amounts.items():
            allocations.append({"allocation_case": basis, "cost_group": group,
                                "source_direct_input_usd_per_kwh_cap": amount,
                                "direct_input_denominator_usd_per_kwh_cap": denominator,
                                "dimensionless_share": amount / denominator,
                                "projected_usd_per_enclosure": values[group],
                                "projected_fleet_usd": values[group] * count,
                                "status": "RELATED_BENCHMARK_ALLOCATION_NOT_REPAIR_QUOTE"})
    preferred = cases["MMP_related_allocation"]
    active = sum(preferred[g] for g in ("cells", "battery_management", "thermal_management"))
    battery_control = preferred["cells"] + preferred["battery_management"]
    check("market_direct_inputs", 96.3 + 25 + 20, 141.3)
    check("active_known_answer", active / enclosure, 1213 / 1413)
    check("battery_control_known_answer", battery_control / enclosure, 1138 / 1413)
    for name, q in [("missing", None), ("nan", float("nan")), ("infinite", float("inf")),
                    ("negative", -.1), ("above_one", 1.1), ("boolean", True), ("string", "1")]:
        check("affected_fraction_" + name, conditional_replacement(active, affected_fraction=q), None)
    check("no_affected_hardware", conditional_replacement(active, affected_fraction=0), 0.)
    check("quarter_affected", conditional_replacement(active, affected_fraction=.25), active / 4)
    check("one_affected_enclosure", conditional_replacement(active, affected_fraction=1), active)
    check("two_enclosures_different_states", sum(conditional_replacement(active, affected_fraction=q) for q in (0, 1)), active)
    check("eighty_enclosures_uniform_state", sum(conditional_replacement(active, affected_fraction=1) for _ in range(count)), active * count)
    policies = []
    for label, value in [("battery_and_management_only", battery_control),
                         ("all_active_hardware_proposed_policy", active),
                         ("entire_enclosure_stress_policy", enclosure)]:
        policies.append({"repair_policy": label, "explicit_affected_fraction": 1,
                         "conditional_usd_one_enclosure": value,
                         "conditional_usd_80_identically_affected_enclosures": value * count,
                         "remaining_enclosure_value_not_evaluated_usd": enclosure - value,
                         "complete_enclosure_loss_usd": None,
                         "status": "POLICY_COMPARISON_NOT_PROBABILITY_OR_LOSS_BOUND"})
    probes = []
    # Owner-review scenarios only: neither entry nor whole-group impact is defaulted.
    for entry in [.30, .60]:
        for depth in [0., .15, .29, .30, .32, .45, .60, .61, .90]:
            q = float(depth > entry)
            probes.append({"hypothetical_entry_m": entry, "external_depth_m": depth,
                           "policy_affected_fraction": q,
                           "conditional_active_hardware_usd_one_enclosure": conditional_replacement(active, affected_fraction=q),
                           "complete_enclosure_loss_usd": None,
                           "status": "COMMON_ENTRY_POLICY_HYPOTHESIS_NOT_ADMITTED"})
    check("at_entry_policy_zero", next(r["policy_affected_fraction"] for r in probes if r["hypothetical_entry_m"] == .3 and r["external_depth_m"] == .3), 0.)
    check("above_entry_policy_one", next(r["policy_affected_fraction"] for r in probes if r["hypothetical_entry_m"] == .3 and r["external_depth_m"] == .32), 1.)
    check("complete_losses_withheld", all(r["complete_enclosure_loss_usd"] is None for r in probes), True)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "value_allocations.csv", allocations)
    write_csv(output / "repair_policy_examples.csv", policies)
    write_csv(output / "entry_policy_examples.csv", probes)
    write_csv(output / "known_answer_checks.csv", tests)
    summary = {"classification": "EVIDENCE_ONLY_NO_OUTPUT_CHANGE", "runtime_admitted": False,
               "research_policy_ruling": "OPEN_BF_Q01", "checks_passed": len(tests),
               "reference_tiv_usd": total, "reference_enclosure_usd": enclosure,
               "active_hardware_candidate_usd_per_enclosure": active,
               "active_hardware_candidate_fleet_usd": active * count,
               "enclosure_composite_not_evaluated_usd": (enclosure - active) * count,
               "active_plus_pcs_candidate_value_fraction": (active * count + budget["pcs"]) / total,
               "other_plant_value_not_evaluated_usd": total - active * count - budget["pcs"],
               "market_allocation_active_share": active / enclosure,
               "msp_sensitivity_active_share": 100 / 120,
               "review_warning": "Value shares are not DRs. Policy scenarios are not measured average damage or upper/lower bounds.",
               "raw_source_sha256": PINS, "reference_sha256": reference_pins,
               "script_sha256": sha(Path(__file__)),
               "output_sha256": {name: sha(output / name) for name in (
                   "value_allocations.csv", "repair_policy_examples.csv",
                   "entry_policy_examples.csv", "known_answer_checks.csv")}}
    (output / "audit_receipt.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("checks_passed", "runtime_admitted", "active_hardware_candidate_usd_per_enclosure", "active_plus_pcs_candidate_value_fraction")}, indent=2))


if __name__ == "__main__":
    main()
