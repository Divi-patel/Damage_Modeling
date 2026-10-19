"""Deterministic builder for the noncanonical wildfire × real estate model-v0.1 / docs-r1 package.

One pathway (wildfire_building_exposure) × the three Hazard reference profiles r1, from the USFS Wildfire Risk to
Communities structure response (shrub) on the exact FSim flame-length class state, with CAL FIRE DINS same-fire
building factors for the warehouse and office (decision log D-WFRE-01 to D-WFRE-14).

Reads the governed CSVs in docs/cells/wildfire_real_estate/proposed/ (the ordinates come from
derive_wildfire_real_estate_curves.py) and writes:
    wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json   (bundle v3, embedded capability)
    wildfire_real_estate__model_v0_1__docs_r1__capability.json       (identical standalone capability)
    known_answer_tests_wildfire_real_estate__model_v0_1__docs_r1.json
    damage_curve_records_wildfire_real_estate__model_v0_1__docs_r1.xlsx

Known-answer expectations are read here from the ordinates CSV, not by calling the evaluator. Requires openpyxl for
the workbook.

Usage (from the repository root):
    python scripts/reference_helpers/build_wildfire_real_estate_v0_1_package.py
"""
from __future__ import annotations

import csv
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "wildfire_real_estate"
CELL = f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
PW = "wildfire_building_exposure"
UNIT = "WFRE_BUILDING_STRUCTURE"
CONTENTS = "WFRE_BUILDING_CONTENTS"
AXIS = "conditional_flame_length_class_state"
PRODUCT = "USFS_RDS_2016_0034_3_270M"
LO, HI = 0, 6
EXPECTED_RECORDS = 3
NATIVE_CLASS_MAP = {"lt_2_ft": 1, "gte_2_lt_4_ft": 2, "gte_4_lt_6_ft": 3, "gte_6_lt_8_ft": 4,
                    "gte_8_lt_12_ft": 5, "gte_12_ft": 6}
BUILDINGS = {
    "RE_RES_SFD_1S_SLAB": {"profile": "re_house_1s_wood_slab", "factor": 1.0, "dins_group": "house",
                           "flags": ["WRC_HOME_RESPONSE_USED_DIRECTLY", "NO_EMBER_RESISTANT_VENT_OR_DEFENSIBLE_SPACE_CREDIT"]},
    "RE_IND_WAREHOUSE": {"profile": "re_warehouse_1s_steel_slab", "factor": 0.8, "dins_group": "warehouse_like",
                         "flags": ["WRC_HOME_RESPONSE_TIMES_DINS_SAME_FIRE_FACTOR", "BUILDING_FACTOR_T4_TRANSFER_FROM_CALIFORNIA_COMMERCIAL_STOCK"]},
    "RE_COM_OFFICE_3S_SLAB": {"profile": "re_office_3s_slab", "factor": 0.9, "dins_group": "office_like",
                              "flags": ["WRC_HOME_RESPONSE_TIMES_DINS_SAME_FIRE_FACTOR", "BUILDING_FACTOR_T4_TRANSFER_FROM_CALIFORNIA_COMMERCIAL_STOCK"]},
}
ALWAYS = ["NONCANONICAL_PROPOSAL", "SCREENING_AGENCY_RESPONSE_FUNCTION_NOT_FIELD_CALIBRATED",
          "WRC_SHRUB_LIFEFORM_DEFAULT_LIFEFORM_NOT_SUPPLIED", "WRC_LOSS_VALUE_READ_AS_REPAIR_COST_RATIO",
          "FSIM_CLASS_IS_NOT_LOCAL_HEAT_FLUX_OR_EMBER_EXPOSURE", "WHOLE_BUILDING_SOURCE_ATOM",
          "REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED", "NOT_FIELD_OR_CLAIMS_CALIBRATED",
          "CURVE_INTRINSIC_SPREAD_NOT_CARRIED", "PLATFORM_CODES_PROPOSED_NOT_ISSUED"]


def rows(name: str) -> list[dict[str, str]]:
    with open(ROOT / CELL / name, newline="") as fh:
        return list(csv.DictReader(fh))


def ordinates() -> dict[str, list[list[float]]]:
    pts: dict[str, list[list[float]]] = {}
    for r in rows(f"CURVE_ORDINATES_{TAG}.csv"):
        pts.setdefault(r["reference_building_id"], []).append([int(r["state_index"]), float(r["damage_ratio"])])
    return {k: sorted(v) for k, v in pts.items()}


def curve_ids() -> dict[str, str]:
    return {r["reference_building_id"]: r["curve_id"] for r in rows(f"CURVE_ORDINATES_{TAG}.csv")}


def curve_records(pts) -> list[dict]:
    ids = curve_ids()
    out = []
    for building, spec in BUILDINGS.items():
        p = pts[building]
        factor = "" if spec["factor"] == 1.0 else f" x {spec['factor']:.1f} (DINS same-fire building factor)"
        refs = ["WFRE-S001#Process_Step_5:shrub_FLP1-FLP6", "WFRE-S003#Entity_and_Attribute:FLP1-FLP6"]
        if spec["factor"] != 1.0:
            refs.append(f"WFRE-S002#DINS_BUILDING_COMPARISON:same_fire_ratio:{spec['dins_group']}")
        out.append({
            "curve_id": ids[building], "pathway_id": PW, "failure_unit_id": UNIT,
            "curve_form": "piecewise_linear", "x_axis": "fsim_conditional_flame_length_class_state_exact_integer_only",
            "y_axis": "failure_unit_damage_ratio", "parameters": {"points": p},
            "valid_range": [LO, HI],
            "interpolation_policy": "linear_between_source_knots",
            "extrapolation_policy": "exact integer states 0-6 only (USFS shrub response / 100" + factor
                                    + "; state 0 = 0); the evaluator does not interpolate; fractional or out-of-range states rejected (INVALID_CLASS_STATE)",
            "selector_match": {"reference_building_id": building, "source_wildfire_product_id": PRODUCT},
            "source_parameter_refs": refs,
            "metadata_flags": spec["flags"],
        })
    return out


def capability() -> dict:
    return {
        "schema_version": "capability_declaration.v3", "cell_id": CELL_ID,
        "canonical_runtime_artifact": False,
        "pathway_capabilities": [{
            "pathway_id": PW,
            "failure_unit_scalar_dr": "conditional",
            "scenario_loss_given_value_basis": "withheld",
            "curve_intrinsic_spread": "not_carried",
            "populated_emit_modes": ["scalar_mean"],
            "conditions": [
                "reference_building_id must be one of the three Hazard reference profiles r1 buildings",
                f"source_wildfire_product_id must be {PRODUCT} (the FSim class semantics the curve is bound to)",
                f"{AXIS} is the exact FSim conditional flame-length class state 0-6 (0 = no event); integers only, no interpolation",
                "burn probability is frequency and never a damage input",
                "the shrub response is used for every location (Hazard supplies no lifeform)",
                "scenario dollars stay withheld until the consumer qualifies the building value",
                "owner acceptance of the scope and selections is required before any canonical use",
            ],
            "limitation_flags": ALWAYS + ["VALUE_COVERAGE_NOT_ITEMIZED_BY_SOURCE",
                                          "MULTI_PERIL_SAME_BUILDING_COMBINATION_CONSUMER_OWNED"],
            "withheld_failure_units": [{"failure_unit_id": CONTENTS, "reason_codes": [
                "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"]}],
        }],
        "consumer_annual_metrics": {
            "computation_owner": "downstream_consumer",
            "status_before_promotion": "withheld_noncanonical_proposal",
            "status_after_promotion": "withheld",
            "prerequisites": ["owner acceptance of scope and curve selections",
                              "consumer-qualified replacement cost new for each reference building",
                              "Hazard fire frequency at building locations reviewed (NRI check: burnable-pixel burn probability)",
                              "exact model/docs/schema/SHA pin"],
            "limitation_flags": ["ANNUAL_AND_TAIL_METRICS_CONSUMER_OWNED", "VALUE_COVERAGE_NOT_ITEMIZED_BY_SOURCE",
                                 "BURNABLE_PIXEL_FREQUENCY_NOT_BUILDING_EXPOSURE"],
        },
        "cap_binding": {
            "policy": "consumer_enforced_fail_closed", "enforcement_owner": "downstream_consumer",
            "checks_required": ["exact model/docs/schema/SHA pin",
                                "record routing by reference_building_id and source_wildfire_product_id",
                                "exact integer class state; burn probability never passed to the damage call",
                                "all perils on one building in one event together at most 100% of structure value"],
            "action_if_fail": "withhold the affected DR or downstream metric; do not substitute another record or clamp",
        },
        "promotion_gate": {"status": "blocked", "required_before_canonical_use": [
            "owner accepts D-WFRE-01 to D-WFRE-14",
            "consumer value qualification of each reference budget (shared with the other real-estate cells)",
            "reviewer accepts the agency-response basis, the shrub default and the building factors",
            "independent review of the package"]},
    }


def axis() -> dict:
    return {"id": "FSIM_CONDITIONAL_FLAME_LENGTH_CLASS_STATE_SCREENING", "preferred_input_field": AXIS,
            "unit": "source_native_categorical_class", "valid_range": [LO, HI],
            "extrapolation_policy": "exact integers only; 0 is the no-event control; reject non-integer, non-numeric and out-of-range states",
            "source_product": PRODUCT, "native_class_map": NATIVE_CLASS_MAP,
            "permitted_proxy_fields": [],
            "bridge": "the USFS response was defined on WRC 30 m WildEST FLP1-6; applied to Hazard's 270 m FSim FLP1-6 (same class boundaries; flagged identity bridge)",
            "guardrail": "The class is the flame length of the wildland fire in the cell, not the heat flux, ember load or flame contact at the building; burn probability is frequency and never enters the damage call."}


def pathway_block(pts) -> dict:
    return {
        "pathway_id": PW,
        "hazard_scope": {
            "included": ["wildfire reaching the building location, with embers, radiant heat, direct flame contact and "
                         "building-to-building spread as they are inside the source response and the inspected outcomes"],
            "excluded": ["burn probability and fire frequency (Hazard)", "smoke, soot or ash contamination without fire damage",
                         "post-fire debris flow, flooding and erosion", "power shutoff, loss of use, business interruption",
                         "contents, land, landscaping, site works, vehicles"],
            "deferred_pathways": [],
            "compound_event_rule": "All perils on one building in one event together at most 100% of structure value (consumer)."},
        "hazard_axis": axis(),
        "reference_profile_binding": {b: s["profile"] for b, s in BUILDINGS.items()},
        "record_routing_fields": ["reference_building_id", "source_wildfire_product_id"],
        "selector_logic": [
            {"field": "reference_building_id", "required": True, "default": None, "allowed": list(BUILDINGS),
             "effect": "Fixed identity of the reference building; picks the building factor."},
            {"field": "source_wildfire_product_id", "required": True, "default": None, "allowed": [PRODUCT],
             "effect": "Pins the FSim flame-length class semantics the curve is bound to."}],
        "conditioner_logic": [],
        "building_factors": {b: {"factor_on_house_curve": s["factor"], "dins_comparison_group": s["dins_group"]}
                             for b, s in BUILDINGS.items()},
        "exposure_contract": {
            "required_subject_grain": "one reference building",
            "value_rule": "Scenario dollars need structure replacement cost new for the same building; the consumer qualifies the reference budget.",
            "spatial_rule": "Hazard couples the building to the FSim class mix and fire rate of its location; the curve does not add a hit probability.",
            "mitigation_rule": "No defensible-space, vegetation or ember-resistant construction credit in model v0.1.",
        },
        "failure_unit_coverage": [
            {"failure_unit_id": UNIT, "status": "conditional_numeric_screening_curve", "reason_codes": []},
            {"failure_unit_id": CONTENTS, "status": "withheld_not_zero",
             "reason_codes": ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"]},
        ],
        "curve_records": curve_records(pts),
    }


def artifact(pts) -> dict:
    return {
        "schema_version": "damage_curve_record_bundle.v3", "schema_status": "proposed_draft",
        "cell_id": CELL_ID, "damage_code_id": "WILDFIRE_REAL_ESTATE_WRC_FSIM_SCREENING_V0_1",
        "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1",
        "lifecycle_state": "scaffold", "promotion_status": "proposed", "review_status": "not_yet_reviewed",
        "model_grade": "screening_agency_response_function_with_inspection_building_factors",
        "package_release": "unreleased", "package_baseline": "library v2.5", "package_inclusion_status": "not_included",
        "canonical_runtime_artifact": False,
        "source_dossier": f"{CELL}/{CELL_ID}_curve_derivation_dossier__model_v0_1__docs_r1.md",
        "source_workbook": f"{CELL}/damage_curve_records_{TAG}.xlsx",
        "known_answer_tests": f"{CELL}/known_answer_tests_{TAG}.json",
        "source_register": f"{CELL}/SOURCE_REGISTER_{TAG}.csv",
        "claim_parameter_register": f"{CELL}/CLAIM_PARAMETER_REGISTER_{TAG}.csv",
        "value_crosswalk": f"{CELL}/VALUE_CROSSWALK_{TAG}.csv",
        "failure_units": [
            {"id": UNIT, "subsystem": "BUILDING", "component": "BUILDING_STRUCTURE_ASSEMBLY",
             "treatment": "primary_nonzero", "y_axis": "failure_unit_damage_ratio",
             "denominator": "structure replacement cost new of the same reference building (no land, contents, site works or depreciation)",
             "platform_code_status": "proposed_awaiting_platform_codes",
             "source_atom_note": "Whole-structure relative loss (USFS response) and whole-structure damage bands (DINS); not an aggregate of component records."},
            {"id": CONTENTS, "subsystem": "BUILDING", "component": "CONTENTS", "treatment": "withheld",
             "y_axis": "failure_unit_damage_ratio", "denominator": "contents value (deferred)",
             "withheld_reason_codes": ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"],
             "platform_code_status": "proposed_awaiting_platform_codes"},
        ],
        "pathways": [pathway_block(pts)],
        "value_linkage": {
            "curve_denominator": "structure replacement cost new of the reference building",
            "scenario_loss_formula": "loss = DR * structure_replacement_cost_new_usd",
            "scenario_loss_status": "withheld_consumer_value_qualification",
            "rejected_denominators": ["depreciated value", "market value", "assessed value"],
            "implicit_default_profile": None,
        },
        "parameter_tier_table": rows(f"PARAMETER_TIER_TABLE_{TAG}.csv"),
        "evaluation_contract": {
            "supported_pathway_ids": [PW], "supported_failure_unit_id": UNIT,
            "required_selector_fields": ["reference_building_id", "source_wildfire_product_id"],
            "required_conditioner_fields": [],
            "accepted_axis_payloads": [{"pathway_id": PW, "mode": "exact_fsim_class_state", "required_fields": [AXIS]}],
            "metadata_flags_always": ALWAYS,
            "out_of_range_behavior": "non-integer or outside 0-6: error INVALID_CLASS_STATE; no withheld band (closed class set)",
            "frequency_guard": "a burn probability field in the damage call is an error (FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL)",
            "reference_evaluator": "scripts/reference_helpers/wildfire_real_estate_curve_eval.py",
        },
        "emit_contract": {
            "schema_version": "damage_emit.v2",
            "populated_emit_modes_for_this_cell": ["scalar_mean"],
            "supported_output": "conditional scalar DR for WFRE_BUILDING_STRUCTURE given a fire at the building location in the stated class",
            "scenario_loss": "withheld until the consumer qualifies the building value",
            "annual_and_tail_metrics": "withheld; consumer-owned",
            "withheld_units_emit": "explicit null DR plus reason codes; never zero",
        },
        "capability_declaration": capability(),
        "derivation_rationale": {
            "source_spine": "USFS Wildfire Risk to Communities 2nd ed. (RDS-2020-0016-2) conditional risk to potential structures response function, shrub lifeform, per FSim flame-length class; CAL FIRE DINS 2013-2025 same-fire comparison for the warehouse and office factors.",
            "adopted_form": "exact class-state table: DR(0) = 0; DR(k) = factor x WRC_shrub(FLP_k) / 100; factor 1.0 house, 0.8 warehouse, 0.9 office",
            "why_not_flat": "A flat loss per building would discard Hazard's flame-length information; the owner chose the class-based response (D-WFRE-03).",
            "parameter_tier_mix": "House response T3 (agency judgment checked against DINS level); lifeform default, value reading, class identity and factor transfer T4; building factors T3 (adjacent empirical); axis T2.",
            "nri_check": "Yearly building loss 2.0x (house), 1.6x (warehouse), 1.8x (office) NRI nationally; median cell 2.4-3.0x; rank correlation 0.88; West 1.75x, East 4.7x (house, median cell).",
        },
        "legacy_comparison": {"prior_cell_state": "none (new cell)", "changes_from_prior": [],
                              "legacy_arrays_used": "none", "canonical_or_consumer_change": False},
    }


def known_answer_tests(pts) -> dict:
    ids = curve_ids()

    def req(building, state, **extra):
        return {"pathway_id": PW, "failure_unit_id": UNIT, "reference_building_id": building,
                "source_wildfire_product_id": PRODUCT, AXIS: state, **extra}

    formula, withheld, errors = [], [], []
    for building in BUILDINGS:
        p, cid = dict((int(x), y) for x, y in pts[building]), ids[building]
        for k in range(7):
            formula.append({"test_id": f"{cid}_STATE_{k}", "input": req(building, k),
                            "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": p[k]}})
        formula.append({"test_id": f"{cid}_STATE_3_AS_FLOAT", "input": req(building, 3.0),
                        "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": p[3],
                                     "metadata_flags_include": ["FSIM_CLASS_IS_NOT_LOCAL_HEAT_FLUX_OR_EMBER_EXPOSURE"]}})
        withheld.append({"test_id": f"{cid}_CONTENTS_WITHHELD", "input": {**req(building, 4), "failure_unit_id": CONTENTS},
                         "expected": {"status": "withheld", "reason_code": "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT"}})
    base = req("RE_RES_SFD_1S_SLAB", 4)
    drop = lambda k: {key: v for key, v in base.items() if key != k}  # noqa: E731
    for tid, inp, code in [
        ("PATHWAY_REQUIRED", drop("pathway_id"), "PATHWAY_ID_REQUIRED"),
        ("PATHWAY_UNKNOWN", {**base, "pathway_id": "wildfire_thermal_attack"}, "PATHWAY_ID_UNKNOWN"),
        ("BUILDING_REQUIRED", drop("reference_building_id"), "REFERENCE_BUILDING_ID_REQUIRED"),
        ("BUILDING_UNKNOWN", {**base, "reference_building_id": "RE_COM_LOWRISE"}, "REFERENCE_BUILDING_ID_UNKNOWN"),
        ("BUILDING_PROFILE_ID_NOT_A_SELECTOR", {**base, "reference_building_id": "re_house_1s_wood_slab"}, "REFERENCE_BUILDING_ID_UNKNOWN"),
        ("PRODUCT_REQUIRED", drop("source_wildfire_product_id"), "SOURCE_WILDFIRE_PRODUCT_ID_REQUIRED"),
        ("PRODUCT_UNSUPPORTED", {**base, "source_wildfire_product_id": "USFS_WRC_RDS_2020_0016_2_30M"}, "SOURCE_WILDFIRE_PRODUCT_ID_UNSUPPORTED"),
        ("AXIS_REQUIRED", drop(AXIS), "AXIS_PAYLOAD_REQUIRED"),
        ("FLAME_LENGTH_FEET_NOT_A_STATE", {**drop(AXIS), "conditional_flame_length_ft": 7.0}, "AXIS_PAYLOAD_REQUIRED"),
        ("CLASS_LABEL_NOT_A_STATE", {**base, AXIS: "gte_6_lt_8_ft"}, "INVALID_CLASS_STATE"),
        ("STATE_FRACTIONAL", {**base, AXIS: 2.5}, "INVALID_CLASS_STATE"),
        ("STATE_BOOLEAN", {**base, AXIS: True}, "INVALID_CLASS_STATE"),
        ("STATE_NEGATIVE", {**base, AXIS: -1}, "INVALID_CLASS_STATE"),
        ("STATE_ABOVE_SIX", {**base, AXIS: 7}, "INVALID_CLASS_STATE"),
        ("BURN_PROBABILITY_IN_DAMAGE_CALL", {**base, "burn_probability": 0.01}, "FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL"),
        ("UNIT_REQUIRED", drop("failure_unit_id"), "FAILURE_UNIT_ID_REQUIRED"),
        ("UNIT_UNKNOWN", {**base, "failure_unit_id": "WFRE_ROOF"}, "FAILURE_UNIT_ID_UNKNOWN"),
    ]:
        errors.append({"test_id": tid, "input": inp, "expected_error_code": code})
    return {
        "schema_version": "known_answer_tests.v3", "cell_id": CELL_ID,
        "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1",
        "artifact_schema_version": "damage_curve_record_bundle.v3", "artifact_status": "noncanonical_proposal",
        "absolute_tolerance": 1e-12,
        "equation": {"runtime": "exact lookup of the integer class state in the selected record; no interpolation",
                     "axis": "FSim conditional flame-length class state 0-6 (0 = no event)",
                     "ranges": "0 to 6 integers evaluate; anything else is an error"},
        "formula_known_answer_tests": formula, "withheld_tests": withheld, "error_tests": errors,
        "contract_assertions": [
            {"assertion_id": "WFRE_EXACT_STATE_ONLY", "expected": "a fractional or out-of-range state is an error, never interpolated or clamped"},
            {"assertion_id": "WFRE_NO_FREQUENCY_IN_DAMAGE", "expected": "burn probability in the damage call is an error"},
            {"assertion_id": "WFRE_NO_DOLLARS", "expected": "no scenario dollars until the consumer qualifies the building value"},
            {"assertion_id": "WFRE_CONTENTS_WITHHELD_NOT_ZERO", "expected": "contents are withheld, never reported as zero"},
        ],
    }


def workbook(art: dict, kats: dict, path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    for line in [
        [f"{CELL_ID} model v0.1 / docs r1 — noncanonical proposal (review workbook)"],
        ["Generated by scripts/reference_helpers/build_wildfire_real_estate_v0_1_package.py; do not edit by hand."],
        ["Damage ratio = fraction of structure replacement cost new; axis = exact FSim flame-length class state 0-6."],
        ["House = USFS shrub response; warehouse 0.8 x house; office 0.9 x house (CAL FIRE DINS same-fire ratios)."],
    ]:
        ws.append(line)
    ws["A1"].font = Font(bold=True)

    def sheet(title, header, data):
        s = wb.create_sheet(title)
        s.append(header)
        for c in s[1]:
            c.font = Font(bold=True)
        for row in data:
            s.append(row)

    recs = [r for p in art["pathways"] for r in p["curve_records"]]
    sheet("curve_records", ["curve_id", "pathway_id", "reference_building_id", "class_state", "damage_ratio"],
          [[r["curve_id"], r["pathway_id"], r["selector_match"]["reference_building_id"], x, y]
           for r in recs for x, y in r["parameters"]["points"]])
    sheet("reference_buildings", ["reference_building_id", "reference_profile", "factor_on_house_curve", "dins_group"],
          [[b, s["profile"], s["factor"], s["dins_group"]] for b, s in BUILDINGS.items()])
    for name, fname in [("wrc_response", f"WRC_RESPONSE_FUNCTION_TABLE_{TAG}.csv"),
                        ("building_factors", f"BUILDING_FACTOR_TABLE_{TAG}.csv"),
                        ("dins_comparison", f"DINS_BUILDING_COMPARISON_{TAG}.csv"),
                        ("sources", f"SOURCE_REGISTER_{TAG}.csv"), ("claims", f"CLAIM_PARAMETER_REGISTER_{TAG}.csv"),
                        ("parameter_tiers", f"PARAMETER_TIER_TABLE_{TAG}.csv"), ("value_crosswalk", f"VALUE_CROSSWALK_{TAG}.csv"),
                        ("sensitivity", f"SENSITIVITY_{TAG}.csv"), ("nri_check", f"NRI_CHECK_{TAG}.csv")]:
        data = rows(fname)
        sheet(name, list(data[0]), [list(r.values()) for r in data])
    sheet("known_answer_tests", ["test_id", "kind", "expected"],
          [[t["test_id"], k, json.dumps(t.get("expected", t.get("expected_error_code")))]
           for k in ("formula_known_answer_tests", "withheld_tests", "error_tests") for t in kats[k]])
    for s in wb.worksheets:
        s.column_dimensions["A"].width = 42
    wb.properties.creator = f"{CELL_ID} builder"
    fixed = datetime.datetime(2026, 10, 18)
    wb.properties.created = fixed
    wb.properties.modified = fixed
    wb.save(path)


def main() -> None:
    pts = ordinates()
    art = artifact(pts)
    kats = known_answer_tests(pts)
    out = ROOT / CELL
    (out / f"{TAG}__curve_artifact.json").write_text(json.dumps(art, indent=2) + "\n")
    (out / f"{TAG}__capability.json").write_text(json.dumps(art["capability_declaration"], indent=2) + "\n")
    (out / f"known_answer_tests_{TAG}.json").write_text(json.dumps(kats, indent=2) + "\n")
    workbook(art, kats, out / f"damage_curve_records_{TAG}.xlsx")
    n = sum(len(kats[k]) for k in ("formula_known_answer_tests", "withheld_tests", "error_tests"))
    nrec = sum(len(p["curve_records"]) for p in art["pathways"])
    print(f"wrote artifact ({nrec} curve records), capability, {n} known-answer tests, workbook")


if __name__ == "__main__":
    main()
