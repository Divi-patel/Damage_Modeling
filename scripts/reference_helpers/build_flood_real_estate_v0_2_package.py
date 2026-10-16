"""Deterministic builder for the noncanonical flood × real estate model-v0.2 / docs-r1 package.

Model v0.2 changes from v0.1 (decision log D-FRE-27, D-FRE-28):
    - house, warehouse and the new three-storey office use one Hazus record each for all still water
      (freshwater and coastal surge); their selector_match lists both water types;
    - new office selector RE_COM_OFFICE_3S_SLAB with Hazus DF 431;
    - the retail record RE_COM_LOWRISE is unchanged (Hazus DF 217 freshwater, NACCS prototype 2 coastal surge).

Reads the governed CURVE_ORDINATES_flood_real_estate__model_v0_2__docs_r1.csv and the shared cell registers in
docs/cells/flood_real_estate/proposed/ and writes:
    flood_real_estate__model_v0_2__docs_r1__curve_artifact.json   (bundle v3, embedded capability)
    flood_real_estate__model_v0_2__docs_r1__capability.json       (identical standalone capability)
    known_answer_tests_flood_real_estate__model_v0_2__docs_r1.json
    damage_curve_records_flood_real_estate__model_v0_2__docs_r1.xlsx

Known-answer expectations are computed here from the ordinates CSV with a separate, minimal interpolation, not
by calling the evaluator. Requires openpyxl for the workbook.

Usage (from the repository root):
    python scripts/reference_helpers/build_flood_real_estate_v0_2_package.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELL = "docs/cells/flood_real_estate/proposed"
TAG = "flood_real_estate__model_v0_2__docs_r1"
REG = "flood_real_estate__model_v0_1__docs_r1"  # shared cell registers keep their docs-r1 names
P = "flood_inundation_contact"
UNIT = "FRE_BUILDING_STRUCTURE"
CONTENTS = "FRE_BUILDING_CONTENTS"
FRESH, COAST, UNKNOWN = "freshwater_riverine_or_pluvial", "coastal_surge_saline", "unknown"
ANY = "freshwater_or_coastal_surge"  # ordinates-CSV marker: one record for all still water
EXPECTED_RECORDS = 7
# reference building -> (first-floor height ft, [(curve_id, water type or ANY, bands)])
BUILDINGS = {
    "RE_RES_SFD_1S_SLAB": (0.75, [("FRE_RES_HAZUS_DF129", ANY, ["point"])]),
    "RE_COM_LOWRISE": (0.25, [("FRE_COM_FRESH_HAZUS_DF217", FRESH, ["point"]),
                              ("FRE_COM_COAST_NACCS_P2", COAST, ["point", "lower_bound", "upper_bound"])]),
    "RE_IND_WAREHOUSE": (0.25, [("FRE_IND_HAZUS_DF341", ANY, ["point"])]),
    "RE_COM_OFFICE_3S_SLAB": (0.25, [("FRE_OFF_HAZUS_DF431", ANY, ["point"])]),
}
PROFILES = {"RE_RES_SFD_1S_SLAB": "re_house_1s_wood_slab", "RE_IND_WAREHOUSE": "re_warehouse_1s_steel_slab",
            "RE_COM_OFFICE_3S_SLAB": "re_office_3s_slab", "RE_COM_LOWRISE": None}
SOURCE_REFS = {
    "FRE_RES_HAZUS_DF129": ["FRE-S002#Table_5-2", "FRE-S003#DF129", "FRE-S010#DF129", "FRE-S012#coastal_comparison"],
    "FRE_COM_FRESH_HAZUS_DF217": ["FRE-S002#Table_5-2", "FRE-S003#DF217", "FRE-S010#DF217"],
    "FRE_COM_COAST_NACCS_P2": ["FRE-S004#Table_25"],
    "FRE_IND_HAZUS_DF341": ["FRE-S002#Table_5-2", "FRE-S003#DF341", "FRE-S010#DF341", "FRE-S010#flBldgStructDmgFinal"],
    "FRE_OFF_HAZUS_DF431": ["FRE-S002#Table_5-2", "FRE-S003#DF431", "FRE-S005#COM4", "FRE-S010#DF431",
                            "FRE-S010#flBldgStructDmgFinal", "FRE-S012#by_storeys"],
}
EXTRA_FLAGS = {
    "FRE_RES_HAZUS_DF129": ["COASTAL_STILL_WATER_USES_HAZUS_RIVERINE_CURVE"],
    "FRE_COM_FRESH_HAZUS_DF217": ["SINGLE_USACE_DISTRICT_GALVESTON"],
    "FRE_COM_COAST_NACCS_P2": [],
    "FRE_IND_HAZUS_DF341": ["SINGLE_USACE_DISTRICT_GALVESTON", "COASTAL_STILL_WATER_USES_HAZUS_RIVERINE_CURVE"],
    "FRE_OFF_HAZUS_DF431": ["SINGLE_USACE_DISTRICT_GALVESTON", "COASTAL_STILL_WATER_USES_HAZUS_RIVERINE_CURVE",
                            "HAZUS_COMMERCIAL_CURVE_NOT_HEIGHT_SPECIFIC"],
}
ALWAYS = ["NONCANONICAL_PROPOSAL", "SCREENING_SOURCE_NATIVE_ADOPTED_TABLE", "WHOLE_BUILDING_SOURCE_ATOM",
          "REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED", "NOT_FIELD_OR_CLAIMS_CALIBRATED",
          "PLATFORM_CODES_PROPOSED_NOT_ISSUED"]
SUFFIX = {"point": "", "lower_bound": "_MIN", "upper_bound": "_MAX"}


def rows(name: str) -> list[dict[str, str]]:
    with open(ROOT / CELL / name, newline="") as fh:
        return list(csv.DictReader(fh))


def ordinates() -> dict[tuple[str, str], list[list[float]]]:
    pts: dict[tuple[str, str], list[list[float]]] = {}
    for r in rows(f"CURVE_ORDINATES_{TAG}.csv"):
        pts.setdefault((r["curve_id"], r["band"]), []).append(
            [float(r["depth_above_first_floor_ft"]), int(r["damage_pct_structure_replacement_cost"]) / 100])
    return {k: sorted(v) for k, v in pts.items()}


def interp(points: list[list[float]], x: float) -> float:
    xs = [p[0] for p in points]
    if x <= xs[0]:
        return points[0][1] if x == xs[0] else 0.0
    i = max(j for j, xv in enumerate(xs) if xv <= x)
    if xs[i] == x:
        return points[i][1]
    (x0, y0), (x1, y1) = points[i], points[i + 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def curve_records(pts) -> list[dict]:
    out = []
    for building, (_, records) in BUILDINGS.items():
        for cid, water, bands in records:
            for band in bands:
                p = pts[(cid, band)]
                lib = "NACCS" if "NACCS" in cid else "HAZUS"
                match = {"reference_building_id": building,
                         "flood_water_type": [FRESH, COAST] if water == ANY else water, "band": band}
                out.append({
                    "curve_id": cid + SUFFIX[band], "pathway_id": P, "failure_unit_id": UNIT,
                    "curve_form": "piecewise_linear", "x_axis": "flood_depth_above_first_floor_ft",
                    "y_axis": "failure_unit_damage_ratio", "parameters": {"points": p},
                    "valid_range": [p[0][0], p[-1][0]],
                    "interpolation_policy": "linear_between_source_knots",
                    "extrapolation_policy": f"below {p[0][0]:g} ft returns 0 (published zero region); above {p[-1][0]:g} ft withholds; no clamp",
                    "selector_match": match,
                    "source_parameter_refs": SOURCE_REFS[cid],
                    "metadata_flags": [f"{lib}_SOURCE_TABLE"] + (
                        ["NACCS_NORTH_ATLANTIC_TRANSFER_LIMIT"] if lib == "NACCS" else ["HAZUS_CLASS_AVERAGE_OR_GENERIC_DEFAULT"])
                        + EXTRA_FLAGS[cid] + (["BUILDING_VARIANT_BOUND_NOT_PROBABILITY"] if band != "point" else []),
                })
    return out


def capability() -> dict:
    return {
        "schema_version": "capability_declaration.v3", "cell_id": "flood_real_estate",
        "canonical_runtime_artifact": False,
        "pathway_capabilities": [{
            "pathway_id": P,
            "failure_unit_scalar_dr": "conditional",
            "scenario_loss_given_value_basis": "withheld",
            "curve_intrinsic_spread": "nonprobabilistic_epistemic_envelope",
            "populated_emit_modes": ["scalar_mean", "scalar_mean_plus_bounds"],
            "conditions": [
                "reference_building_id must be one of the four proposed reference buildings",
                "flood_water_type must be freshwater_riverine_or_pluvial or coastal_surge_saline; unknown withholds",
                "house, warehouse and office use one Hazus record for both water types; the retail record routes by water type",
                "depth is referenced to the first finished floor; depth above grade of 0 or less is not inundated and returns 0",
                "Hazus records are valid from -4 to 24 ft and the retail coastal record from -1 to 10 ft above the floor; above withholds",
                "bounds are emitted for the retail coastal record only and are NACCS building-variant bounds, not a probability spread",
                "scenario dollars stay withheld until the consumer qualifies a replacement cost new for the building",
                "owner acceptance of the scope and selections is required before any canonical use",
            ],
            "limitation_flags": ALWAYS + ["COASTAL_STILL_WATER_USES_HAZUS_RIVERINE_CURVE_FOR_TARGET_BUILDINGS",
                                          "OFFICE_HEIGHT_BIAS_RECORDED_NOT_CORRECTED",
                                          "WAVE_VELOCITY_PATHWAY_DEFERRED_WITHHELD_NOT_ZERO",
                                          "VALUE_COVERAGE_NOT_ITEMIZED_BY_SOURCE"],
            "withheld_failure_units": [{"failure_unit_id": CONTENTS, "reason_codes": [
                "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"]}],
        }],
        "consumer_annual_metrics": {
            "computation_owner": "downstream_consumer",
            "status_before_promotion": "withheld_noncanonical_proposal",
            "status_after_promotion": "withheld",
            "prerequisites": ["owner acceptance of scope and curve selections",
                              "consumer-qualified replacement cost new for each reference building",
                              "Hazard frequency-depth coupling supplying flood_water_type per event",
                              "exact model/docs/schema/SHA pin"],
            "limitation_flags": ["ANNUAL_AND_TAIL_METRICS_CONSUMER_OWNED", "VALUE_COVERAGE_NOT_ITEMIZED_BY_SOURCE"],
        },
        "cap_binding": {
            "policy": "consumer_enforced_fail_closed", "enforcement_owner": "downstream_consumer",
            "checks_required": ["exact model/docs/schema/SHA pin",
                                "record-level valid range enforced (the retail coastal record stops at 10 ft)",
                                "record routing by reference_building_id, plus flood_water_type for RE_COM_LOWRISE only",
                                "dry-ground rule applied when depth is sent relative to the floor",
                                "one building value charged once per event across pathways"],
            "action_if_fail": "withhold the affected DR or downstream metric; do not substitute another record or clamp",
        },
        "promotion_gate": {"status": "blocked", "required_before_canonical_use": [
            "the reviewer accepts scope D-FRE-01 to D-FRE-06 and selections D-FRE-16 to D-FRE-28",
            "consumer value qualification of each reference budget against the structure denominator",
            "consumer integration resolves record-level ranges, routing and the dry-ground rule",
            "independent review of the package"]},
    }


def artifact(pts) -> dict:
    tiers = rows(f"PARAMETER_TIER_TABLE_{REG}.csv")
    cap = capability()
    return {
        "schema_version": "damage_curve_record_bundle.v3", "schema_status": "proposed_draft",
        "cell_id": "flood_real_estate", "damage_code_id": "FLOOD_REAL_ESTATE_HAZUS_NACCS_SCREENING_V0_2",
        "semantic_damage_model_version": "model v0.2", "documentation_revision": "docs r1",
        "lifecycle_state": "scaffold", "promotion_status": "proposed", "review_status": "not_yet_reviewed",
        "model_grade": "screening_source_native_adopted_tables",
        "package_release": "unreleased", "package_baseline": "library v2.5", "package_inclusion_status": "not_included",
        "canonical_runtime_artifact": False,
        "source_dossier": f"{CELL}/flood_real_estate_curve_derivation_dossier__model_v0_2__docs_r1.md",
        "source_workbook": f"{CELL}/damage_curve_records_{TAG}.xlsx",
        "known_answer_tests": f"{CELL}/known_answer_tests_{TAG}.json",
        "source_register": f"{CELL}/SOURCE_REGISTER_{REG}.csv",
        "claim_parameter_register": f"{CELL}/CLAIM_PARAMETER_REGISTER_{REG}.csv",
        "value_crosswalk": f"{CELL}/VALUE_CROSSWALK_{REG}.csv",
        "failure_units": [
            {"id": UNIT, "subsystem": "BUILDING", "component": "BUILDING_STRUCTURE_ASSEMBLY",
             "treatment": "primary_nonzero", "y_axis": "failure_unit_damage_ratio",
             "denominator": "structure replacement cost new of the same reference building (no land, contents, site works or depreciation)",
             "platform_code_status": "proposed_awaiting_platform_codes",
             "source_atom_note": "Whole-building source-native depth-damage function; not an aggregate of component records."},
            {"id": CONTENTS, "subsystem": "BUILDING", "component": "CONTENTS", "treatment": "withheld",
             "y_axis": "failure_unit_damage_ratio", "denominator": "contents value (deferred)",
             "withheld_reason_codes": ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"],
             "platform_code_status": "proposed_awaiting_platform_codes"},
        ],
        "pathways": [{
            "pathway_id": P,
            "hazard_scope": {
                "included": ["still-water inundation of the building from riverine, pluvial or coastal-surge flooding"],
                "excluded": ["wave impact, high-velocity flow, scour and debris (deferred pathway flood_wave_velocity; withheld, not zero)",
                             "contents, business interruption, land, site works",
                             "mould and long-duration effects beyond what the source curves embed"],
                "deferred_pathways": ["flood_wave_velocity"],
                "compound_event_rule": "Charge one building value once per event across flood pathways and other perils.",
            },
            "hazard_axis": {
                "id": "FLOOD_DEPTH_ABOVE_FIRST_FINISHED_FLOOR_FT",
                "preferred_input_field": "flood_depth_above_first_floor_ft",
                "permitted_proxy_fields": ["flood_depth_above_grade_ft", "first_floor_height_ft"],
                "unit": "ft",
                "valid_range": [-4.0, 24.0],
                "extrapolation_policy": "record-level ranges govern: Hazus records -4 to 24 ft, retail coastal record -1 to 10 ft; below a record range returns 0; above withholds",
                "bridge": "flood_depth_above_first_floor_ft = flood_depth_above_grade_ft - first_floor_height_ft; depth above grade <= 0 is not inundated (DR 0); a consumer sending floor-relative depth applies the dry rule itself",
            },
            "reference_first_floor_height_ft": {b: v[0] for b, v in BUILDINGS.items()},
            "reference_profile_binding": {b: PROFILES[b] for b in BUILDINGS},
            "record_routing_fields": ["reference_building_id", "flood_water_type", "band"],
            "record_routing_note": "for house, warehouse and office selector_match.flood_water_type lists both water types (one record); only RE_COM_LOWRISE has a record per water type",
            "selector_logic": [{"field": "reference_building_id", "required": True, "default": None,
                                "allowed": list(BUILDINGS),
                                "effect": "Fixed identity of the reference building; picks the occupancy-specific record."}],
            "conditioner_logic": [{"field": "flood_water_type", "required": True,
                                   "allowed": [FRESH, COAST, UNKNOWN],
                                   "numeric_support_when": [FRESH, COAST],
                                   "withhold_otherwise": "FLOOD_WATER_TYPE_UNKNOWN",
                                   "effect": "Event-time state. House, warehouse and office: same Hazus record for both types. Retail: Hazus (freshwater) or NACCS (coastal surge), never blended."}],
            "exposure_contract": {
                "required_subject_grain": "one reference building",
                "value_rule": "Scenario dollars need structure replacement cost new for the same building; the consumer qualifies the reference budget.",
                "protection_rule": "Flood protection must already be reflected in the delivered depth; no curve-side credit.",
            },
            "failure_unit_coverage": [
                {"failure_unit_id": UNIT, "status": "conditional_numeric_screening_curve", "reason_codes": []},
                {"failure_unit_id": CONTENTS, "status": "withheld_not_zero",
                 "reason_codes": ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"]},
            ],
            "curve_records": curve_records(pts),
        }],
        "value_linkage": {
            "curve_denominator": "structure replacement cost new of the reference building",
            "scenario_loss_formula": "loss = DR * structure_replacement_cost_new_usd",
            "scenario_loss_status": "withheld_consumer_value_qualification",
            "rejected_denominators": ["NSI val_struct (depreciated)", "market value", "assessed value"],
            "implicit_default_profile": None,
        },
        "parameter_tier_table": tiers,
        "evaluation_contract": {
            "supported_pathway_id": P, "supported_failure_unit_id": UNIT,
            "required_selector_fields": ["reference_building_id"],
            "required_conditioner_fields": ["flood_water_type"],
            "accepted_axis_payloads": [
                {"mode": "depth_above_grade_ft", "required_fields": ["flood_depth_above_grade_ft"],
                 "optional_fields": ["first_floor_height_ft"]},
                {"mode": "depth_above_first_floor_ft", "required_fields": ["flood_depth_above_first_floor_ft"]},
            ],
            "metadata_flags_always": ALWAYS,
            "out_of_range_behavior": "above a record's highest published depth: withhold; below its lowest: 0",
            "reference_evaluator": "scripts/reference_helpers/flood_real_estate_curve_eval.py",
        },
        "emit_contract": {
            "schema_version": "damage_emit.v2",
            "populated_emit_modes_for_this_cell": ["scalar_mean", "scalar_mean_plus_bounds"],
            "supported_output": "conditional scalar DR for FRE_BUILDING_STRUCTURE; the retail coastal record adds NACCS Min/Max building-variant bounds",
            "scenario_loss": "withheld until the consumer qualifies the building value",
            "annual_and_tail_metrics": "withheld; consumer-owned",
            "withheld_units_emit": "explicit null DR plus reason codes; never zero",
        },
        "capability_declaration": cap,
        "derivation_rationale": {
            "source_spine": "FEMA Hazus 7.0 Table 5-2 structure defaults (house RES1, warehouse COM2, office COM4, retail COM1) for still water; USACE NACCS 2015 prototype 2 for retail coastal surge only. Verified against originals and independent copies; compared with NFIP claims (FRE-S012).",
            "adopted_form": "exact published tables, straight lines between published points",
            "why_one_curve_for_both_waters": "NFIP coastal-surge claims are closer to the Hazus curves than to NACCS for the house and multi-floor business buildings (FRE-C027, C029, C035); FEMA assigns DF 341 and DF 431 to coastal zones (FRE-C033); D-FRE-28.",
            "why_not_smooth_fits": "Smooth fits (incl. anchored logistic) predicted held-out points worse on all point curves and moved published values by 2-6 points.",
            "parameter_tier_mix": "Ordinates T2 with stated transfer limits; first-floor heights T2 (house) and T3 (commercial, warehouse, office); value coverage not itemized by the sources.",
        },
        "legacy_comparison": {"prior_cell_state": "model v0.1 proposal (artifact sha256 106e3b53c8ac84f3dba7c233a261e32a8663012794d90c898e6ccab9dbd128e1), kept for reproducibility",
                              "changes_from_prior": ["house and warehouse coastal surge: NACCS 5A and prototype 3 replaced by their Hazus records (D-FRE-28)",
                                                     "new office record DF 431 (D-FRE-27, D-FRE-28)",
                                                     "retail record unchanged"],
                              "legacy_arrays_used": "none (Real Estate_Hail rejected, D-FRE-11)",
                              "canonical_or_consumer_change": False},
    }


def known_answer_tests(pts) -> dict:
    def req(building, water, **axis):
        return {"pathway_id": P, "failure_unit_id": UNIT, "reference_building_id": building,
                "flood_water_type": water, **axis}

    formula, withheld, errors = [], [], []
    for building, (ffh, records) in BUILDINGS.items():
        for cid, water, bands in records:
            p = pts[(cid, "point")]
            waters = [FRESH, COAST] if water == ANY else [water]
            for x, y in p:  # every published point (first water type)
                formula.append({"test_id": f"{cid}_KNOT_{x:+g}FT", "input": req(building, waters[0], flood_depth_above_first_floor_ft=x),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": y}})
            for w in waters:
                tag = "" if len(waters) == 1 else ("_FRESH" if w == FRESH else "_COAST")
                mid = (p[2][0] + p[3][0]) / 2
                formula.append({"test_id": f"{cid}{tag}_BETWEEN_{mid:+g}FT", "input": req(building, w, flood_depth_above_first_floor_ft=mid),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": interp(p, mid)}})
                g = 2.0
                formula.append({"test_id": f"{cid}{tag}_BRIDGE_2FT_ABOVE_GRADE", "input": req(building, w, flood_depth_above_grade_ft=g),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": interp(p, g - ffh),
                                             "metadata_flags_include": ["REFERENCE_FIRST_FLOOR_HEIGHT_DEFAULT_USED"]}})
                formula.append({"test_id": f"{cid}{tag}_NOT_INUNDATED", "input": req(building, w, flood_depth_above_grade_ft=0),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": 0.0,
                                             "metadata_flags_include": ["NOT_INUNDATED_ABOVE_GRADE"]}})
                hi = p[-1][0]
                withheld.append({"test_id": f"{cid}{tag}_ABOVE_RANGE", "input": req(building, w, flood_depth_above_first_floor_ft=hi + 0.0001),
                                 "expected": {"status": "withheld", "reason_code": "ABOVE_SOURCE_VALID_RANGE"}})
                formula.append({"test_id": f"{cid}{tag}_BELOW_RANGE_ZERO", "input": req(building, w, flood_depth_above_first_floor_ft=p[0][0] - 0.5),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": 0.0,
                                             "metadata_flags_include": ["BELOW_SOURCE_RANGE_ZERO"]}})
            if "lower_bound" in bands:
                lo_p, hi_p = pts[(cid, "lower_bound")], pts[(cid, "upper_bound")]
                formula.append({"test_id": f"{cid}_BOUNDS_4FT", "input": req(building, water, flood_depth_above_first_floor_ft=4.0),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": interp(p, 4.0),
                                             "scenario_drs": {"naccs_min_building_variant": interp(lo_p, 4.0), "naccs_max_building_variant": interp(hi_p, 4.0)}}})
        withheld.append({"test_id": f"{building}_UNKNOWN_WATER_WITHHELD", "input": req(building, UNKNOWN, flood_depth_above_first_floor_ft=2.0),
                         "expected": {"status": "withheld", "reason_code": "FLOOD_WATER_TYPE_UNKNOWN"}})
    formula.append({"test_id": "FFH_OVERRIDE_HOUSE_FRESH", "input": req("RE_RES_SFD_1S_SLAB", FRESH, flood_depth_above_grade_ft=3.0, first_floor_height_ft=1.0),
                    "expected": {"status": "conditional", "curve_id": "FRE_RES_HAZUS_DF129",
                                 "failure_unit_damage_ratio": interp(pts[("FRE_RES_HAZUS_DF129", "point")], 2.0)}})
    withheld.append({"test_id": "CONTENTS_WITHHELD", "input": {**req("RE_RES_SFD_1S_SLAB", FRESH, flood_depth_above_first_floor_ft=2.0), "failure_unit_id": CONTENTS},
                     "expected": {"status": "withheld", "reason_code": "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT"}})
    base = req("RE_RES_SFD_1S_SLAB", FRESH, flood_depth_above_first_floor_ft=2.0)
    for tid, inp, code in [
        ("PATHWAY_REQUIRED", {k: v for k, v in base.items() if k != "pathway_id"}, "PATHWAY_ID_REQUIRED"),
        ("WAVE_PATHWAY_NOT_IN_ARTIFACT", {**base, "pathway_id": "flood_wave_velocity"}, "PATHWAY_ID_UNKNOWN"),
        ("BUILDING_REQUIRED", {k: v for k, v in base.items() if k != "reference_building_id"}, "REFERENCE_BUILDING_ID_REQUIRED"),
        ("BUILDING_UNKNOWN", {**base, "reference_building_id": "RE_HOSPITAL"}, "REFERENCE_BUILDING_ID_UNKNOWN"),
        ("BUILDING_PROFILE_ID_NOT_A_SELECTOR", {**base, "reference_building_id": "re_office_3s_slab"}, "REFERENCE_BUILDING_ID_UNKNOWN"),
        ("WATER_TYPE_REQUIRED", {k: v for k, v in base.items() if k != "flood_water_type"}, "FLOOD_WATER_TYPE_REQUIRED"),
        ("WATER_TYPE_BAD_VALUE", {**base, "flood_water_type": "saltwater"}, "FLOOD_WATER_TYPE_UNKNOWN_VALUE"),
        ("AXIS_REQUIRED", {k: v for k, v in base.items() if k != "flood_depth_above_first_floor_ft"}, "AXIS_PAYLOAD_REQUIRED"),
        ("AXIS_AMBIGUOUS", {**base, "flood_depth_above_grade_ft": 2.0}, "AXIS_PAYLOAD_AMBIGUOUS"),
        ("AXIS_NOT_NUMBER", {**base, "flood_depth_above_first_floor_ft": "2"}, "AXIS_VALUE_INVALID"),
        ("NEGATIVE_DEPTH_ABOVE_GRADE", {**{k: v for k, v in base.items() if k != "flood_depth_above_first_floor_ft"}, "flood_depth_above_grade_ft": -0.5}, "NEGATIVE_DEPTH_ABOVE_GRADE"),
        ("UNIT_UNKNOWN", {**base, "failure_unit_id": "FRE_ROOF"}, "FAILURE_UNIT_ID_UNKNOWN"),
    ]:
        errors.append({"test_id": tid, "input": inp, "expected_error_code": code})
    return {
        "schema_version": "known_answer_tests.v3", "cell_id": "flood_real_estate",
        "semantic_damage_model_version": "model v0.2", "documentation_revision": "docs r1",
        "artifact_schema_version": "damage_curve_record_bundle.v3", "artifact_status": "noncanonical_proposal",
        "absolute_tolerance": 1e-12,
        "equation": {"runtime": "straight lines between published points of the selected record",
                     "bridge": "depth above floor = depth above grade - first-floor height; depth above grade <= 0 returns 0",
                     "ranges": "Hazus records -4..24 ft, retail coastal -1..10 ft above the floor; below returns 0; above withholds"},
        "formula_known_answer_tests": formula, "withheld_tests": withheld, "error_tests": errors,
        "contract_assertions": [
            {"assertion_id": "FRE_LIBRARIES_NEVER_BLENDED", "expected": "the retail freshwater and coastal records are never averaged or substituted"},
            {"assertion_id": "FRE_SAME_RECORD_BOTH_WATERS", "expected": "house, warehouse and office return the same record and value for freshwater and coastal surge at the same depth"},
            {"assertion_id": "FRE_BOUNDS_NOT_PROBABILITY", "expected": "NACCS Min/Max bounds are building-variant bounds, not a spread for PML/VaR"},
            {"assertion_id": "FRE_NO_DOLLARS", "expected": "no scenario dollars until the consumer qualifies the building value"},
            {"assertion_id": "FRE_WAVES_WITHHELD_NOT_ZERO", "expected": "wave and velocity damage is withheld, never reported as zero"},
        ],
    }


def workbook(art: dict, kats: dict, path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    for line in [
        ["flood_real_estate model v0.2 / docs r1 — noncanonical proposal (review workbook)"],
        ["Generated by scripts/reference_helpers/build_flood_real_estate_v0_2_package.py; do not edit by hand."],
        ["Damage ratio = fraction of structure replacement cost new; depth in ft above the first finished floor."],
        ["Straight lines between published points; Hazus -4..24 ft, retail coastal -1..10 ft; above withholds."],
        ["House, warehouse and office: one Hazus record for freshwater and coastal surge (D-FRE-28)."],
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

    recs = art["pathways"][0]["curve_records"]
    sheet("curve_records", ["curve_id", "reference_building_id", "flood_water_types", "band", "depth_above_floor_ft", "damage_ratio"],
          [[r["curve_id"], r["selector_match"]["reference_building_id"],
            "; ".join(r["selector_match"]["flood_water_type"]) if isinstance(r["selector_match"]["flood_water_type"], list)
            else r["selector_match"]["flood_water_type"],
            r["selector_match"]["band"], x, y] for r in recs for x, y in r["parameters"]["points"]])
    sheet("reference_buildings", ["reference_building_id", "reference_profile", "first_floor_height_ft", "records"],
          [[b, PROFILES[b] or "(none: retail kept, unbound)", v[0], "; ".join(c for c, _, _ in v[1])] for b, v in BUILDINGS.items()])
    for name, fname in [("sources", f"SOURCE_REGISTER_{REG}.csv"), ("claims", f"CLAIM_PARAMETER_REGISTER_{REG}.csv"),
                        ("parameter_tiers", f"PARAMETER_TIER_TABLE_{REG}.csv"), ("value_crosswalk", f"VALUE_CROSSWALK_{REG}.csv")]:
        data = rows(fname)
        sheet(name, list(data[0]), [list(r.values()) for r in data])
    sheet("known_answer_tests", ["test_id", "kind", "expected"],
          [[t["test_id"], k, json.dumps(t.get("expected", t.get("expected_error_code")))]
           for k in ("formula_known_answer_tests", "withheld_tests", "error_tests") for t in kats[k]])
    for s in wb.worksheets:
        s.column_dimensions["A"].width = 42
    wb.properties.creator = "flood_real_estate builder"
    import datetime
    fixed = datetime.datetime(2026, 10, 16)
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
    print(f"wrote artifact ({len(art['pathways'][0]['curve_records'])} curve records), capability, {n} known-answer tests, workbook")


if __name__ == "__main__":
    main()
