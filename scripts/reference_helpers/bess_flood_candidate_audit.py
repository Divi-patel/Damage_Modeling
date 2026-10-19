#!/usr/bin/env python3
"""Test BESS Flood hypotheses; never produce a runtime curve or risk result.

The battery formulas deliberately expose two unqualified interpretations. Their
span is not a confidence interval or a bound on real loss. PCS values reproduce
the existing FS_INV response under explicit hypothetical target inputs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from damage_curve_eval import evaluate_curve_record

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs/extra/discussion/bess_damage/evidence"
SOURCE = ROOT / "docs/cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json"
SOURCE_SHA = "a08e77ef034e1ecea3e7cd05d13c825921b54d610fca9de8651ebda8e857082d"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def pcs_probe(record: dict, *, depth: object, entry: object, unit: str = "m",
              water: str = "freshwater", target: str = "separate_pcs_hardware",
              ip_credit: bool = False) -> dict:
    """Audit-only adapter. Entry is supplied, never defaulted from a mounting base."""
    reason = None
    if unit != "m":
        reason = "UNSUPPORTED_UNITS"
    elif not finite_number(depth) or not finite_number(entry):
        reason = "MISSING_OR_INVALID_EXPOSURE"
    elif depth < 0 or entry < 0:
        reason = "NEGATIVE_DEPTH_OR_ENTRY"
    elif water != "freshwater":
        reason = "WATER_CONDITION_NOT_QUALIFIED"
    elif target != "separate_pcs_hardware":
        reason = "INCOMPATIBLE_VALUE_UNIT"
    elif ip_credit:
        reason = "UNQUALIFIED_PROTECTION_CREDIT"
    if reason:
        return {"audit_status": reason, "audit_dr": None, "native_depth_m": None}
    # Round away subtraction noise only; do not extend the source domain.
    native = max(0.0, round(depth - entry, 12))
    if native > record["parameters"]["points"][-1][0]:
        return {"audit_status": "OUTSIDE_SOURCE_DOMAIN", "audit_dr": None, "native_depth_m": native}
    return {"audit_status": "HYPOTHETICAL_TRANSFER_ONLY",
            "audit_dr": evaluate_curve_record(record, x=native), "native_depth_m": native}


def battery_hypotheses(depth: float, base: float, height: float) -> tuple[float, float]:
    """Rejected-as-mean illustrations, not a BESS vulnerability implementation."""
    above = max(0.0, round(depth - base, 12))
    immediate_bundle = float(above > 0)
    uniform_height = min(1.0, above / height)
    return immediate_bundle, uniform_height


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def plot_comparison(output: Path, base: float, height: float, record: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), layout="constrained")
    fig.suptitle("BESS Flood — assumption test, not an admitted damage curve", fontsize=15)
    ax = axes[0]
    ax.plot([0, base, base, base + height], [0, 0, 100, 100], "--",
            color="#ad4c27", label="Immediate full enclosure replacement")
    ax.plot([0, base, base + height], [0, 0, 100], color="#276b89",
            label="Uniform replacement value with height")
    ax.set_title("Battery enclosure: two unqualified interpretations", fontsize=11)
    ax.legend(loc="center right", fontsize=8)
    ax.text(.04, .88, "Neither selected; do not average", transform=ax.transAxes, fontsize=10,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": .85})
    ax = axes[1]
    points = record["parameters"]["points"]
    ax.plot([0] + [base+x for x, _ in points], [0] + [100*y for _, y in points],
            "o-", color="#527746", markersize=4)
    ax.set_title("PCS: exact existing FS_INV response, hypothetical entry", fontsize=11)
    ax.text(.04, .08, "T3 proxy candidate\nTarget entry and repair scope remain open",
            transform=ax.transAxes, fontsize=10)
    for ax in axes:
        ax.axvline(base, color="#737373", linewidth=.8, alpha=.7)
        ax.set(xlim=(0, 1.3), ylim=(-3, 105), xlabel="External water depth above local grade (m)",
               ylabel="Same-unit hardware damage ratio (%)")
        ax.grid(alpha=.2)
        ax.spines[["top", "right"]].set_visible(False)
    fig.supxlabel("Both panels assume entry at the 0.30 m mounting base for this experiment only.\n"
                  "Geometry is known for the selected reference; water-entry performance is not.", fontsize=10)
    fig.savefig(output, dpi=160, metadata={"Software": "bess_flood_candidate_audit.py"})
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hazard-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    hazard = args.hazard_repo.resolve()
    reference = hazard / "docs/plans/_cross_cutting/bess_conus"
    spec_path = EVIDENCE / "r2/experiment_spec.json"
    spec = json.loads(spec_path.read_text())
    assert spec["runtime_admitted"] is False and spec["selected_battery_curve"] is None
    assert sha(SOURCE) == SOURCE_SHA, "Source changed; requalify the audit"
    checks = json.loads((reference / "verification/reference_checks.json").read_text())
    for name, digest in checks["sha256"].items():
        assert sha(reference / name) == digest, f"Reference changed: {name}"
    record = next(r for r in json.loads(SOURCE.read_text())["curve_records"] if r["curve_id"] == "FS_INV")
    with (reference / "reference_budget.csv").open() as stream:
        budget = {r["row_id"]: float(r["included_usd"]) for r in csv.DictReader(stream)}
    with (reference / "layout.csv").open() as stream:
        layout = list(csv.DictReader(stream))
    enclosures = [r for r in layout if r["group_id"] == "battery_enclosures"]
    pcs = [r for r in layout if r["group_id"] == "pcs"]
    assert len(enclosures) == 80 and len(pcs) == 20
    assert {r["base_z_m"] for r in enclosures + pcs} == {"0.3"}
    assert {r["height_m"] for r in enclosures} == {"2.9"}
    base, height = float(enclosures[0]["base_z_m"]), float(enclosures[0]["height_m"])
    enclosure_value, pcs_value = budget["battery_cabinets"] / len(enclosures), budget["pcs"] / len(pcs)
    assert enclosure_value == 1050000 and pcs_value == 520000
    test_rows = []

    def check(name: str, actual: object, expected: object) -> None:
        ok = math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12) if isinstance(expected, float) else actual == expected
        assert ok, (name, actual, expected)
        test_rows.append({"check_id": name, "result": "PASS", "actual": actual, "expected": expected})

    # Independent known answers cover the transfer seam, not just source parity.
    for name, depth, entry, expected in [
        ("dry", 0., .3, 0.), ("below_entry", .29, .3, 0.),
        ("at_entry", .3, .3, 0.), ("first_knot", .32, .3, .05),
        ("intermediate", .40, .3, .5), ("single_height_subtraction", .45, .3, .75),
        ("same_relative_depth_raised_entry", .75, .6, .75),
        ("upper_endpoint", 2.3, .3, 1.),
    ]:
        check(name, pcs_probe(record, depth=depth, entry=entry)["audit_dr"], expected)
    invalid = [
        ("no_depth", {"depth": None}, "MISSING_OR_INVALID_EXPOSURE"),
        ("no_entry", {"entry": None}, "MISSING_OR_INVALID_EXPOSURE"),
        ("nan_depth", {"depth": float("nan")}, "MISSING_OR_INVALID_EXPOSURE"),
        ("infinite_depth", {"depth": float("inf")}, "MISSING_OR_INVALID_EXPOSURE"),
        ("bool_depth", {"depth": True}, "MISSING_OR_INVALID_EXPOSURE"),
        ("negative_depth", {"depth": -.1}, "NEGATIVE_DEPTH_OR_ENTRY"),
        ("negative_entry", {"entry": -.1}, "NEGATIVE_DEPTH_OR_ENTRY"),
        ("feet_are_not_metres", {"unit": "ft"}, "UNSUPPORTED_UNITS"),
        ("saline", {"water": "saline"}, "WATER_CONDITION_NOT_QUALIFIED"),
        ("unknown_water", {"water": "unknown"}, "WATER_CONDITION_NOT_QUALIFIED"),
        ("whole_plant", {"target": "whole_plant"}, "INCOMPATIBLE_VALUE_UNIT"),
        ("integrated_pcs_and_mv", {"target": "pcs_and_mv"}, "INCOMPATIBLE_VALUE_UNIT"),
        ("rating_credit", {"ip_credit": True}, "UNQUALIFIED_PROTECTION_CREDIT"),
        ("above_domain", {"depth": 2.3001}, "OUTSIDE_SOURCE_DOMAIN"),
    ]
    for name, overrides, expected in invalid:
        result = pcs_probe(record, **({"depth": .45, "entry": .3} | overrides))
        check(name, result["audit_status"], expected)
        check(name + "_no_numeric_output", result["audit_dr"], None)
    for x, expected in record["parameters"]["points"]:
        check(f"source_parity_{x}", pcs_probe(record, depth=base+x, entry=base)["audit_dr"], float(expected))
    check("battery_both_zero_at_base", battery_hypotheses(base, base, height), (0., 0.))
    check("battery_both_one_at_roof", battery_hypotheses(base+height, base, height), (1., 1.))
    check("battery_uniform_015_m", battery_hypotheses(.45, base, height)[1], .15/2.9)
    check("one_pcs_015_m_usd", pcs_probe(record, depth=.45, entry=base)["audit_dr"] * pcs_value, 390000.)
    check("two_pcs_distinct_exposures_usd", sum(pcs_probe(record, depth=d, entry=base)["audit_dr"] * pcs_value for d in [.25, .45]), 390000.)
    check("two_enclosures_distinct_exposures_step_usd", sum(battery_hypotheses(d, base, height)[0] * enclosure_value for d in [.25, .45]), 1050000.)
    check("remaining_budget_not_dropped_usd", sum(budget.values()) - budget["pcs"] - budget["battery_cabinets"], 15400000.)

    pcs_rows, battery_rows = [], []
    for depth in spec["external_depth_probes_m"]:
        result = pcs_probe(record, depth=depth, entry=base)
        dr = result["audit_dr"]
        pcs_rows.append({"external_depth_m": depth, "assumed_entry_m": base, **result,
                         "one_pcs_hardware_arithmetic_usd": None if dr is None else dr * pcs_value,
                         "runtime_admitted": False})
        immediate, uniform = battery_hypotheses(depth, base, height)
        battery_rows.append({"external_depth_m": depth, "assumed_entry_m": base,
                             "hypothesis_immediate_bundle_dr": immediate,
                             "hypothesis_uniform_height_dr": uniform,
                             "immediate_one_enclosure_arithmetic_usd": immediate * enclosure_value,
                             "uniform_one_enclosure_arithmetic_usd": uniform * enclosure_value,
                             "selected_curve": "NONE", "runtime_admitted": False})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "pcs_probes.csv", pcs_rows)
    write_csv(args.output_dir / "battery_hypothesis_probes.csv", battery_rows)
    write_csv(args.output_dir / "known_answer_checks.csv", test_rows)
    plot_comparison(args.output_dir / "candidate_comparison.png", base, height, record)
    paths = {"helper": Path(__file__), "experiment_spec": spec_path, "source_curve": SOURCE,
             "source_evaluator": ROOT / "scripts/reference_helpers/damage_curve_eval.py",
             "reference_checks": reference / "verification/reference_checks.json",
             "budget": reference / "reference_budget.csv", "layout": reference / "layout.csv",
             "runtime_index": ROOT / "docs/contracts/machine_readable_artifact_index.json"}
    receipt = {"schema": "bess_flood_hypothesis_audit.v1", "change_class": "EVIDENCE_ONLY_NO_OUTPUT_CHANGE",
               "checks_passed": len(test_rows), "all_checks_passed": True,
               "runtime_admitted": False, "selected_battery_curve": None,
               "pcs_status": "conditional_proxy_candidate; target_entry_and_repair_scope_not_qualified",
               "risk_result": None, "remaining_reference_value_usd": 15400000,
               "inputs": {key: {"path": str(path.relative_to(hazard if path.is_relative_to(hazard) else ROOT)),
                                "repository": "Hazard_modeling" if path.is_relative_to(hazard) else "damage_modeling",
                                "sha256": sha(path)} for key, path in paths.items()},
               "outputs": {name: sha(args.output_dir / name) for name in
                           ["pcs_probes.csv", "battery_hypothesis_probes.csv", "known_answer_checks.csv",
                            "candidate_comparison.png"]}}
    (args.output_dir / "audit_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"checks_passed": len(test_rows), "runtime_admitted": False}))


if __name__ == "__main__":
    main()
