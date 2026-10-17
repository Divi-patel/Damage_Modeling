#!/usr/bin/env python3
"""Reproduce a bounded reuse review; never publish a new Damage cell or loss result.

Reads exact Git blobs from Damage and Hazard. Exercises the existing Flood/Wind
reference evaluator against the retained source table, then accounts for every
canonical-station budget row. The result proves reproducibility, not transfer
approval. Run from a checkout containing the two pinned commits.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import subprocess
import sys
from decimal import Decimal

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
DAMAGE_COMMIT = "02eba9be57e40ae5301fa02a45c7a49d5e86b204"
HAZARD_COMMIT = "509bf435e1990a5d04d59c0c34621cc2d9a82fdb"
CELL = "docs/cells/flood_wind/current/"
ARTIFACT = CELL + "flood_wind__model_v1_0__docs_r1__curve_artifact.json"
CAPABILITY = CELL + "flood_wind__model_v1_0__docs_r1__capability.json"
HELPER = "scripts/reference_helpers/flood_wind_curve_eval.py"
PROFILE = "docs/plans/_cross_cutting/substation_conus/"
UNIT = "FW_HAZUS_GSU_SUBSTATION_ASSEMBLY"
PATHWAY = "flood_inundation_contact"
# Independently transcribed from the retained dossier's Table 7.9, not read back
# from the JSON under test. Fresh primary-PDF access remains a separate task.
SOURCE_PERCENT = [0, 2, 4, 6, 7, 8, 9, 10, 12, 14, 15]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{commit}:{path}"])


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hazard-repo", type=Path, default=ROOT.parent / "Hazard_modeling")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs/extra/discussion/substation_damage/verification")
    args = parser.parse_args()
    receipts = []

    def read(repo: Path, commit: str, path: str, repo_name: str) -> bytes:
        data = blob(repo, commit, path)
        receipts.append({"repository": repo_name, "commit": commit, "path": path,
                         "sha256": sha(data), "bytes": len(data)})
        return data

    artifact = json.loads(read(ROOT, DAMAGE_COMMIT, ARTIFACT, "Damage_Modeling"))
    capability = json.loads(read(ROOT, DAMAGE_COMMIT, CAPABILITY, "Damage_Modeling"))
    read(ROOT, DAMAGE_COMMIT, CELL + "flood_wind_curve_derivation_dossier__model_v1_0__docs_r1.md", "Damage_Modeling")
    read(ROOT, DAMAGE_COMMIT, CELL + "SOURCE_REGISTER_flood_wind__model_v1_0__docs_r1.csv", "Damage_Modeling")
    helper_bytes = read(ROOT, DAMAGE_COMMIT, HELPER, "Damage_Modeling")
    require((ROOT / HELPER).read_bytes() == helper_bytes, "Reference evaluator drifted from review pin")
    spec = importlib.util.spec_from_file_location("substation_review_flood_wind", ROOT / HELPER)
    require(spec is not None and spec.loader is not None, "Cannot load reference evaluator")
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    profile_bytes = read(args.hazard_repo, HAZARD_COMMIT, PROFILE + "asset_model.json", "Hazard_modeling")
    budget_bytes = read(args.hazard_repo, HAZARD_COMMIT, PROFILE + "reference_budget.csv", "Hazard_modeling")
    budget = list(csv.DictReader(io.StringIO(budget_bytes.decode())))
    summary = json.loads(read(args.hazard_repo, HAZARD_COMMIT, PROFILE + "reference_budget_summary.json", "Hazard_modeling"))
    require(sha(profile_bytes) == summary["physical_model_sha256"], "Profile/summary mismatch")
    require(sha(budget_bytes) == summary["budget_csv_sha256"], "Budget/summary mismatch")
    require(not summary["runtime_admitted"] and summary["selected_damage_denominator_usd"] is None,
            "Review assumes a candidate profile without an admitted denominator")
    require(artifact["capability_declaration"] == capability, "Embedded/standalone capability mismatch")
    require(capability["consumer_annual_metrics"]["status_after_promotion"] == "withheld", "Annual capability changed")
    pin = {key: artifact[key] for key in ["cell_id", "semantic_damage_model_version", "documentation_revision", "schema_version"]}
    pin["artifact_sha256"] = receipts[0]["sha256"]
    evaluator.verify_artifact_pin(artifact, pin, artifact_sha256_hex=pin["artifact_sha256"])
    cases = []
    base = {"pathway_id": PATHWAY, "failure_unit_id": UNIT, "substation_hazus_class": "ESSM",
            "source_assumption_set_id": "FEMA_HAZUS_MH_2_1_TABLE_7_9_UNPROTECTED_SUBSTATION",
            "water_quality_class": "freshwater_non_contaminated",
            "delivered_depth_basis": "unprotected_or_internal_post_bypass_depth",
            "flood_depth_above_substation_grade_ft": 4.0}

    def check(name: str, request: dict, expected_dr=None, expected_reason=None) -> None:
        try:
            emit = evaluator.evaluate_damage_call(artifact, request)
            row = emit["failure_unit_results"][0]
            actual = row["scalar_central_dr"]
            reasons = row["withheld_reason_codes"]
            if expected_reason:
                require(actual is None and row["status"] == "withheld" and expected_reason in reasons, name)
            else:
                require(actual is not None and math.isclose(actual, expected_dr, abs_tol=1e-12, rel_tol=0), name)
            outcome = row["status"]
        except evaluator.FloodWindEvaluationError as exc:
            require(exc.code == expected_reason, f"{name}: unexpected {exc.code}")
            actual, reasons, outcome = None, [exc.code], "rejected"
        cases.append({"case_id": name, "request": request, "expected_dr": expected_dr,
                      "expected_reason": expected_reason, "actual_dr": actual,
                      "actual_reasons": reasons, "outcome": outcome, "passed": True})

    for source_class in ["ESSL", "ESSM", "ESSH"]:
        for depth, percent in enumerate(SOURCE_PERCENT):
            check(f"{source_class}_knot_{depth}", {**base, "substation_hazus_class": source_class,
                  "flood_depth_above_substation_grade_ft": depth}, percent / 100)
        for depth in range(10):
            check(f"{source_class}_midpoint_{depth}", {**base, "substation_hazus_class": source_class,
                  "flood_depth_above_substation_grade_ft": depth + 0.5},
                  (SOURCE_PERCENT[depth] + SOURCE_PERCENT[depth + 1]) / 200)
    bridge = {k: v for k, v in base.items() if k != "flood_depth_above_substation_grade_ft"}
    bridge.update(water_surface_elevation_m=101.6764, substation_grade_elevation_m=100,
                  water_surface_vertical_datum_id="NAVD88", substation_grade_vertical_datum_id="NAVD88")
    check("same_datum_metres_5p5ft", bridge, 0.085)
    check("datum_mismatch", {**bridge, "substation_grade_vertical_datum_id": "NGVD29"}, expected_reason="VERTICAL_DATUM_MISMATCH")
    check("both_axes", {**bridge, "flood_depth_above_substation_grade_ft": 4}, expected_reason="AXIS_PAYLOAD_AMBIGUOUS")
    for depth, reason in [(-0.1, "AXIS_OUTSIDE_VALID_RANGE"), (10.01, "ABOVE_SOURCE_VALID_RANGE")]:
        check(f"depth_{depth}", {**base, "flood_depth_above_substation_grade_ft": depth}, expected_reason=reason)
    for water in ["freshwater_contaminated", "brackish", "saltwater", "chemically_contaminated", "unknown"]:
        check(f"water_{water}", {**base, "water_quality_class": water}, expected_reason="WATER_QUALITY_OUTSIDE_SCREENING_DOMAIN")
    for field, reason in [("water_quality_class", "WATER_QUALITY_CLASS_REQUIRED"),
                          ("source_assumption_set_id", "SOURCE_ASSUMPTION_SET_REQUIRED"),
                          ("flood_depth_above_substation_grade_ft", "AXIS_PAYLOAD_REQUIRED")]:
        check(f"missing_{field}", {k: v for k, v in base.items() if k != field}, expected_reason=reason)
    check("wrong_pathway", {**base, "pathway_id": "flood_scour"}, expected_reason="PATHWAY_ID_UNKNOWN")
    check("wrong_class", {**base, "substation_hazus_class": "HV"}, expected_reason="SUBSTATION_HAZUS_CLASS_UNSUPPORTED")
    check("wrong_assumptions", {**base, "source_assumption_set_id": "our_exact_station"}, expected_reason="SOURCE_ASSUMPTION_SET_UNSUPPORTED")
    for unit in artifact["failure_units"]:
        if unit["id"] != UNIT:
            check("withheld_" + unit["id"], {**base, "failure_unit_id": unit["id"]}, expected_reason="NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT")
    try:
        evaluator.verify_artifact_pin(artifact, {**pin, "artifact_sha256": "0" * 64}, artifact_sha256_hex=pin["artifact_sha256"])
        raise ValueError("Wrong SHA was accepted")
    except evaluator.FloodWindEvaluationError as exc:
        require(exc.code == "ARTIFACT_PIN_MISMATCH", "Wrong pin rejection reason")

    # All groups below are research dispositions, never fractions usable by M3.
    unresolved = {"containment", "control_house", "site", "misc_civil", "trench_345", "trench_138"}
    rows = []
    for row in budget:
        row_id = row["row_id"]
        if row_id == "road":
            group, reason = "outside_assembly", "External access road has no response in this electrical assembly; remains in full physical budget."
        elif row_id in unresolved:
            group, reason = "scope_unresolved", "Mixed or civil value needs source-denominator qualification; do not remove or include by label alone."
        else:
            group, reason = "candidate_assembly_member", "Equipment/cabling plausibly belongs to the source assembly; exact repair denominator and transfer remain unqualified."
        rows.append({"row_id": row_id, "item": row["item"], "amount_usd": row["amount_usd"],
                     "source_file": PROFILE + "reference_budget.csv", "disposition": group,
                     "candidate_response": UNIT if group == "candidate_assembly_member" else "",
                     "runtime_admitted": "false", "allocation_fraction": "", "reason": reason})
    for name, amount in summary["separate_support_allowances_usd"].items():
        rows.append({"row_id": "support_" + name, "item": name, "amount_usd": str(amount),
                     "source_file": PROFILE + "reference_budget_summary.json", "disposition": "support_unallocated",
                     "candidate_response": "", "runtime_admitted": "false", "allocation_fraction": "",
                     "reason": "New-build overhead is not an independent fragility or automatically repair cost; separate repair-support method required."})
    require(len(budget) == 28 and len(rows) == 31, "Budget row count drift")
    require(len({r["row_id"] for r in rows}) == len(rows), "Duplicate value row")
    totals = {}
    for row in rows:
        group = row["disposition"]
        totals[group] = totals.get(group, Decimal(0)) + Decimal(row["amount_usd"])
    total = sum(totals.values())
    require(total == Decimal(str(summary["including_support_budget_usd"])), "Value accounting does not close")
    require(sum(Decimal(row["amount_usd"]) for row in rows[:28]) == Decimal(str(summary["direct_installed_budget_usd"])), "Direct subtotal differs")
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "value_review.csv", rows)
    report = {"author": "owner-directed (Divy); agent-researched", "review_date": "2026-10-16",
              "status": "passed_reproducibility_and_accounting_only", "standalone_substation_runtime_admitted": False,
              "fresh_primary_table_verified": False, "selected_damage_denominator_usd": None,
              "review_script_sha256": sha(Path(__file__).read_bytes()), "input_receipts": receipts,
              "source_table_basis": "retained governed Flood/Wind dossier; primary PDF fresh retrieval unavailable",
              "curve_case_count": len(cases), "curve_cases": cases, "wrong_pin_rejected": True,
              "value_row_count": len(rows), "budget_total_usd": str(total),
              "research_disposition_totals_usd": {key: str(value) for key, value in totals.items()},
              "annual_metrics": "withheld_by_existing_capability",
              "reference_helper_limitation": "Retains historical scenario_loss_status=withheld_noncanonical_proposal; this probe tests DR only, not production admission or dollar loss."}
    (output / "review_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["status", "curve_case_count", "value_row_count", "budget_total_usd", "research_disposition_totals_usd", "standalone_substation_runtime_admitted"]}, indent=2))


if __name__ == "__main__":
    main()
