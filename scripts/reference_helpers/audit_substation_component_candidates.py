#!/usr/bin/env python3
"""Review-only inventory and datum audit; no new curve, loss or runtime binding.

Reads the existing Solar component artifact and station accounting. Groups are
research work queues, not accepted Damage coverage or a component cost allocation.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GROUPS = {
    "controls_and_auxiliaries": {
        "relays_345", "relays_138", "comms", "battery", "station_service"},
    "main_transformers": {"transformers"},
    "yard_breakers_and_disconnects": {
        "345_breaker_count", "138_breaker_count",
        "345_three_phase_disconnect_count", "138_three_phase_disconnect_count"},
    "cables_conduits_trenches": {
        "cable_345", "cable_138", "conduit_345", "conduit_138",
        "trench_345", "trench_138"},
    "building": {"control_house"},
    "remaining_yard_and_civil": {
        "345_three_phase_bus_support_count", "138_three_phase_bus_support_count",
        "345_three_phase_voltage_transformer_set_count",
        "138_three_phase_voltage_transformer_set_count",
        "345_line_deadend_count", "138_line_deadend_count", "hv_arresters",
        "containment", "site", "misc_civil"},
    "outside_current_response": {
        "road", "project_management", "administrative_general",
        "engineering_testing_commissioning"},
}
CANDIDATES = {
    "controls_and_auxiliaries": "FS_SCADA: electronics only; auxiliary transfer unresolved",
    "main_transformers": "FS_XFMR: controls-to-whole-transformer denominator unresolved",
    "yard_breakers_and_disconnects": "FS_SWG: transmission AIS transfer unresolved",
    "cables_conduits_trenches": "FS_CABLE: cable-only candidate; route/termination exposure unresolved",
    "building": "no building-shell candidate selected in this audit",
    "remaining_yard_and_civil": "no blanket residual damage rule selected",
    "outside_current_response": "retain existing outside-response disposition",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hazard-repo", type=Path, default=ROOT.parent / "Hazard_modeling")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    paths = {
        "solar_artifact": ROOT / "docs/cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json",
        "binding_value": ROOT / "docs/contracts/hazard_handoff/substation_flood_screening_v1/value_crosswalk.csv",
        "profile": args.hazard_repo / "docs/plans/_cross_cutting/substation_conus/asset_model.json",
        "pluvial_method": args.hazard_repo / "perils/flood/src/flood/pluvial/ponding.py",
        "audit_helper": Path(__file__).resolve(),
    }
    raw = {k: p.read_bytes() for k, p in paths.items()}
    artifact = json.loads(raw["solar_artifact"])
    profile = json.loads(raw["profile"])
    rows = list(csv.DictReader(raw["binding_value"].decode().splitlines()))
    row_ids = [r["row_id"] for r in rows]
    grouped_ids = [row_id for group in GROUPS.values() for row_id in group]
    assert len(row_ids) == len(set(row_ids)) == len(grouped_ids) == len(set(grouped_ids)) == 31
    assert set(row_ids) == set(grouped_ids)
    curves = {r["curve_id"]: r for r in artifact["curve_records"]}
    for key in ("FS_SCADA", "FS_XFMR", "FS_SWG"):
        assert curves[key]["x_axis"] == "local_depth_above_component_datum_m"
        assert curves[key]["parameters"]["points"][0] == [0.0, 0.0]

    # Read the authored design recursively without inventing a new runtime schema.
    def find_spec(node, key):
        found = []
        if isinstance(node, dict):
            if key in node and isinstance(node[key], dict) and "value" in node[key]:
                found.append(node[key]["value"])
            for child in node.values():
                found.extend(find_spec(child, key))
        elif isinstance(node, list):
            for child in node:
                found.extend(find_spec(child, key))
        return found

    floor, = find_spec(profile, "control_house_floor_above_grade_m")
    transformer, = find_spec(profile, "transformer_control_cabinet_above_grade_m")
    # Extract the literal owner constant, not a duplicated hazard implementation.
    import ast
    tree = ast.parse(raw["pluvial_method"])
    cap, = [ast.literal_eval(n.value) for n in tree.body
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAP_M" for t in n.targets)]
    assert (floor, transformer, cap) == (0.3, 1.0, 0.3), "revisit this audit when profile/domain changes"

    totals = {group: Decimal(0) for group in GROUPS}
    ledger = []
    for row in rows:
        group, = [g for g, ids in GROUPS.items() if row["row_id"] in ids]
        totals[group] += Decimal(row["amount_usd"])
        ledger.append({"row_id": row["row_id"], "amount_usd": row["amount_usd"],
                       "existing_role": row["role"], "research_group": group,
                       "candidate_and_limit": CANDIDATES[group], "component_runtime_admitted": False})
    total = sum(totals.values())
    assert total == Decimal("30415059.81")
    assert total - totals["outside_current_response"] == Decimal("27353236.37")
    receipt = {
        "schema": "substation_component_feasibility_audit.v1", "runtime_admitted": False,
        "change_class": "EVIDENCE_ONLY_NO_OUTPUT_CHANGE", "budget_rows": len(rows),
        "all_rows_once": True, "full_budget_usd": str(total),
        "group_totals_usd": {k: str(v) for k, v in totals.items()},
        "group_totals_are_not_qualified_value_coverage": True,
        "inputs": {k: {"path": str(paths[k].relative_to(ROOT if k not in ("profile", "pluvial_method") else args.hazard_repo)),
                       "repository": "Hazard_modeling" if k in ("profile", "pluvial_method") else "damage_modeling",
                       "sha256": hashlib.sha256(v).hexdigest()} for k, v in raw.items()},
        "datum_checks": [
            {"target": "control_house_floor_as_overtopping_threshold_only", "datum_above_local_grade_m": floor,
             "max_model_depth_m": cap, "max_positive_depth_above_datum_m": max(0, cap-floor),
             "limitation": "floor is not a proven barrier to conduit or other ingress; no whole-station zero"},
            {"target": "transformer_control_cabinet", "datum_above_local_grade_m": transformer,
             "max_model_depth_m": cap, "max_positive_depth_above_datum_m": max(0, cap-transformer),
             "limitation": "direct overtopping only; not whole-transformer or auxiliary coverage"}],
        "numerical_response_selection": "none; existing assembly and Solar artifacts unchanged",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "component_candidate_crosswalk.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ledger[0])); writer.writeheader(); writer.writerows(ledger)
    (args.output_dir / "component_candidate_audit.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "all_rows_once": True, "groups_usd": receipt["group_totals_usd"],
                      "runtime_admitted": False}))


if __name__ == "__main__":
    main()
