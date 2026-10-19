"""Research-only reproduction of existing TC-wind records; never a BESS evaluator."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
HAZARD = ROOT.parent / "Hazard_modeling"
ARTIFACT = ROOT / "docs/cells/tropical_cyclone_wind_solar/current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__curve_artifact.json"
EXPECTED_SHA = "2fbc34fbf8f91df408fe1b3c8d01d260d013119cbcba594b6a9a60044cd2113e"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="") as stream:
        reader = csv.DictReader(stream)
        result = list(reader)
    assert all(None not in row and None not in row.values() for row in result), name
    return result


def main() -> None:
    assert digest(ARTIFACT) == EXPECTED_SHA
    index_path = ROOT / "docs/contracts/machine_readable_artifact_index.json"
    index_bytes = index_path.read_bytes()
    index = json.loads(index_bytes)
    indexed = next(x for x in index["artifacts"] if x["cell_id"] == "tropical_cyclone_wind_solar")
    assert indexed["sha256"] == EXPECTED_SHA
    assert [x["cell_id"] for x in index["artifacts"] if "bess" in x["cell_id"]] == ["flood_bess"]
    sys.path.insert(0, str(ROOT / "scripts/reference_helpers"))
    import tropical_cyclone_wind_solar_v2_1_curve_eval as source

    artifact = json.loads(ARTIFACT.read_text())
    records = [r for r in artifact["pathways"][0]["curve_records"] if r["x_axis"] == "site_facility_tropical_cyclone_wind_demand_ratio"]
    assert len(records) == 5
    probes = []
    max_delta = 0.0
    ordering_checks = 0

    def evaluate(unit: str, **axis: float) -> dict:
        request = {
            "pathway_id": "tropical_cyclone_wind",
            "event_id": "SOURCE_ONLY_RESEARCH",
            "event_family_id": "tropical_cyclone",
            "failure_unit_id": unit,
            "site_facility_demand_bridge_id": "SOURCE_ONLY_AXIS_AUDIT_NOT_BESS",
            **axis,
        }
        return source.evaluate_damage_call(artifact, request, verified_artifact_sha256_hex=EXPECTED_SHA)["failure_unit_results"][0]

    for record in records:
        params = record["parameters"]
        costs = [s["cost_ratio"] for s in params["damage_states"]]
        for x in (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0):
            result = evaluate(record["failure_unit_id"], tc_site_event_to_design_wind_pressure_ratio=x)
            scenario_values = result["scenario_drs"]
            assert scenario_values["lower_resistance"] >= scenario_values["central_screening"] >= scenario_values["upper_resistance"]
            ordering_checks += 1
            for scenario in params["capacity_scenarios"]:
                # Expected ordered-state cost = sum of incremental costs times exceedance.
                beta = params["beta_ln"]
                exceedance = [0.0 if x == 0 else 0.5 * (1.0 + math.erf(math.log(x / median) / (beta * math.sqrt(2.0)))) for median in scenario["state_medians"]]
                independent = sum((costs[i + 1] - costs[i]) * q for i, q in enumerate(exceedance))
                actual = scenario_values[scenario["scenario_id"]]
                delta = abs(actual - independent)
                max_delta = max(max_delta, delta)
                assert delta < 1e-14
                probabilities = result["state_probabilities_by_scenario"][scenario["scenario_id"]]
                assert abs(sum(probabilities.values()) - 1.0) < 1e-14
                assert min(probabilities.values()) >= 0.0
                probes.append({"curve_id": record["curve_id"], "source_failure_unit": record["failure_unit_id"], "pressure_ratio": x, "scenario": scenario["scenario_id"], "source_dr": actual, "independent_dr": independent, "bess_response_admitted": False})

    invalid_checks = 0
    for x in (-0.01, 2.01, True):
        try:
            evaluate("PV_POWER_CONVERSION_AND_COLLECTION", tc_site_event_to_design_wind_pressure_ratio=x)
        except source.TropicalCycloneWindSolarV21EvaluationError:
            invalid_checks += 1
        else:
            raise AssertionError(f"invalid source axis admitted: {x}")
    speed_checks = 0
    for record in records:
        direct = evaluate(record["failure_unit_id"], tc_site_event_to_design_wind_pressure_ratio=(50.0 / 60.0) ** 2)
        speed = evaluate(record["failure_unit_id"], tc_peak_gust_3s_10m_mps=50.0, qualified_site_design_3s_gust_mps=60.0)
        assert direct["scenario_drs"] == speed["scenario_drs"]
        speed_checks += 1

    sources = rows("sources.csv")
    ids = {s["source_id"] for s in sources}
    assert len(ids) == len(sources) == 9
    claims = rows("claims.csv")
    for claim in claims:
        assert set(claim["source_ids"].split(";")) <= ids
    reuse = rows("reuse_matrix.csv")
    for row in reuse:
        assert set(row["candidate_source_ids"].split(";")) <= ids
    with (HAZARD / "docs/plans/_cross_cutting/bess_conus/reference_budget.csv").open(newline="") as stream:
        budget = list(csv.DictReader(stream))
    included = sum(float(r["included_usd"]) for r in budget)
    assert included == 109_800_000.0
    excluded = sum(float(r["excluded_usd"]) for r in budget)
    assert excluded == 23_400_000.0
    for row in budget:
        original = float(row["source_usd_per_kwh_usable_ac"]) * float(row["basis_kwh_usable_ac"])
        assert math.isclose(float(row["included_usd"]), original * float(row["retained_fraction"]), abs_tol=1e-8)
        assert math.isclose(float(row["included_usd"]) + float(row["excluded_usd"]), original, abs_tol=1e-8)
        if row["target_group"] == "excluded":
            assert float(row["included_usd"]) == 0.0
    for row in reuse:
        assert float(row["included_usd"]) == sum(float(b["included_usd"]) for b in budget if b["target_group"] == row["target_group"])
    assert sum(float(r["included_usd"]) for r in reuse) == included
    assert len(budget) == 10
    assert all(not r["bess_response_admitted"] for r in probes)

    with (OUT / "source_curve_probes.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(probes[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(probes)

    raw = ROOT / "data/bess/raw_hurricane_review_r1"
    retrievals = json.loads((raw / "retrievals.json").read_text())
    assert all(r["status"] == "cached" for r in retrievals)
    for r in retrievals:
        assert digest(ROOT / r["path"]) == r["sha256"]
    inputs = [ARTIFACT, index_path, Path(__file__).resolve(), HAZARD / "docs/plans/_cross_cutting/bess_conus/asset_model.json", HAZARD / "docs/plans/_cross_cutting/bess_conus/layout.csv", HAZARD / "docs/plans/_cross_cutting/bess_conus/reference_budget.csv", ROOT / "scripts/reference_helpers/tropical_cyclone_wind_solar_v2_1_curve_eval.py", ROOT / "scripts/reference_helpers/tropical_cyclone_wind_solar_v2_curve_eval.py", ROOT / "data/bess/raw_flood_review_r2/sma_storage_mv_manual.pdf", ROOT / "data/bess/raw_flood_review_r2/sungrow_st2752_manual.pdf"]
    receipt = {"classification": "EVIDENCE_ONLY_NO_OUTPUT_CHANGE", "review_date": "2026-10-19", "damage_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "input_hashes": {str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p.relative_to(ROOT.parent)): digest(p) for p in inputs}, "new_source_captures": retrievals, "visually_reviewed_pages": {"BW-S03": "PDF75", "BW-S05": "PDF20 S-102", "BW-S06": "PDF193 printed28"}, "existing_runtime_artifacts_changed": False, "bess_wind_response_admitted": False}
    (OUT / "input_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    assert index_path.read_bytes() == index_bytes
    validation = {"status": "PASS", "scope": "source reproduction and research evidence only", "source_records": len(sources), "claim_records": len(claims), "source_dr_checks": len(probes), "source_scenario_ordering_checks": ordering_checks, "invalid_axis_controls": invalid_checks, "pressure_speed_equivalence_controls": speed_checks, "budget_rows_reconciled": len(budget), "included_value_usd": included, "excluded_source_value_usd": excluded, "independent_dr_max_abs_delta": max_delta, "bess_wind_response_admitted": False, "curve_or_schema_version_changed": False}
    (OUT / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
