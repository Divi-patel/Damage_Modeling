"""Deterministic builder for the noncanonical tropical-cyclone wind × real estate model-v0.1 / docs-r1 package.

Reads the governed CSVs in docs/cells/tropical_cyclone_wind_real_estate/proposed/ and writes:
    tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json   (bundle v3, embedded capability)
    tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__capability.json       (identical standalone capability)
    known_answer_tests_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.json
    damage_curve_records_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.xlsx

Known-answer expectations are computed here from the ordinates CSV with a separate, minimal
interpolation, not by calling the evaluator. Requires openpyxl for the workbook.

Usage (from the repository root):
    python scripts/reference_helpers/build_tropical_cyclone_wind_real_estate_v0_1_package.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "tropical_cyclone_wind_real_estate"
CELL = f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
P = "tropical_cyclone_wind"
UNIT = "TCRE_BUILDING_STRUCTURE"
CONTENTS = "TCRE_BUILDING_CONTENTS"
AXIS = "tc_peak_gust_3s_10m_mph"
TERRAINS = ["open", "light_suburban", "suburban", "light_trees", "trees"]
LO, HI = 50.0, 250.0
SHUTTERS = {"allowed": ["no", "yes"], "reference": "no"}
METAL_DECK = {"allowed": ["standard", "superior"], "reference": "standard"}
# reference building -> Hazus type, wbID, characteristic contract (allowed values; reference = most common, D-TCRE-07)
BUILDINGS = {
    "RE_RES_SFD_1S_SLAB": {
        "stem": "TCRE_RES_HAZUS_WSF1", "sbt": "WSF1", "wbid": 6, "case": "ContinentalUS (CaseID 1)",
        "simcenter_id": "W.SF.1.gab.0.6d.tnail.no.0",
        "characteristics": {
            "hazus_roof_shape": {"allowed": ["gable", "hip"], "reference": "gable"},
            "hazus_secondary_water_resistance": {"allowed": ["no", "yes"], "reference": "no"},
            "hazus_roof_deck_attachment": {"allowed": ["6d_6_12", "8d_6_12", "6d8d_mix_6_6", "8d_6_6"], "reference": "6d_6_12"},
            "hazus_roof_to_wall_connection": {"allowed": ["toe_nail", "strap"], "reference": "toe_nail"},
            "hazus_garage_door": {"allowed": ["none", "weak", "standard", "sfbc_1994"], "reference": "none"},
            "hazus_shutters": SHUTTERS,
            "hazus_roof_cover": {"allowed": ["shingle"], "reference": "shingle"},
        },
        "flags": ["TREE_FALL_ADDITIVE_TERM_DEFERRED"],
    },
    "RE_COM_LOWRISE": {
        "stem": "TCRE_COM_HAZUS_SECBL", "sbt": "SECBL", "wbid": 1812, "case": "ContUS+Hawaii (CaseID 3)",
        "simcenter_id": "S.ECB.L.bur.0.B.std.low",
        "characteristics": {
            "hazus_roof_cover": {"allowed": ["bur", "spm"], "reference": "bur"},
            "hazus_window_area": {"allowed": ["low", "medium", "high"], "reference": "low"},
            "hazus_shutters": SHUTTERS,
            "hazus_windborne_debris_environment": {
                "allowed": ["residential_commercial", "varies_by_direction", "residential", "none"],
                "reference": "varies_by_direction"},
            "hazus_metal_deck_attachment": METAL_DECK,
        },
        "flags": ["SECBL_EQUALS_MECBL_IN_SOURCE", "HAZUS_COMMERCIAL_TERRAIN_ORDER_NOT_MONOTONE"],
    },
    "RE_IND_WAREHOUSE": {
        "stem": "TCRE_IND_HAZUS_SPMBL", "sbt": "SPMBL", "wbid": 1729, "case": "ContUS+Hawaii (CaseID 3)",
        "simcenter_id": "S.PMB.L.0.por.std",
        "characteristics": {
            "hazus_roof_deck_age": {"allowed": ["old", "new_or_average"], "reference": "old"},
            "hazus_shutters": SHUTTERS,
            "hazus_metal_deck_attachment": METAL_DECK,
        },
        "flags": ["WAREHOUSE_FLOOR_AREA_ABOVE_50000_FT2_ASSUMED", "HAZUS_SPMB_FAMILY_ANOMALY_NOT_IN_SELECTED_ROW"],
    },
}
SIMCENTER_TERRAIN = {"open": "3", "light_suburban": "15", "suburban": "35", "light_trees": "70", "trees": "100"}
ALWAYS = ["NONCANONICAL_PROPOSAL", "SCREENING_SOURCE_NATIVE_ADOPTED_TABLE", "WHOLE_BUILDING_SOURCE_ATOM",
          "HAZUS_COMBINED_PRESSURE_DEBRIS_RAIN_INGRESS", "REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED",
          "NOT_FIELD_OR_CLAIMS_CALIBRATED", "PLATFORM_CODES_PROPOSED_NOT_ISSUED"]
DIP_LIMIT = 0.005


def rows(name: str) -> list[dict[str, str]]:
    with open(ROOT / CELL / name, newline="") as fh:
        return list(csv.DictReader(fh))


def ordinates() -> dict[tuple[str, str], list[list[float]]]:
    pts: dict[tuple[str, str], list[list[float]]] = {}
    for r in rows(f"CURVE_ORDINATES_{TAG}.csv"):
        pts.setdefault((r["reference_building_id"], r["hazus_terrain_class"]), []).append(
            [float(r["peak_gust_3s_10m_open_terrain_mph"]), float(r["building_loss_ratio"])])
    return {k: sorted(v) for k, v in pts.items()}


def interp(points: list[list[float]], x: float) -> float:
    if x < points[0][0]:
        return 0.0
    i = max(j for j, p in enumerate(points) if p[0] <= x)
    if points[i][0] == x:
        return points[i][1]
    (x0, y0), (x1, y1) = points[i], points[i + 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def has_dips(points: list[list[float]]) -> bool:
    return any(b[1] < a[1] for a, b in zip(points, points[1:]))


def curve_id(building: str, terrain: str) -> str:
    return f"{BUILDINGS[building]['stem']}_{terrain.upper()}"


def curve_records(pts) -> list[dict]:
    out = []
    for building, spec in BUILDINGS.items():
        for terrain in TERRAINS:
            p = pts[(building, terrain)]
            out.append({
                "curve_id": curve_id(building, terrain), "pathway_id": P, "failure_unit_id": UNIT,
                "curve_form": "piecewise_linear", "x_axis": AXIS,
                "y_axis": "failure_unit_damage_ratio", "parameters": {"points": p},
                "valid_range": [p[0][0], p[-1][0]],
                "interpolation_policy": "linear_between_source_knots",
                "extrapolation_policy": "0 <= gust < 50 mph returns 0 (the source is 0 at 50 mph); above 250 mph withholds; no clamp",
                "selector_match": {"reference_building_id": building, "hazus_terrain_class": terrain},
                "source_parameter_refs": [
                    "TCRE-S001#Section_2.1",
                    f"TCRE-S002#huDamLossFun:wbID={spec['wbid']};TERRAINID={TERRAINS.index(terrain) + 1};DamLossDescID=5",
                    f"TCRE-S003#loss_repair:{spec['simcenter_id']}.{SIMCENTER_TERRAIN[terrain]}"],
                "metadata_flags": ["HAZUS_HURRICANE_BUILDING_LOSS_TABLE", "HAZUS_6_1_EXTRACT_VERIFIED_AGAINST_5_1_COPY",
                                   "MOST_COMMON_WIND_CHARACTERISTICS_ASSUMED"] + spec["flags"] + (
                                      ["HAZUS_SIMULATION_NOISE_SMALL_DIPS"] if has_dips(p) else []),
            })
    return out


def characteristic_selectors() -> list[dict]:
    """Optional selectors that admit only the published (reference) values, so a generic loader that ignores
    wind_characteristic_contract still refuses a non-reference value instead of pricing it as the reference."""
    fields: dict[str, list[str]] = {}
    for spec in BUILDINGS.values():
        for f, c in spec["characteristics"].items():
            fields.setdefault(f, [])
            if c["reference"] not in fields[f]:
                fields[f].append(c["reference"])
    return [{"field": f, "required": False, "allowed": vals,
             "effect": "Optional wind building characteristic; v0.1 publishes only the reference value. Building-specific "
                       "values are in wind_characteristic_contract; another valid value withholds "
                       "(WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED) in the reference evaluator."}
            for f, vals in sorted(fields.items())]


def capability() -> dict:
    return {
        "schema_version": "capability_declaration.v3", "cell_id": CELL_ID,
        "canonical_runtime_artifact": False,
        "pathway_capabilities": [{
            "pathway_id": P,
            "failure_unit_scalar_dr": "conditional",
            "scenario_loss_given_value_basis": "withheld",
            "curve_intrinsic_spread": "not_carried",
            "populated_emit_modes": ["scalar_mean"],
            "conditions": [
                "reference_building_id must be one of the three proposed reference buildings",
                "hazus_terrain_class is required (open, light_suburban, suburban, light_trees, trees); no default, no interpolation",
                "tc_peak_gust_3s_10m_mph is the open-terrain 3-second gust at 10 m; terrain is applied only by the record choice",
                "records are valid from 50 to 250 mph; below 50 returns 0, above 250 withholds",
                "only the most-common wind building characteristics are published; other values withhold",
                "the damage ratio includes wind pressure, windborne debris and rain entering through wind damage; no separate debris or rain pathway may be added",
                "scenario dollars stay withheld until a per-area replacement cost new is selected",
                "owner acceptance of the scope and selections is required before any canonical use",
            ],
            "limitation_flags": ALWAYS + ["TREE_FALL_ADDITIVE_TERM_DEFERRED", "VALUE_PER_AREA_NOT_SELECTED",
                                          "TERRAIN_CLASS_MAPPING_CONSUMER_OWNED",
                                          "WIND_AND_FLOOD_SAME_BUILDING_COMBINATION_CONSUMER_OWNED"],
            "withheld_failure_units": [{"failure_unit_id": CONTENTS, "reason_codes": [
                "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"]}],
        }],
        "consumer_annual_metrics": {
            "computation_owner": "downstream_consumer",
            "status_before_promotion": "withheld_noncanonical_proposal",
            "status_after_promotion": "withheld",
            "prerequisites": ["owner acceptance of scope and curve selections",
                              "selected per-area replacement cost new for each reference building",
                              "Hazard terrain class per building location",
                              "exact model/docs/schema/SHA pin"],
            "limitation_flags": ["ANNUAL_AND_TAIL_METRICS_CONSUMER_OWNED", "VALUE_PER_AREA_NOT_SELECTED"],
        },
        "cap_binding": {
            "policy": "consumer_enforced_fail_closed", "enforcement_owner": "downstream_consumer",
            "checks_required": ["exact model/docs/schema/SHA pin",
                                "record routing by reference_building_id and hazus_terrain_class",
                                "terrain never defaulted and never also applied to the gust",
                                "wind and flood damage on one building in one storm together at most 100% of structure value"],
            "action_if_fail": "withhold the affected DR or downstream metric; do not substitute another record or clamp",
        },
        "promotion_gate": {"status": "blocked", "required_before_canonical_use": [
            "owner accepts scope D-TCRE-01 to D-TCRE-05 and D-TCRE-08 to D-TCRE-13, and selections D-TCRE-17 to D-TCRE-21",
            "per-area replacement cost new selected (shared with flood_real_estate)",
            "Hazard supplies a terrain class per building location",
            "independent review of the package"]},
    }


def artifact(pts) -> dict:
    tiers = rows(f"PARAMETER_TIER_TABLE_{TAG}.csv")
    return {
        "schema_version": "damage_curve_record_bundle.v3", "schema_status": "proposed_draft",
        "cell_id": CELL_ID, "damage_code_id": "TROPICAL_CYCLONE_WIND_REAL_ESTATE_HAZUS_SCREENING_V0_1",
        "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1",
        "lifecycle_state": "scaffold", "promotion_status": "proposed", "review_status": "not_yet_reviewed",
        "model_grade": "screening_source_native_adopted_tables",
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
             "source_atom_note": "Whole-building Hazus building-loss function; not an aggregate of component records."},
            {"id": CONTENTS, "subsystem": "BUILDING", "component": "CONTENTS", "treatment": "withheld",
             "y_axis": "failure_unit_damage_ratio", "denominator": "contents value (deferred)",
             "withheld_reason_codes": ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"],
             "platform_code_status": "proposed_awaiting_platform_codes"},
        ],
        "pathways": [{
            "pathway_id": P,
            "hazard_scope": {
                "included": ["tropical-cyclone wind acting on the building: wind pressure, windborne-debris impact and rain entering through wind damage, as combined in the Hazus building loss functions"],
                "excluded": ["storm surge, waves and rainfall flooding (flood_real_estate)",
                             "tornadoes spawned by the tropical cyclone (future convective-wind cell)",
                             "tree fall on the house (deferred Hazus additive term; withheld, not zero)",
                             "contents, loss of use, business interruption, land, site works"],
                "deferred_pathways": [],
                "compound_event_rule": "Keep one event_family_id; wind and flood damage on the same building in one storm must together stay at or below 100% of structure value; no separate debris or rain-ingress pathway may be added to Hazus-based records.",
            },
            "hazard_axis": {
                "id": "TC_PEAK_GUST_3S_10M_OPEN_TERRAIN_MPH",
                "preferred_input_field": AXIS,
                "permitted_proxy_fields": [],
                "unit": "mph",
                "valid_range": [LO, HI],
                "extrapolation_policy": "gust < 0 rejects; 0 <= gust < 50 returns 0 (source zero); 50-250 straight lines between published 5-mph points; > 250 withholds",
                "averaging_period_s": 3, "reference_height_m": 10, "terrain_basis": "open terrain, z0 0.03 m",
                "bridge": "none in Damage; Hazard converts STORM 10-minute wind to the 3-second gust",
                "category_guardrail": "Saffir-Simpson category and sustained wind are not accepted damage inputs.",
            },
            "record_routing_fields": ["reference_building_id", "hazus_terrain_class"],
            "selector_logic": [
                {"field": "reference_building_id", "required": True, "default": None, "allowed": list(BUILDINGS),
                 "effect": "Fixed identity of the reference building; picks the Hazus building type and characteristics."},
                {"field": "hazus_terrain_class", "required": True, "default": None, "allowed": TERRAINS,
                 "effect": "Fixed site attribute (Hazus surface-roughness class); picks the terrain record. Never interpolated; never also applied to the gust."},
            ] + characteristic_selectors(),
            "conditioner_logic": [],
            "wind_characteristic_contract": {b: spec["characteristics"] for b, spec in BUILDINGS.items()},
            "hazus_variants": {b: {"sbt": spec["sbt"], "wbid": spec["wbid"], "case": spec["case"],
                                   "damage_loss_desc_id": 5, "simcenter_id_stem": spec["simcenter_id"],
                                   "wind_building_characteristics": {f: c["reference"] for f, c in spec["characteristics"].items()}}
                               for b, spec in BUILDINGS.items()},
            "exposure_contract": {
                "required_subject_grain": "one reference building",
                "value_rule": "Scenario dollars need structure replacement cost new for the same building; withheld in v0.1.",
                "protection_rule": "Opening protection and roof upgrades are characteristics with published values only; no curve-side credit.",
                "terrain_rule": "The consumer maps site roughness to one Hazus terrain class; Damage never defaults it.",
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
            "scenario_loss_status": "withheld_value_per_area_not_selected",
            "rejected_denominators": ["depreciated value", "market value", "assessed value"],
            "implicit_default_profile": None,
        },
        "parameter_tier_table": tiers,
        "evaluation_contract": {
            "supported_pathway_id": P, "supported_failure_unit_id": UNIT,
            "required_selector_fields": ["reference_building_id", "hazus_terrain_class"],
            "required_conditioner_fields": [],
            "optional_characteristic_fields": sorted({f for s in BUILDINGS.values() for f in s["characteristics"]}),
            "accepted_axis_payloads": [{"mode": "open_terrain_gust_mph", "required_fields": [AXIS]}],
            "metadata_flags_always": ALWAYS,
            "out_of_range_behavior": "above 250 mph: withhold; 0 to 50 mph: 0; negative: error",
            "reference_evaluator": "scripts/reference_helpers/tropical_cyclone_wind_real_estate_curve_eval.py",
        },
        "emit_contract": {
            "schema_version": "damage_emit.v2",
            "populated_emit_modes_for_this_cell": ["scalar_mean"],
            "supported_output": "conditional scalar DR for TCRE_BUILDING_STRUCTURE",
            "scenario_loss": "withheld until a per-area replacement cost new is selected",
            "annual_and_tail_metrics": "withheld; consumer-owned",
            "withheld_units_emit": "explicit null DR plus reason codes; never zero",
        },
        "capability_declaration": capability(),
        "derivation_rationale": {
            "source_spine": "FEMA Hazus hurricane building-loss functions (Hazus 7.0 TM method; Hazus 6.1 FEMA extract values), verified identical to SimCenter's independent Hazus 5.1 copy.",
            "adopted_form": "exact published 5-mph tables, straight lines between published points",
            "why_not_smooth_fits": "41 published points per record; nothing to fill and a fit could only move published values.",
            "parameter_tier_mix": "Ordinates T2; building types T2-T3; wind characteristics T4 assumptions from T2 frequencies; terrain required input; value per area open.",
        },
        "legacy_comparison": {"prior_cell_state": "none; new cell",
                              "legacy_arrays_used": "none (legacy Climada residential and Unanwa straight-line arrays rejected, D-TCRE-10)",
                              "canonical_or_consumer_change": False},
    }


def known_answer_tests(pts) -> dict:
    def req(building, terrain, gust, **extra):
        return {"pathway_id": P, "failure_unit_id": UNIT, "reference_building_id": building,
                "hazus_terrain_class": terrain, AXIS: gust, **extra}

    formula, withheld, errors = [], [], []
    for building, spec in BUILDINGS.items():
        for terrain in TERRAINS:
            p, cid = pts[(building, terrain)], curve_id(building, terrain)
            for x, y in p:  # every published point
                formula.append({"test_id": f"{cid}_KNOT_{x:g}MPH", "input": req(building, terrain, x),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": y}})
            for x in (122.5, 61.4, 228.8):  # between published points; Hazard's range ends
                formula.append({"test_id": f"{cid}_BETWEEN_{x:g}MPH", "input": req(building, terrain, x),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": interp(p, x)}})
            formula.append({"test_id": f"{cid}_BELOW_RANGE_ZERO", "input": req(building, terrain, 40.0),
                            "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": 0.0,
                                         "metadata_flags_include": ["BELOW_SOURCE_RANGE_ZERO"]}})
            withheld.append({"test_id": f"{cid}_ABOVE_RANGE", "input": req(building, terrain, HI + 0.0001),
                             "expected": {"status": "withheld", "reason_code": "ABOVE_SOURCE_VALID_RANGE"}})
        p = pts[(building, "suburban")]
        ref = {f: c["reference"] for f, c in spec["characteristics"].items()}
        formula.append({"test_id": f"{building}_REFERENCE_CHARACTERISTICS_SUPPLIED", "input": req(building, "suburban", 130.0, **ref),
                        "expected": {"status": "conditional", "curve_id": curve_id(building, "suburban"),
                                     "failure_unit_damage_ratio": interp(p, 130.0)}})
        formula.append({"test_id": f"{building}_REFERENCE_DEFAULT_FLAGGED", "input": req(building, "suburban", 130.0),
                        "expected": {"status": "conditional", "curve_id": curve_id(building, "suburban"),
                                     "failure_unit_damage_ratio": interp(p, 130.0),
                                     "metadata_flags_include": ["REFERENCE_WIND_CHARACTERISTICS_DEFAULT_USED"]}})
        withheld.append({"test_id": f"{building}_SHUTTERS_VARIANT_WITHHELD", "input": req(building, "suburban", 130.0, hazus_shutters="yes"),
                         "expected": {"status": "withheld", "reason_code": "WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED"}})
        withheld.append({"test_id": f"{building}_CONTENTS_WITHHELD", "input": {**req(building, "suburban", 130.0), "failure_unit_id": CONTENTS},
                         "expected": {"status": "withheld", "reason_code": "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT"}})
    withheld.append({"test_id": "WAREHOUSE_SUPERIOR_DECK_WITHHELD",
                     "input": req("RE_IND_WAREHOUSE", "open", 120.0, hazus_metal_deck_attachment="superior"),
                     "expected": {"status": "withheld", "reason_code": "WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED"}})
    formula.append({"test_id": "ZERO_GUST", "input": req("RE_RES_SFD_1S_SLAB", "open", 0),
                    "expected": {"status": "conditional", "curve_id": "TCRE_RES_HAZUS_WSF1_OPEN", "failure_unit_damage_ratio": 0.0}})
    base = req("RE_RES_SFD_1S_SLAB", "suburban", 130.0)
    drop = lambda k: {key: v for key, v in base.items() if key != k}  # noqa: E731
    for tid, inp, code in [
        ("PATHWAY_REQUIRED", drop("pathway_id"), "PATHWAY_ID_REQUIRED"),
        ("PATHWAY_UNKNOWN", {**base, "pathway_id": "tropical_cyclone_rain_ingress"}, "PATHWAY_ID_UNKNOWN"),
        ("BUILDING_REQUIRED", drop("reference_building_id"), "REFERENCE_BUILDING_ID_REQUIRED"),
        ("BUILDING_UNKNOWN", {**base, "reference_building_id": "RE_HOSPITAL"}, "REFERENCE_BUILDING_ID_UNKNOWN"),
        ("TERRAIN_REQUIRED", drop("hazus_terrain_class"), "TERRAIN_CLASS_REQUIRED"),
        ("TERRAIN_UNKNOWN", {**base, "hazus_terrain_class": "urban"}, "TERRAIN_CLASS_UNKNOWN"),
        ("TERRAIN_AS_ROUGHNESS_NUMBER", {**base, "hazus_terrain_class": 0.35}, "TERRAIN_CLASS_UNKNOWN"),
        ("AXIS_REQUIRED", drop(AXIS), "AXIS_PAYLOAD_REQUIRED"),
        ("AXIS_NOT_NUMBER", {**base, AXIS: "130"}, "AXIS_VALUE_INVALID"),
        ("AXIS_BOOLEAN", {**base, AXIS: True}, "AXIS_VALUE_INVALID"),
        ("AXIS_NEGATIVE", {**base, AXIS: -5.0}, "NEGATIVE_GUST"),
        ("UNIT_UNKNOWN", {**base, "failure_unit_id": "TCRE_ROOF"}, "FAILURE_UNIT_ID_UNKNOWN"),
        ("CHARACTERISTIC_FIELD_UNKNOWN", {**base, "hazus_roof_color": "white"}, "WIND_CHARACTERISTIC_FIELD_UNKNOWN"),
        ("CHARACTERISTIC_NOT_APPLICABLE", {**base, "hazus_window_area": "low"}, "WIND_CHARACTERISTIC_NOT_APPLICABLE"),
        ("CHARACTERISTIC_VALUE_UNKNOWN", {**base, "hazus_roof_shape": "mansard"}, "WIND_CHARACTERISTIC_VALUE_UNKNOWN"),
    ]:
        errors.append({"test_id": tid, "input": inp, "expected_error_code": code})
    return {
        "schema_version": "known_answer_tests.v3", "cell_id": CELL_ID,
        "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1",
        "artifact_schema_version": "damage_curve_record_bundle.v3", "artifact_status": "noncanonical_proposal",
        "absolute_tolerance": 1e-12,
        "equation": {"runtime": "straight lines between the published 5-mph points of the selected record",
                     "axis": "peak 3-second gust at 10 m, open terrain, mph; terrain enters only through the record",
                     "ranges": "0 to 50 mph returns 0; 50 to 250 mph evaluates; above 250 mph withholds"},
        "formula_known_answer_tests": formula, "withheld_tests": withheld, "error_tests": errors,
        "contract_assertions": [
            {"assertion_id": "TCRE_TERRAIN_NEVER_DEFAULTED", "expected": "a missing terrain class is an error, never a default"},
            {"assertion_id": "TCRE_NO_SEPARATE_DEBRIS_OR_RAIN_PATHWAY", "expected": "debris and rain ingress are inside the Hazus record; no added pathway"},
            {"assertion_id": "TCRE_NO_DOLLARS_V0_1", "expected": "no scenario dollars until a per-area replacement cost new is selected"},
            {"assertion_id": "TCRE_TREE_FALL_WITHHELD_NOT_ZERO", "expected": "tree fall on the house is deferred and withheld, never reported as zero"},
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
        ["Generated by scripts/reference_helpers/build_tropical_cyclone_wind_real_estate_v0_1_package.py; do not edit by hand."],
        ["Damage ratio = Hazus building loss, fraction of structure replacement cost new; axis = peak 3-s gust at 10 m, open terrain, mph."],
        ["Straight lines between published 5-mph points; 0-50 mph returns 0; above 250 mph withholds; terrain class required."],
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
    sheet("curve_records", ["curve_id", "reference_building_id", "hazus_terrain_class", "gust_mph", "damage_ratio"],
          [[r["curve_id"], r["selector_match"]["reference_building_id"], r["selector_match"]["hazus_terrain_class"], x, y]
           for r in recs for x, y in r["parameters"]["points"]])
    sheet("reference_buildings", ["reference_building_id", "hazus_sbt", "hazus_wbid", "hazus_case"],
          [[b, s["sbt"], s["wbid"], s["case"]] for b, s in BUILDINGS.items()])
    sheet("wind_characteristics", ["reference_building_id", "field", "reference_value", "allowed_values"],
          [[b, f, c["reference"], ", ".join(c["allowed"])] for b, s in BUILDINGS.items() for f, c in s["characteristics"].items()])
    for name, fname in [("sources", f"SOURCE_REGISTER_{TAG}.csv"), ("claims", f"CLAIM_PARAMETER_REGISTER_{TAG}.csv"),
                        ("parameter_tiers", f"PARAMETER_TIER_TABLE_{TAG}.csv"), ("value_crosswalk", f"VALUE_CROSSWALK_{TAG}.csv"),
                        ("variant_sensitivity", f"VARIANT_SENSITIVITY_{TAG}.csv")]:
        data = rows(fname)
        sheet(name, list(data[0]), [list(r.values()) for r in data])
    sheet("known_answer_tests", ["test_id", "kind", "expected"],
          [[t["test_id"], k, json.dumps(t.get("expected", t.get("expected_error_code")))]
           for k in ("formula_known_answer_tests", "withheld_tests", "error_tests") for t in kats[k]])
    for s in wb.worksheets:
        s.column_dimensions["A"].width = 42
    wb.properties.creator = f"{CELL_ID} builder"
    import datetime
    fixed = datetime.datetime(2026, 10, 12)
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
