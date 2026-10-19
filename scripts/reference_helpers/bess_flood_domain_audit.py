#!/usr/bin/env python3
"""Research-only BESS domain comparisons against saved local Riverine evidence.

No runtime import, artifact promotion, new hazard calculation or annual metric.
Run with Hazard's existing Python environment (pandas/pyarrow). Never imported
by a production consumer. The candidate, budget and saved evidence are pinned.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "docs/cells/flood_bess/proposed/local_candidate_v0_1"
PIN_SHA = "68b3b60684638dc9c03f115f93d235921ff8af4b710a01a52330c05dfa11c953"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hazard-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    hazard = args.hazard_repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    tests: list[dict] = []

    def check(name: str, actual: object, expected: object) -> None:
        ok = math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-7) if isinstance(expected, float) else actual == expected
        if not ok:
            raise AssertionError((name, actual, expected))
        tests.append({"check_id": name, "actual": actual, "expected": expected, "result": "PASS"})

    check("original_pin", sha(CANDIDATE / "consumption_pin.json"), PIN_SHA)
    pin = json.loads((CANDIDATE / "consumption_pin.json").read_text())
    for name, digest in pin["sha256"].items():
        check("candidate_" + name, sha(CANDIDATE / name), digest)
    binding = json.loads((CANDIDATE / "value_binding.json").read_text())
    artifact = json.loads((CANDIDATE / "curve_artifact.json").read_text())
    for name, digest in binding["reference_sha256"].items():
        check("reference_" + name, sha(hazard / "docs/plans/_cross_cutting/bess_conus" / name), digest)
    units = binding["units"]
    points = next(r["parameters"]["points"] for r in artifact["curve_records"]
                  if r["curve_id"] == units["pcs"]["curve_id"])
    check("pcs_terminal_dr", points[-1][1], 1.)
    check("pcs_saturated_at_native_point_6", next(y for x, y in points if x == .6), 1.)

    def policy_cost(kind: str, depth: object, water: str, policy: str,
                    hazard_status: str = "available") -> float | None:
        """Explicit what-if policies; not an admitted vulnerability evaluator."""
        if kind not in units or hazard_status != "available":
            return None
        if isinstance(depth, bool) or not isinstance(depth, (float, int)):
            return None
        if not math.isfinite(depth) or depth < 0:
            return None
        if water not in ("freshwater_screening", "saline_screening"):
            return None
        if policy == "current_v0_1":
            if water != "freshwater_screening" or depth > 2.3:
                return None
        elif policy == "freshwater_saturation_only":
            if water != "freshwater_screening":
                return None
        elif policy == "saline_same_proxy_hypothesis":
            if water != "saline_screening":
                return None
        elif policy == "saline_contact_replacement_hypothesis":
            if water != "saline_screening":
                return None
        else:
            return None
        unit = units[kind]
        h = max(0., depth - unit["assumed_entry_m"])
        if kind == "battery_enclosures" or policy == "saline_contact_replacement_hypothesis":
            dr = float(depth > unit["assumed_entry_m"])
        elif h >= points[-1][0]:
            dr = 1.  # explicit saturation hypothesis, never linear extrapolation
        else:
            dr = 0.
            for (x0, y0), (x1, y1) in zip(points, points[1:]):
                if x0 <= h <= x1:
                    dr = y0 + (y1 - y0) * (h - x0) / (x1 - x0)
                    break
        return dr * unit["same_unit_value_usd"]

    active = units["battery_enclosures"]["same_unit_value_usd"]
    pcs = units["pcs"]["same_unit_value_usd"]
    for policy, water in [("current_v0_1", "freshwater_screening"),
                          ("freshwater_saturation_only", "freshwater_screening"),
                          ("saline_same_proxy_hypothesis", "saline_screening"),
                          ("saline_contact_replacement_hypothesis", "saline_screening")]:
        for value in (None, float("nan"), float("inf"), -.01, True, "1"):
            check(f"invalid_{policy}_{value}", policy_cost("pcs", value, water, policy), None)
        check("unknown_water_" + policy, policy_cost("pcs", 1., "unknown", policy), None)
        check("missing_hazard_" + policy, policy_cost("pcs", 1., water, policy, "missing_hand"), None)
        check("no_mv_admission_" + policy, policy_cost("mv", 1., water, policy), None)
        check("exact_entry_zero_" + policy, policy_cost("pcs", .3, water, policy), 0.)
    check("freshwater_no_saline_default", policy_cost("pcs", 1., "saline_screening", "freshwater_saturation_only"), None)
    check("current_deep_withheld", policy_cost("pcs", 3., "freshwater_screening", "current_v0_1"), None)
    check("deep_battery_cap", policy_cost("battery_enclosures", 10., "freshwater_screening", "freshwater_saturation_only"), active)
    check("deep_pcs_cap", policy_cost("pcs", 10., "freshwater_screening", "freshwater_saturation_only"), pcs)
    check("pcs_point45_fresh", policy_cost("pcs", .45, "freshwater_screening", "freshwater_saturation_only"), 390000.)
    check("pcs_point45_saline_hypothesis", policy_cost("pcs", .45, "saline_screening", "saline_contact_replacement_hypothesis"), pcs)

    examples = []
    for depth in (0., .15, .30, .32, .45, .60, .90, 2.3, 3., 10.):
        for policy, water in [("current_v0_1", "freshwater_screening"),
                              ("freshwater_saturation_only", "freshwater_screening"),
                              ("saline_same_proxy_hypothesis", "saline_screening"),
                              ("saline_contact_replacement_hypothesis", "saline_screening")]:
            a = policy_cost("battery_enclosures", depth, water, policy)
            b = policy_cost("pcs", depth, water, policy)
            examples.append({"external_depth_m": depth, "water_condition": water,
                             "research_policy": policy, "one_enclosure_active_usd": a,
                             "one_pcs_usd": b,
                             "whole_reference_uniform_depth_candidate_only_usd": None if a is None or b is None else 80*a + 20*b,
                             "complete_plant_loss_usd": None,
                             "interpretation": "RESEARCH_WHAT_IF_NOT_ANNUAL_OR_ADMITTED"})

    source = hazard / "data/bess/flood_local/20261018_riverine_r2/riverine_unit_cases.parquet"
    # Use the committed receipt, not a newly computed hash as evidence of integrity.
    receipt_path = hazard / "docs/plans/_cross_cutting/bess_conus/verification/riverine_local_proof.json"
    receipt = json.loads(receipt_path.read_text())
    check("saved_riverine_hash_in_committed_receipt", sha(source), receipt["output_sha256"][source.name])
    frame = pd.read_parquet(source)
    check("saved_case_count", len(frame), 43800)
    check("saved_full_plant_cost_absent", bool(frame.complete_plant_loss_usd.isna().all()), True)
    check("unique_case_keys", not frame.duplicated(["cell_id", "placement", "instance_id", "rp_years"]).any(), True)
    fresh = [policy_cost(r.unit_kind, r.external_depth_m, "freshwater_screening", "freshwater_saturation_only", r.hazard_status)
             for r in frame.itertuples()]
    original = [policy_cost(r.unit_kind, r.external_depth_m, "freshwater_screening", "current_v0_1", r.hazard_status)
                for r in frame.itertuples()]
    prior = frame.candidate_hardware_loss_usd
    parity = all((a is None and pd.isna(b)) or (a is not None and not pd.isna(b) and math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-7))
                 for a, b in zip(original, prior))
    check("original_policy_all_saved_cases_parity", parity, True)
    frame["research_freshwater_saturation_cost"] = fresh
    recovered = frame.reason.eq("OUTSIDE_LOCAL_TEST_DOMAIN")
    check("recoverable_known_deep_cases", int(recovered.sum()), 876)
    check("all_known_deep_recovered", bool(frame.loc[recovered, "research_freshwater_saturation_cost"].notna().all()), True)
    check("missing_hazard_stays_missing", bool(frame.loc[frame.hazard_status.ne("available"), "research_freshwater_saturation_cost"].isna().all()), True)
    check("new_available_cases", int(frame.research_freshwater_saturation_cost.notna().sum()), 35151)
    check("candidate_scope_value_preserved", 80*active + 20*pcs + binding["unmodeled_value_usd"], binding["reference_tiv_usd"])
    caps = frame.unit_kind.map({k: v["same_unit_value_usd"] for k, v in units.items()})
    check("all_proposed_costs_within_same_unit_cap", bool((frame.research_freshwater_saturation_cost.dropna() <= caps.loc[frame.research_freshwater_saturation_cost.notna()]).all()), True)

    impacts = []
    for (cell, placement, rp), group in frame.groupby(["cell_id", "placement", "rp_years"], sort=True):
        impacts.append({"cell_id": int(cell), "placement": placement, "rp_years": int(rp),
                        "unit_count": len(group), "prior_available": int(group.candidate_hardware_loss_usd.notna().sum()),
                        "research_available": int(group.research_freshwater_saturation_cost.notna().sum()),
                        "known_deep_units_recovered": int(group.reason.eq("OUTSIDE_LOCAL_TEST_DOMAIN").sum()),
                        "prior_partial_candidate_sum_usd": float(group.candidate_hardware_loss_usd.sum()),
                        "research_partial_candidate_sum_usd": float(group.research_freshwater_saturation_cost.sum()),
                        "complete_plant_loss_usd": None,
                        "interpretation": "DIAGNOSTIC_SAME_RP_SURFACES_NOT_JOINT_EVENT_OR_SAMPLE"})
    write_csv(output / "policy_examples.csv", examples)
    write_csv(output / "riverine_domain_impact.csv", impacts)
    write_csv(output / "known_answer_checks.csv", tests)
    result = {"classification": "EVIDENCE_ONLY_NO_OUTPUT_CHANGE", "runtime_admitted": False,
              "checks_passed": len(tests), "source_cases": len(frame), "prior_available": int(prior.notna().sum()),
              "research_available_after_saturation": int(frame.research_freshwater_saturation_cost.notna().sum()),
              "known_deep_cases_recovered": int(recovered.sum()),
              "recovered_by_unit_kind": {k: int(v) for k, v in frame.loc[recovered].unit_kind.value_counts().items()},
              "missing_hazard_cases_unchanged": int(frame.research_freshwater_saturation_cost.isna().sum()),
              "diagnostic_scenarios_with_100_candidate_units_before": sum(r["prior_available"] == 100 for r in impacts),
              "diagnostic_scenarios_with_100_candidate_units_after": sum(r["research_available"] == 100 for r in impacts),
              "maximum_observed_depth_m": float(frame.external_depth_m.max()),
              "candidate_scope_value_usd": 80*active + 20*pcs,
              "unmodeled_property_value_usd": binding["unmodeled_value_usd"],
              "reference_tiv_usd": binding["reference_tiv_usd"],
              "saline_policy_status": "UNADMITTED_RESEARCH_HYPOTHESIS_REQUIRES_SEPARATE_REPAIR_POLICY_REVIEW",
              "inputs_sha256": {str(p): sha(p) for p in (source, receipt_path, CANDIDATE / "consumption_pin.json")},
              "candidate_sha256": pin["sha256"], "script_sha256": sha(Path(__file__)),
              "outputs_sha256": {p: sha(output / p) for p in ("policy_examples.csv", "riverine_domain_impact.csv", "known_answer_checks.csv")}}
    (output / "audit_receipt.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if not k.endswith("sha256")}, indent=2))


if __name__ == "__main__":
    main()
