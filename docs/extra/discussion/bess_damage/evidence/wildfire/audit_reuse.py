"""Research-only donor reproduction and cost audit; never a BESS evaluator.

Run with Hazard_modeling/.venv/bin/python. Nothing here is a production import.
No proposed BESS curve, annual loss, or fit is emitted.
"""
from __future__ import annotations

import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

from wildfire.api import (
    WildfireDamageContractError,
    load_curated_wildfire_curve,
    run_curated_wildfire_kats,
    wildfire_failure_unit_dr,
)

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
HAZARD = ROOT.parent / "Hazard_modeling"
SOURCE = ROOT / "docs/cells/wildfire_solar/current"
ARTIFACT = SOURCE / "wildfire_solar__model_v1_0__docs_r3__curve_artifact.json"
SHA = "598512fbe2f0a3c8db48df69fdb2cd00ca5e0cc8e7ef761555837a3d76d166d8"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    assert len(set(reader.fieldnames)) == len(reader.fieldnames)
    assert all(None not in r and None not in r.values() for r in data), path
    return data


def save_rows(name, data):
    with (OUT / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def main():
    index = ROOT / "docs/contracts/machine_readable_artifact_index.json"
    before = index.read_bytes()
    entries = json.loads(before)["artifacts"]
    assert digest(ARTIFACT) == SHA
    assert next(e for e in entries if e["cell_id"] == "wildfire_solar")["sha256"] == SHA
    assert not any(e["cell_id"] == "wildfire_bess" for e in entries)
    curve = load_curated_wildfire_curve(ARTIFACT)
    kats = run_curated_wildfire_kats(curve, json.loads((SOURCE / "known_answer_tests_wildfire_solar__model_v1_0__docs_r3.json").read_text()))
    assert kats["status"] == "pass"
    table = rows(SOURCE / "ORDINATE_TABLE_wildfire_solar__model_v1_0__docs_r3.csv")
    selected = ["WSV1_INVERTER_THERMAL", "WSV1_MV_EQUIPMENT_THERMAL", "WSV1_SCADA_THERMAL", "WSV1_CABLE_EXPOSED", "WSV1_CIVIL_DIRECT"]
    state_columns = list(table[0])[3:10]
    probes = []
    for unit in selected:
        row = next(r for r in table if r["failure_unit_id"] == unit)
        expected = [float(row[k]) for k in state_columns]
        assert expected[0] == 0 and all(0 <= x <= 1 for x in expected)
        assert all(a <= b for a, b in zip(expected, expected[1:]))
        for state, target in enumerate(expected):
            actual = wildfire_failure_unit_dr(curve, unit, state_index=state)
            assert actual == target
            probes.append(dict(source_failure_unit=unit, state=state, source_dr=actual,
                               independent_csv_dr=target, bess_response_admitted=False))
    rejected = 0
    for state in [-1, 7, 1.5, True, "3"]:
        try:
            wildfire_failure_unit_dr(curve, selected[0], state_index=state)
        except WildfireDamageContractError:
            rejected += 1
        else:
            raise AssertionError(f"invalid state admitted: {state!r}")
    try:
        wildfire_failure_unit_dr(curve, selected[0], state_index=3, burn_probability=.01)
    except WildfireDamageContractError:
        rejected += 1
    else:
        raise AssertionError("hazard frequency entered Damage")

    budget_path = HAZARD / "docs/plans/_cross_cutting/bess_conus/reference_budget.csv"
    budget = rows(budget_path)
    crosswalk = rows(OUT / "value_crosswalk.csv")
    assert len(crosswalk) == len(budget) == 10
    for r, c in zip(budget, crosswalk):
        assert r["row_id"] == c["row_id"]
        for key in ("target_group", "included_usd", "excluded_usd"):
            assert r[key] == c[key]
        original = Decimal(r["source_usd_per_kwh_usable_ac"]) * Decimal(r["basis_kwh_usable_ac"])
        assert Decimal(r["included_usd"]) + Decimal(r["excluded_usd"]) == original
    total = sum(Decimal(r["included_usd"]) for r in budget)
    assert total == Decimal("109800000")
    reuse = rows(OUT / "reuse_matrix.csv")
    assert sum(Decimal(r["included_usd"]) for r in reuse) == total
    for r in reuse:
        assert Decimal(r["included_usd"]) == sum(Decimal(b["included_usd"]) for b in budget if b["target_group"] == r["target_group"])
    sources = rows(OUT / "sources.csv")
    source_ids = {r["source_id"] for r in sources}
    assert len(source_ids) == len(sources)
    for name in ("claims.csv", "parameters.csv", "reuse_matrix.csv", "value_crosswalk.csv"):
        for r in rows(OUT / name):
            assert set(r["source_ids"].split(";")) <= source_ids

    # Pure cost scenarios for explicitly different inspected outcomes. No hazard
    # state, probability, serviceability determination or Damage DR is inferred.
    allocation_path = ROOT / "docs/extra/discussion/bess_damage/evidence/r3/value_allocations.csv"
    allocation = {r["cost_group"]: float(r["projected_usd_per_enclosure"]) for r in rows(allocation_path) if r["allocation_case"] == "MMP_related_allocation"}
    assert abs(sum(allocation.values()) - 1_050_000) < 1e-8
    policies = [
        ("cooling_shell_rack_safety_only_if_cells_and_BMS_verified_serviceable", allocation["thermal_management"] + allocation["enclosure_racks_fire_suppression"]),
        ("all_noncell_groups_only_if_cells_verified_serviceable", 1_050_000 - allocation["cells"]),
        ("whole_integrated_enclosure_if_battery_compromised", 1_050_000),
    ]
    cost_probes = [dict(hypothesis=name, unit_cost_usd=cost, full_tiv_percent_for_one_unit=100*cost/float(total), wildfire_state_assigned=False, probability_assigned=False, owner_selected_for_wildfire=False) for name, cost in policies]
    assert 0 < cost_probes[0]["unit_cost_usd"] < cost_probes[1]["unit_cost_usd"] < cost_probes[2]["unit_cost_usd"]
    # Hypothetical transfer pressure test: same class, known PCS dollars. These
    # are diagnostic consequences of a possible transfer, never admitted losses.
    pcs_probes = []
    for s in range(7):
        dr = wildfire_failure_unit_dr(curve, selected[0], state_index=s)
        pcs_probes.append(dict(source_state=s, source_dr=dr, one_PCS_hypothetical_usd=dr*520_000, all_20_PCS_same_state_hypothetical_usd=dr*10_400_000, hypothetical_percent_full_tiv=100*dr*10_400_000/float(total), bess_response_admitted=False))
    save_rows("source_curve_probes.csv", probes)
    save_rows("consequence_cost_probes.csv", cost_probes)
    save_rows("pcs_transfer_pressure_test.csv", pcs_probes)
    assert index.read_bytes() == before
    inputs = [ARTIFACT, index, Path(__file__), allocation_path, budget_path,
              HAZARD / "docs/plans/_cross_cutting/bess_conus/asset_model.json",
              HAZARD / "docs/plans/_cross_cutting/bess_conus/layout.csv"]
    receipt = dict(classification="EVIDENCE_ONLY_NO_OUTPUT_CHANGE", review_date="2026-10-19",
                   input_hashes={str(p.relative_to(ROOT.parent)): digest(p) for p in inputs},
                   artifact_index_changed=False, bess_wildfire_response_admitted=False)
    (OUT / "input_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    validation = dict(status="PASS", scope="read-only source reproduction, evidence integrity and cost arithmetic; no BESS runtime",
                      current_index_entries=len(entries), source_records=len(sources), claim_records=len(rows(OUT / "claims.csv")),
                      source_state_comparisons=len(probes), source_published_known_answers=kats,
                      invalid_axis_or_frequency_controls=rejected, budget_rows_reconciled=10,
                      total_physical_value_usd=float(total), excluded_source_value_usd=float(sum(Decimal(r["excluded_usd"]) for r in budget)),
                      cost_hypotheses=cost_probes, source_pcs_pressure_test_cases=len(pcs_probes),
                      bess_wildfire_response_admitted=False, runtime_or_schema_changed=False)
    (OUT / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
