#!/usr/bin/env python3
"""Reproduce legacy Flood curves and BESS value arithmetic for research only.

No BESS curve is selected and no BESS loss is calculated. The source evaluator
is reused unchanged. Output is an audit, never an input to a production model.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

from damage_curve_eval import evaluate_curve_record

ROOT = Path(__file__).resolve().parents[2]
CURVE_IDS = ("FS_INV", "FS_SWG", "FS_XFMR", "FS_SCADA", "FS_CABLE")
TREATMENTS = {
    "battery_cabinets": "integrated_enclosure_response_pending; do_not_split_embedded_hardware",
    "pcs": "FS_INV_proxy_candidate_only; compatibility_and_datum_pending",
    "sbos": "civil_mechanism_pending; no_independent_wet_yard_DR",
    "ebos": "mixed_MV_controls_collection; suballocation_pending",
    "installation": "support_cost_once; allocation_pending; no_independent_DR",
    "permitting": "excluded_nonphysical",
    "sales_tax": "excluded_by_reference_physical_value_convention",
    "contingency": "excluded_unallocated_contingency",
    "epc_overhead": "excluded_mixed_original_development_overhead",
    "developer_profit": "excluded_markup",
}


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
    reference = hazard / "docs/plans/_cross_cutting/bess_conus"
    artifact_path = ROOT / "docs/cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json"
    artifact = json.loads(artifact_path.read_text())
    assert sha(artifact_path) == "a08e77ef034e1ecea3e7cd05d13c825921b54d610fca9de8651ebda8e857082d"
    reference_checks = json.loads((reference / "verification/reference_checks.json").read_text())
    for name, digest in reference_checks["sha256"].items():
        assert sha(reference / name) == digest, f"Reference changed: {name}"
    records = {r["curve_id"]: r for r in artifact["curve_records"]}
    assert len(records) == len(artifact["curve_records"])
    source_rows = []
    for curve_id in CURVE_IDS:
        record = records[curve_id]
        points = record["parameters"]["points"]
        assert record["curve_form"] == "piecewise_linear"
        assert points == sorted(points)
        assert len({p[0] for p in points}) == len(points)
        assert all(0 <= p[1] <= 1 for p in points)
        assert all(a[1] <= b[1] for a, b in zip(points, points[1:]))
        checks = [(x, y, "native_knot") for x, y in points]
        checks += [((x0+x1)/2, (y0+y1)/2, "midpoint")
                   for (x0, y0), (x1, y1) in zip(points, points[1:])]
        checks += [(points[0][0]-.01, points[0][1], "outside_domain_helper_clamp_only"),
                   (points[-1][0]+.01, points[-1][1], "outside_domain_helper_clamp_only")]
        for depth, expected, check_kind in checks:
            actual = evaluate_curve_record(record, x=depth)
            assert abs(actual-expected) < 1e-12, (curve_id, depth)
            source_rows.append({"source_curve_id": curve_id,
                                "source_native_depth_m": depth,
                                "source_axis": record["x_axis"],
                                "check_kind": check_kind, "source_dr": actual,
                                "bess_runtime_admitted": False, "bess_loss_usd": None})
    assert len(source_rows) == 95
    with (reference / "reference_budget.csv").open() as stream:
        budget = list(csv.DictReader(stream))
    assert len(budget) == len(TREATMENTS)
    assert {r["row_id"] for r in budget} == set(TREATMENTS)
    value_rows = []
    for row in budget:
        value = Decimal(row["included_usd"])
        excluded = Decimal(row["excluded_usd"])
        gross = Decimal(row["source_usd_per_kwh_usable_ac"]) * Decimal(row["basis_kwh_usable_ac"])
        assert value == gross * Decimal(row["retained_fraction"])
        assert value + excluded == gross
        value_rows.append({"row_id": row["row_id"], "target_group": row["target_group"],
                           "included_usd": str(value), "excluded_usd": str(excluded),
                           "currency_basis": row["currency_basis"],
                           "research_treatment": TREATMENTS[row["row_id"]],
                           "bess_runtime_admitted": False})
    included = sum(Decimal(r["included_usd"]) for r in value_rows)
    excluded = sum(Decimal(r["excluded_usd"]) for r in value_rows)
    assert included == Decimal("109800000")
    assert excluded == Decimal("23400000")
    paths = {"solar_artifact": artifact_path,
             "source_evaluator": ROOT / "scripts/reference_helpers/damage_curve_eval.py",
             "artifact_index": ROOT / "docs/contracts/machine_readable_artifact_index.json",
             "audit_helper": Path(__file__).resolve(),
             "profile": reference / "asset_model.json", "layout": reference / "layout.csv",
             "budget": reference / "reference_budget.csv",
             "pluvial_ponding": hazard / "perils/flood/src/flood/pluvial/ponding.py"}
    inputs = {key: {"repository": "Hazard_modeling" if path.is_relative_to(hazard) else "damage_modeling",
                    "path": str(path.relative_to(hazard if path.is_relative_to(hazard) else ROOT)),
                    "sha256": sha(path)} for key, path in paths.items()}
    # Extract the owned constant for this audit; do not implement a hazard model here.
    import ast
    tree = ast.parse(paths["pluvial_ponding"].read_text())
    caps = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "CAP_M" for t in n.targets)]
    assert caps == [.30]
    by_id = {r["row_id"]: Decimal(r["included_usd"]) for r in value_rows}
    dr = Decimal(str(evaluate_curve_record(records["FS_INV"], x=.15)))
    audit = {
        "schema": "bess_flood_evidence_audit.v1", "change_class": "EVIDENCE_ONLY_NO_OUTPUT_CHANGE",
        "hazard_reference_commit": "23e1aac4d",
        "damage_source_commit": "81d5309313d53f37d6bac91e22dd55b498101d0f",
        "source_evaluations": len(source_rows), "source_curves": list(CURVE_IDS),
        "tolerance": 1e-12, "source_checks_passed": True, "reference_hashes_passed": True,
        "budget_rows_reconciled": len(value_rows), "included_value_usd": str(included),
        "excluded_value_usd": str(excluded),
        "budget_shares_not_qualified_coverage": {k: float(v/included) for k, v in by_id.items()},
        "audit_only_denominator_example": {"source_native_depth_m": .15, "source_dr": str(dr),
            "pcs_hardware_arithmetic_usd": str(dr*by_id["pcs"]),
            "incorrect_whole_plant_arithmetic_usd": str(dr*included),
            "bess_loss_prediction": False},
        "pluvial_existing_cap_m": caps[0], "pluvial_model_changed": False,
        "bess_runtime_admitted": False, "bess_curve_selected": False,
        "bess_loss_usd": None, "bess_eal_usd": None, "bess_tail_metrics": None,
        "inputs": inputs,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "source_curve_audit.csv", source_rows)
    write_csv(args.output_dir / "value_crosswalk.csv", value_rows)
    (args.output_dir / "audit_receipt.json").write_text(json.dumps(audit, indent=2)+"\n")
    print(json.dumps({k: audit[k] for k in ("source_evaluations", "budget_rows_reconciled", "source_checks_passed", "bess_runtime_admitted")}))


if __name__ == "__main__":
    main()
