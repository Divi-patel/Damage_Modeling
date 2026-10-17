#!/usr/bin/env python3
"""Execute a non-reportable station-binding review against the pinned Flood response.

No curve is copied or fitted. Candidate dollars are audit arithmetic, not admitted
scenario loss. Annual metrics and whole-station loss remain null. This is a research
helper, not the Hazard runtime or a new Damage cell.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BINDING = ROOT / "docs/plans/substation_damage/flood_binding_candidate.json"
CENT = Decimal("0.01")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def cents(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def load_review(binding_path: Path = DEFAULT_BINDING, hazard_repo: Path | None = None) -> dict:
    """Verify exact input bytes and reconcile every row before doing audit arithmetic."""
    hazard_repo = hazard_repo or ROOT.parent / "Hazard_modeling"
    raw = binding_path.read_bytes()
    binding = json.loads(raw)
    require(binding["schema_id"] == "substation_flood_binding.research.v1", "wrong review schema")
    require(binding["runtime_admitted"] is False, "research helper cannot admit runtime")
    require(binding["status"] == "proposed", "review requires proposed binding")
    require(binding["station_count"] == 1 and not isinstance(binding["station_count"], bool),
            "one physical station is required")
    require(binding["response_grain"] == "whole_substation_assembly", "assembly grain required")
    require(binding["component_responses_added"] == [], "assembly/component overlap prohibited")
    require(binding["annual_metrics_status"] == "withheld", "annual metrics must remain withheld")
    require(binding["target_transfer_status"] == "proposed_screening_proxy_not_admitted",
            "this helper cannot approve physical transfer")
    contents = {}
    for key, record in binding["inputs"].items():
        root = {"damage_modeling": ROOT, "Hazard_modeling": hazard_repo}[record["repository"]]
        path = (root / record["path"]).resolve()
        require(path.is_relative_to(root.resolve()), "input must stay in its declared repository")
        data = path.read_bytes()
        require(digest(data) == record["sha256"], f"input SHA mismatch: {key}")
        contents[key] = data
    artifact = json.loads(contents["damage_artifact"])
    capability = json.loads(contents["damage_capability"])
    require(artifact["capability_declaration"] == capability, "capability mismatch")
    require(capability["consumer_annual_metrics"]["status_after_promotion"] == "withheld",
            "parent annual capability changed; requalify this review")
    helper_path = ROOT / binding["inputs"]["damage_evaluator"]["path"]
    spec = importlib.util.spec_from_file_location("pinned_flood_binding_evaluator", helper_path)
    require(spec is not None and spec.loader is not None, "source evaluator unavailable")
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    evaluator.verify_artifact_pin(artifact, binding["damage_pin"],
                                  artifact_sha256_hex=digest(contents["damage_artifact"]))
    require(binding["failure_unit_id"] == evaluator.SUPPORTED_FAILURE_UNIT, "wrong source unit")
    require(binding["selectors"]["source_assumption_set_id"] == evaluator.SUPPORTED_ASSUMPTION_SET,
            "source assumption set changed")
    require(binding["selectors"]["substation_hazus_class"] == "ESSM", "candidate class changed")
    require(binding["pathway_id"] == evaluator.SUPPORTED_PATHWAY, "wrong source pathway")

    budget = list(csv.DictReader(io.StringIO(contents["hazard_budget"].decode())))
    summary = json.loads(contents["hazard_budget_summary"])
    require(summary["physical_model_sha256"] == digest(contents["hazard_profile"]), "profile drift")
    require(summary["budget_csv_sha256"] == digest(contents["hazard_budget"]), "budget drift")
    ids = [row["row_id"] for row in budget]
    require(len(ids) == len(set(ids)), "duplicate budget row")
    included = binding["value_policy"]["candidate_assembly_row_ids"]
    outside = binding["value_policy"]["outside_assembly_row_ids"]
    require(len(included + outside) == len(set(included + outside)), "value rows overlap or repeat")
    require(set(included + outside) == set(ids), "value rows missing or invented")
    require(outside == ["road"], "outside-road disposition changed; new review required")
    ledger = []
    direct = Decimal(0)
    for row in budget:
        amount = cents(Decimal(row["quantity"]) * Decimal(row["unit_cost_usd"]))
        require(amount == Decimal(row["amount_usd"]), f"row arithmetic mismatch: {row['row_id']}")
        direct += amount
        in_assembly = row["row_id"] in included
        ledger.append({"row_id": row["row_id"], "item": row["item"], "amount_usd": str(amount),
                       "disposition": "candidate_assembly_denominator" if in_assembly else "outside_assembly",
                       "rationale_id": binding["value_policy"]["row_rationale_ids"][row["row_id"]],
                       "runtime_admitted": False})
    require(direct == Decimal(str(summary["direct_installed_budget_usd"])), "direct sum mismatch")
    for key, value in summary["separate_support_allowances_usd"].items():
        ledger.append({"row_id": key, "item": key, "amount_usd": str(Decimal(str(value))),
                       "disposition": "support_treatment_unresolved", "rationale_id": "V-SUPPORT",
                       "runtime_admitted": False})
    total = sum((Decimal(row["amount_usd"]) for row in ledger), Decimal(0))
    assembly = sum((Decimal(row["amount_usd"]) for row in ledger
                    if row["disposition"] == "candidate_assembly_denominator"), Decimal(0))
    require(total == Decimal(str(summary["including_support_budget_usd"])), "full value mismatch")
    require(assembly == Decimal(binding["expected_candidate_assembly_usd"]), "candidate value changed")
    return {"binding": binding, "binding_sha256": digest(raw), "artifact": artifact,
            "evaluator": evaluator, "ledger": ledger, "candidate_assembly_usd": assembly,
            "total_budget_usd": total, "outside_candidate_usd": total - assembly}


def evaluate_review(review: dict, event: dict[str, Any]) -> dict:
    """Return source DR and explicitly non-reportable candidate arithmetic only."""
    result = {"status": "withheld", "runtime_admitted": False,
              "binding_sha256": review["binding_sha256"], "source_dr": None,
              "audit_candidate_assembly_loss_usd": None, "scenario_loss_usd": None,
              "whole_station_loss_usd": None,
              "annual_metrics": {key: None for key in ("eal_usd", "pml_usd", "var_usd", "tvar_usd")},
              "reason_codes": [], "flags": ["RESEARCH_ONLY", "TARGET_TRANSFER_NOT_ADMITTED",
              "CANDIDATE_VALUE_POLICY_T4", "ANNUAL_AND_TAIL_METRICS_WITHHELD",
              "NOT_NATIVE_HAZARD_COUPLING", "FULL_STATION_LOSS_WITHHELD"]}
    if event.get("metric", "conditional_event_audit") != "conditional_event_audit":
        result["reason_codes"] = ["ANNUAL_OR_OTHER_OUTPUT_NOT_ADMITTED"]
        return result
    allowed = {"metric", "flood_depth_above_substation_grade_ft", "water_surface_elevation_m",
               "substation_grade_elevation_m", "water_surface_vertical_datum_id",
               "substation_grade_vertical_datum_id", "water_quality_class", "delivered_depth_basis",
               "contact_duration_hr"}
    require(not (set(event) - allowed), "unknown field: no implicit height/value/component overrides")
    b = review["binding"]
    request = {"pathway_id": b["pathway_id"], "failure_unit_id": b["failure_unit_id"],
               **b["selectors"], **{k: v for k, v in event.items() if k != "metric"}}
    try:
        source_emit = review["evaluator"].evaluate_damage_call(review["artifact"], request)
    except review["evaluator"].FloodWindEvaluationError as exc:
        result["reason_codes"] = [exc.code]
        return result
    unit = source_emit["failure_unit_results"][0]
    result["hazard_input_used"] = source_emit["hazard_input_used"]
    result["source_helper_scenario_loss_status"] = source_emit["input_quality"]["scenario_loss_status"]
    result["source_dr"] = unit["scalar_central_dr"]
    result["reason_codes"] = unit["withheld_reason_codes"]
    result["flags"] = list(dict.fromkeys(result["flags"] + unit["metadata_flags"]))
    if result["source_dr"] is not None:
        result["status"] = "audit_arithmetic_only"
        loss = cents(Decimal(str(result["source_dr"])) * review["candidate_assembly_usd"])
        require(0 <= loss <= review["candidate_assembly_usd"], "candidate physical cap failed")
        result["audit_candidate_assembly_loss_usd"] = float(loss)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", type=Path, default=DEFAULT_BINDING)
    parser.add_argument("--hazard-repo", type=Path, default=ROOT.parent / "Hazard_modeling")
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "docs/extra/discussion/substation_damage/verification")
    args = parser.parse_args()
    review = load_review(args.binding, args.hazard_repo)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / "flood_binding_value_crosswalk.csv"
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(review["ledger"][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(review["ledger"])
    examples = []
    for depth in [0, 1, 3, 4, 5.5, 7, 10, 10.01]:
        event = {"flood_depth_above_substation_grade_ft": depth,
                 "water_quality_class": "freshwater_non_contaminated",
                 "delivered_depth_basis": "unprotected_or_internal_post_bypass_depth"}
        examples.append({"input": event, "result": evaluate_review(review, event)})
    output = {"status": "proposed_binding_review", "runtime_admitted": False,
              "binding_sha256": review["binding_sha256"],
              "review_helper_sha256": digest(Path(__file__).read_bytes()),
              "source_inputs": review["binding"]["inputs"],
              "candidate_assembly_usd": str(review["candidate_assembly_usd"]),
              "full_candidate_budget_usd": str(review["total_budget_usd"]),
              "outside_candidate_assembly_usd": str(review["outside_candidate_usd"]),
              "station_count": 1, "value_rows": len(review["ledger"]),
              "examples": examples,
              "limitations": review["binding"]["limitations"]}
    (args.output_dir / "flood_binding_review.json").write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: output[key] for key in ["status", "runtime_admitted", "candidate_assembly_usd",
                                                   "outside_candidate_assembly_usd", "value_rows"]}))


if __name__ == "__main__":
    main()
