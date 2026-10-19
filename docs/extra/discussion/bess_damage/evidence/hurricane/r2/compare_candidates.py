"""Costed BESS wind research hypotheses; no canonical/runtime evaluator."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[7]
OUT = Path(__file__).resolve().parent
HAZARD = ROOT.parent / "Hazard_modeling"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_csv(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name, rows):
    with (OUT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)


def axis(event, design, comparable=True):
    if not comparable or isinstance(event, bool) or isinstance(design, bool):
        return None
    if not math.isfinite(event) or not math.isfinite(design) or event < 0 or design <= 0:
        return None
    x = (event / design) ** 2
    return x if 0 <= x <= 2 else None


def main():
    spec_path = OUT / "experiment_spec.json"
    spec = json.loads(spec_path.read_text())
    a_path = ROOT / spec["source_response"]["path"]
    assert sha(a_path) == spec["source_response"]["sha256"]
    index = ROOT / "docs/contracts/machine_readable_artifact_index.json"
    index_before = index.read_bytes()
    artifact = json.loads(a_path.read_text())
    record = next(r for r in artifact["pathways"][0]["curve_records"] if r["curve_id"] == spec["source_response"]["curve_id"])
    parameters = record["parameters"]
    assert parameters["beta_ln"] == 0.35
    allocation_path = ROOT / spec["cost_allocation"]["path"]
    allocations = read_csv(allocation_path)
    values = {r["cost_group"]: float(r["projected_usd_per_enclosure"]) for r in allocations if r["allocation_case"] == spec["cost_allocation"]["case"]}
    cabinet = sum(values.values())
    assert abs(cabinet - 1_050_000) < 1e-8
    composite = values["enclosure_racks_fire_suppression"]
    repairable_major = composite + values["thermal_management"]
    costs = {
        "repair_if_contained_hardware_serviceable": [0.0, composite / cabinet, repairable_major / cabinet, 1.0],
        "replace_at_major_compromise": [0.0, composite / cabinet, 1.0, 1.0],
    }
    assert spec["policy_default"] is None
    assert spec["owner_ruling"]["scope"] == "local testing only"
    assert spec["runtime_artifact"] is False
    state_rows = [{"repair_policy": policy, "state": state, "cabinet_cost_fraction": c, "cost_usd_per_enclosure": c * cabinet, "status": "RESEARCH_HYPOTHESIS_NOT_OEM_REPAIR_RULE"} for policy, cs in costs.items() for state, c in zip(spec["states"], cs)]
    write_csv("state_costs.csv", state_rows)
    budget_path = HAZARD / "docs/plans/_cross_cutting/bess_conus/reference_budget.csv"
    budget = read_csv(budget_path)
    assert sum(float(r["included_usd"]) for r in budget) == spec["scope"]["full_tiv_usd"]
    assert 80 * cabinet == 84_000_000
    pcs_value = 10_400_000 / 20
    assert 80 * cabinet + 20 * pcs_value == spec["scope"]["candidate_hardware_usd"]
    assert spec["scope"]["full_tiv_usd"] - spec["scope"]["candidate_hardware_usd"] == 15_400_000
    sys.path.insert(0, str(ROOT / "scripts/reference_helpers"))
    import tropical_cyclone_wind_solar_v2_1_curve_eval as source

    def probabilities(x, scenario):
        assert math.isfinite(x) and 0 <= x <= 2
        exceed = [0 if x == 0 else 0.5 * (1 + math.erf(math.log(x / median) / (parameters["beta_ln"] * math.sqrt(2)))) for median in scenario["state_medians"]]
        return [1 - exceed[0], exceed[0] - exceed[1], exceed[1] - exceed[2], exceed[2]]

    probes = []
    max_delta = 0
    for scenario in parameters["capacity_scenarios"]:
        for i in range(81):
            x = i / 40
            p = probabilities(x, scenario)
            assert min(p) >= 0 and abs(sum(p) - 1) < 1e-14
            source_expected = sum(q * s["cost_ratio"] for q, s in zip(p, parameters["damage_states"]))
            request = {"pathway_id": "tropical_cyclone_wind", "event_id": "RESEARCH_HYPOTHESIS", "event_family_id": "tropical_cyclone", "failure_unit_id": record["failure_unit_id"], "site_facility_demand_bridge_id": "SOURCE_ONLY_NOT_TARGET_QUALIFICATION", "tc_site_event_to_design_wind_pressure_ratio": x}
            evaluated = source.evaluate_damage_call(artifact, request, verified_artifact_sha256_hex=sha(a_path))["failure_unit_results"][0]
            pcs_dr = evaluated["scenario_drs"][scenario["scenario_id"]]
            max_delta = max(max_delta, abs(pcs_dr - source_expected))
            assert abs(pcs_dr - source_expected) < 1e-14
            for policy, cs in costs.items():
                dr = sum(q * c for q, c in zip(p, cs))
                dollars = 80 * cabinet * dr + 20 * pcs_value * pcs_dr
                assert 0 <= dr <= 1 and 0 <= dollars <= 94_400_000
                probes.append({"pressure_ratio": x, "event_design_speed_ratio": math.sqrt(x), "repair_policy": policy, "resistance_scenario": scenario["scenario_id"], "enclosure_mean_dr": dr, "pcs_proxy_mean_dr": pcs_dr, "one_enclosure_mean_usd": cabinet * dr, "one_pcs_mean_usd": pcs_value * pcs_dr, "uniform_plant_event_usd": dollars, "uniform_event_pct_full_tiv": 100 * dollars / 109_800_000, "bess_runtime_admitted": False})
    write_csv("response_probes.csv", probes)
    for scenario in parameters["capacity_scenarios"]:
        for policy in costs:
            seq = [p["enclosure_mean_dr"] for p in probes if p["resistance_scenario"] == scenario["scenario_id"] and p["repair_policy"] == policy]
            assert all(a <= b + 1e-14 for a, b in zip(seq, seq[1:]))
            assert seq[0] == 0
    controls = []
    for event, design, comparable in [(0, 60, True), (50, 60, True), (60, 60, True), (85, 60, True), (-1, 60, True), (60, 0, True), (float("nan"), 60, True), (60, float("inf"), True), (60, 60, False), (True, 60, True)]:
        result = axis(event, design, comparable)
        supported = event in (0, 50, 60) and comparable and not isinstance(event, bool) and design == 60 and math.isfinite(event)
        assert (result is not None) == supported
        controls.append({"event_mps": str(event), "reference_mps": str(design), "comparable_wind_basis": comparable, "pressure_ratio": result, "state": "valid_research_demand" if result is not None else "unavailable_no_clamp"})
    write_csv("axis_controls.csv", controls)
    examples = [p for p in probes if p["pressure_ratio"] in (0.5, 1.0, 1.5, 2.0) and p["resistance_scenario"] == "central_screening"]
    msp = {r["cost_group"]: float(r["projected_usd_per_enclosure"]) for r in allocations if r["allocation_case"] == spec["cost_allocation"]["sensitivity_case"]}
    summary = {"scope": "conditional wind research examples; not annual metrics or observed damage", "one_enclosure_usd": cabinet, "limited_composite_cost_usd": composite, "major_repair_if_hardware_serviceable_usd": repairable_major, "major_integrated_replacement_usd": cabinet, "alternative_allocation_major_repair_usd": msp["enclosure_racks_fire_suppression"] + msp["thermal_management"], "candidate_value_usd": 94_400_000, "candidate_fraction_full_tiv": 94_400_000 / 109_800_000, "unbound_property_usd": 15_400_000, "uniform_event_examples": examples}
    (OUT / "example_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.4))
    colors = {"repair_if_contained_hardware_serviceable": "#246582", "replace_at_major_compromise": "#ad5421"}
    labels = {"repair_if_contained_hardware_serviceable": "Repair if hardware serviceable", "replace_at_major_compromise": "Replace at major compromise"}
    for policy in costs:
        for scenario in parameters["capacity_scenarios"]:
            selected = [p for p in probes if p["repair_policy"] == policy and p["resistance_scenario"] == scenario["scenario_id"]]
            central = scenario["scenario_id"] == "central_screening"
            for ax, field, factor in [(axes[0], "enclosure_mean_dr", 100), (axes[1], "uniform_event_pct_full_tiv", 1)]:
                ax.plot([p["pressure_ratio"] for p in selected], [p[field] * factor for p in selected], color=colors[policy], linestyle="-" if central else "--", alpha=1 if central else 0.5, linewidth=2.1 if central else 1.0, label=labels[policy] if central else None)
    for ax in axes:
        ax.set_xlim(0, 2); ax.set_ylim(0, 100)
        ax.set_xlabel("Pressure demand / reference design pressure")
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_title("One enclosure: conditional mean response")
    axes[0].set_ylabel("Percent of $1.05M enclosure value")
    axes[1].set_title("Uniform plant event: enclosure + PCS")
    axes[1].set_ylabel("Percent of $109.8M full TIV")
    axes[0].legend(frameon=False, fontsize=9, loc="upper left")
    fig.suptitle("BESS Hurricane wind: research hypotheses, not calibrated curves", fontsize=13, y=0.98)
    fig.text(0.06, 0.035, "Solid: inherited central T4 resistance. Dashed: unweighted resistance alternatives, not confidence bounds.\nSame demand at all 80 enclosures and 20 PCS; $15.4M remains unbound. No annual frequency or plant failure distribution.", fontsize=9)
    fig.subplots_adjust(bottom=0.24, top=0.84, wspace=0.3)
    fig.savefig(OUT / "candidate_comparison.png", dpi=160)
    plt.close(fig)
    assert index.read_bytes() == index_before
    captures = [json.loads((ROOT / "data/bess/raw_hurricane_review_r2/source_capture.json").read_text())]
    for name, p in [("BW-S11", ROOT / "data/bess/raw_flood_review_r1/tesla_erg.pdf"), ("BW-S12", ROOT / "data/bess/raw_flood_review_r3/pvscm_2024/UPV 2024Q1.txt")]:
        captures.append({"source_id": name, "path": str(p.relative_to(ROOT)), "sha256": sha(p), "reuse_original_bytes": True})
    (OUT / "source_captures.json").write_text(json.dumps(captures, indent=2) + "\n")
    inputs = [spec_path, a_path, allocation_path, budget_path, Path(__file__).resolve(), ROOT / "scripts/reference_helpers/tropical_cyclone_wind_solar_v2_1_curve_eval.py", ROOT / "scripts/reference_helpers/tropical_cyclone_wind_solar_v2_curve_eval.py", HAZARD / "docs/plans/_cross_cutting/bess_conus/asset_model.json"]
    receipt = {"status": "PASS", "scope": "research candidate arithmetic and admission controls only", "candidate_rows": len(probes), "source_dr_parity_checks": 243, "axis_controls": len(controls), "monotone_policy_scenario_curves": 6, "max_source_dr_delta": max_delta, "owner_ruling": spec["owner_ruling"], "runtime_or_index_changed": False, "annual_metrics_qualified": False, "input_hashes": {str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p.relative_to(ROOT.parent)): sha(p) for p in inputs}}
    (OUT / "audit_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "uniform_event_examples"}, indent=2))
    print(json.dumps({k: v for k, v in receipt.items() if k != "input_hashes"}, indent=2))


if __name__ == "__main__":
    main()
