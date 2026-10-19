"""Deterministic builder for the noncanonical flood × real estate model-v0.1 / docs-r1 package.

Reads the governed CSVs in docs/cells/flood_real_estate/proposed/ and writes:
    flood_real_estate__model_v0_1__docs_r1__curve_artifact.json   (bundle v3, embedded capability)
    flood_real_estate__model_v0_1__docs_r1__capability.json       (identical standalone capability)
    known_answer_tests_flood_real_estate__model_v0_1__docs_r1.json
    damage_curve_records_flood_real_estate__model_v0_1__docs_r1.xlsx

Known-answer expectations are computed here from the ordinates CSV with a separate, minimal
interpolation, not by calling the evaluator. Requires openpyxl for the workbook.

Usage (from the repository root):
    python scripts/reference_helpers/build_flood_real_estate_v0_1_package.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELL = "docs/cells/flood_real_estate/proposed"
TAG = "flood_real_estate__model_v0_1__docs_r1"
P = "flood_inundation_contact"
UNIT = "FRE_BUILDING_STRUCTURE"
CONTENTS = "FRE_BUILDING_CONTENTS"
FRESH, COAST, UNKNOWN = "freshwater_riverine_or_pluvial", "coastal_surge_saline", "unknown"
BUILDINGS = {  # reference building -> (first-floor height ft, Hazus record, NACCS record)
    "RE_RES_SFD_1S_SLAB": (0.75, "FRE_RES_FRESH_HAZUS_DF129", "FRE_RES_COAST_NACCS_5A"),
    "RE_COM_LOWRISE": (0.25, "FRE_COM_FRESH_HAZUS_DF217", "FRE_COM_COAST_NACCS_P2"),
    "RE_IND_WAREHOUSE": (0.25, "FRE_IND_FRESH_HAZUS_DF341", "FRE_IND_COAST_NACCS_P3"),
}
SOURCE_REFS = {
    "FRE_RES_FRESH_HAZUS_DF129": ["FRE-S002#Table_5-2", "FRE-S003#DF129", "FRE-S010#DF129"],
    "FRE_COM_FRESH_HAZUS_DF217": ["FRE-S002#Table_5-2", "FRE-S003#DF217", "FRE-S010#DF217"],
    "FRE_IND_FRESH_HAZUS_DF341": ["FRE-S002#Table_5-2", "FRE-S003#DF341", "FRE-S010#DF341"],
    "FRE_RES_COAST_NACCS_5A": ["FRE-S004#Table_56"],
    "FRE_COM_COAST_NACCS_P2": ["FRE-S004#Table_25"],
    "FRE_IND_COAST_NACCS_P3": ["FRE-S004#Table_35"],
}
ALWAYS = ["NONCANONICAL_PROPOSAL", "SCREENING_SOURCE_NATIVE_ADOPTED_TABLE", "WHOLE_BUILDING_SOURCE_ATOM",
          "REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED", "NOT_FIELD_OR_CLAIMS_CALIBRATED",
          "PLATFORM_CODES_PROPOSED_NOT_ISSUED"]


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
    for building, (_, fresh, coast) in BUILDINGS.items():
        for cid, water, bands in ((fresh, FRESH, ["point"]), (coast, COAST, ["point", "lower_bound", "upper_bound"])):
            for band in bands:
                p = pts[(cid, band)]
                suffix = {"point": "", "lower_bound": "_MIN", "upper_bound": "_MAX"}[band]
                lib = "Hazus" if water == FRESH else "NACCS"
                out.append({
                    "curve_id": cid + suffix, "pathway_id": P, "failure_unit_id": UNIT,
                    "curve_form": "piecewise_linear", "x_axis": "flood_depth_above_first_floor_ft",
                    "y_axis": "failure_unit_damage_ratio", "parameters": {"points": p},
                    "valid_range": [p[0][0], p[-1][0]],
                    "interpolation_policy": "linear_between_source_knots",
                    "extrapolation_policy": f"below {p[0][0]:g} ft returns 0 (published zero region); above {p[-1][0]:g} ft withholds; no clamp",
                    "selector_match": {"reference_building_id": building, "flood_water_type": water, "band": band},
                    "source_parameter_refs": SOURCE_REFS[cid],
                    "metadata_flags": [f"{lib.upper()}_SOURCE_TABLE"] + (
                        ["NACCS_NORTH_ATLANTIC_TRANSFER_LIMIT"] if lib == "NACCS" else ["HAZUS_CLASS_AVERAGE_OR_GENERIC_DEFAULT"]) + (
                        ["NACCS_5A_LOW_AGAINST_FEMA_ESTIMATES"] if cid == "FRE_RES_COAST_NACCS_5A" else []) + (
                        ["SINGLE_USACE_DISTRICT_GALVESTON"] if cid in ("FRE_COM_FRESH_HAZUS_DF217", "FRE_IND_FRESH_HAZUS_DF341") else []) + (
                        ["BUILDING_VARIANT_BOUND_NOT_PROBABILITY"] if band != "point" else []),
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
                "reference_building_id must be one of the three proposed reference buildings",
                "flood_water_type must be freshwater_riverine_or_pluvial or coastal_surge_saline; unknown withholds",
                "depth is referenced to the first finished floor; depth above grade of 0 or less is not inundated and returns 0",
                "freshwater records are valid from -4 to 24 ft and coastal records from -1 to 10 ft above the floor; above withholds",
                "bounds are emitted for coastal records only and are NACCS building-variant bounds, not a probability spread",
                "scenario dollars stay withheld until a per-area replacement cost new is selected",
                "owner acceptance of the scope and selections is required before any canonical use",
            ],
            "limitation_flags": ALWAYS + ["FRESHWATER_COASTAL_LIBRARY_GAP_UNRESOLVED",
                                          "WAVE_VELOCITY_PATHWAY_DEFERRED_WITHHELD_NOT_ZERO",
                                          "VALUE_PER_AREA_NOT_SELECTED"],
            "withheld_failure_units": [{"failure_unit_id": CONTENTS, "reason_codes": [
                "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT"]}],
        }],
        "consumer_annual_metrics": {
            "computation_owner": "downstream_consumer",
            "status_before_promotion": "withheld_noncanonical_proposal",
            "status_after_promotion": "withheld",
            "prerequisites": ["owner acceptance of scope and curve selections",
                              "selected per-area replacement cost new for each reference building",
                              "Hazard frequency-depth coupling supplying flood_water_type per event",
                              "exact model/docs/schema/SHA pin"],
            "limitation_flags": ["ANNUAL_AND_TAIL_METRICS_CONSUMER_OWNED", "VALUE_PER_AREA_NOT_SELECTED"],
        },
        "cap_binding": {
            "policy": "consumer_enforced_fail_closed", "enforcement_owner": "downstream_consumer",
            "checks_required": ["exact model/docs/schema/SHA pin",
                                "record-level valid range enforced (coastal records stop at 10 ft)",
                                "record routing by reference_building_id and flood_water_type",
                                "one building value charged once per event across pathways"],
            "action_if_fail": "withhold the affected DR or downstream metric; do not substitute another record or clamp",
        },
        "promotion_gate": {"status": "blocked", "required_before_canonical_use": [
            "the reviewer accepts scope D-FRE-01 to D-FRE-06 and selections D-FRE-16 to D-FRE-24",
            "per-area replacement cost new selected (D-FRE-23)",
            "consumer integration resolves record-level ranges and water-type routing",
            "independent review of the package"]},
    }


def artifact(pts) -> dict:
    tiers = rows(f"PARAMETER_TIER_TABLE_{TAG}.csv")
    cap = capability()
    return {
        "schema_version": "damage_curve_record_bundle.v3", "schema_status": "proposed_draft",
        "cell_id": "flood_real_estate", "damage_code_id": "FLOOD_REAL_ESTATE_HAZUS_NACCS_SCREENING_V0_1",
        "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1",
        "lifecycle_state": "scaffold", "promotion_status": "proposed", "review_status": "not_yet_reviewed",
        "model_grade": "screening_source_native_adopted_tables",
        "package_release": "unreleased", "package_baseline": "library v2.5", "package_inclusion_status": "not_included",
        "canonical_runtime_artifact": False,
        "source_dossier": f"{CELL}/flood_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md",
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
                "extrapolation_policy": "record-level ranges govern: freshwater -4 to 24 ft, coastal -1 to 10 ft; below a record range returns 0; above withholds",
                "bridge": "flood_depth_above_first_floor_ft = flood_depth_above_grade_ft - first_floor_height_ft; depth above grade <= 0 is not inundated (DR 0)",
            },
            "reference_first_floor_height_ft": {b: v[0] for b, v in BUILDINGS.items()},
            "record_routing_fields": ["reference_building_id", "flood_water_type", "band"],
            "selector_logic": [{"field": "reference_building_id", "required": True, "default": None,
                                "allowed": list(BUILDINGS),
                                "effect": "Fixed identity of the reference building; picks the occupancy-specific record."}],
            "conditioner_logic": [{"field": "flood_water_type", "required": True,
                                   "allowed": [FRESH, COAST, UNKNOWN],
                                   "numeric_support_when": [FRESH, COAST],
                                   "withhold_otherwise": "FLOOD_WATER_TYPE_UNKNOWN",
                                   "effect": "Event-time state; routes to the Hazus (freshwater) or NACCS (coastal surge) record. Never blended."}],
            "exposure_contract": {
                "required_subject_grain": "one reference building",
                "value_rule": "Scenario dollars need structure replacement cost new for the same building; withheld in v0.1.",
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
            "scenario_loss_status": "withheld_value_per_area_not_selected",
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
            "supported_output": "conditional scalar DR for FRE_BUILDING_STRUCTURE; coastal records add NACCS Min/Max building-variant bounds",
            "scenario_loss": "withheld until a per-area replacement cost new is selected",
            "annual_and_tail_metrics": "withheld; consumer-owned",
            "withheld_units_emit": "explicit null DR plus reason codes; never zero",
        },
        "capability_declaration": cap,
        "derivation_rationale": {
            "source_spine": "FEMA Hazus 7.0 Table 5-2 riverine structure defaults (freshwater) and USACE NACCS 2015 inundation prototypes (coastal surge), verified against originals and independent copies.",
            "adopted_form": "exact published tables, straight lines between published points",
            "why_not_smooth_fits": "Smooth fits (incl. anchored logistic) predicted held-out points worse on all six point curves and moved published values by 2-6 points.",
            "parameter_tier_mix": "Ordinates T2 with stated transfer limits; first-floor heights T2 (house) and T3 (commercial, warehouse); value per area open (T4 placeholder, not used).",
        },
        "legacy_comparison": {"prior_cell_state": "none; new cell", "legacy_arrays_used": "none (Real Estate_Hail rejected, D-FRE-11)",
                              "canonical_or_consumer_change": False},
    }


def known_answer_tests(pts) -> dict:
    def req(building, water, **axis):
        return {"pathway_id": P, "failure_unit_id": UNIT, "reference_building_id": building,
                "flood_water_type": water, **axis}

    formula, withheld, errors = [], [], []
    for building, (ffh, fresh, coast) in BUILDINGS.items():
        for cid, water in ((fresh, FRESH), (coast, COAST)):
            p = pts[(cid, "point")]
            for x, y in p:  # every published point
                formula.append({"test_id": f"{cid}_KNOT_{x:+g}FT", "input": req(building, water, flood_depth_above_first_floor_ft=x),
                                "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": y}})
            mid = (p[2][0] + p[3][0]) / 2  # an interior point between published depths
            formula.append({"test_id": f"{cid}_BETWEEN_{mid:+g}FT", "input": req(building, water, flood_depth_above_first_floor_ft=mid),
                            "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": interp(p, mid)}})
            g = 2.0  # bridge from depth above grade with the reference first-floor height
            formula.append({"test_id": f"{cid}_BRIDGE_2FT_ABOVE_GRADE", "input": req(building, water, flood_depth_above_grade_ft=g),
                            "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": interp(p, g - ffh),
                                         "metadata_flags_include": ["REFERENCE_FIRST_FLOOR_HEIGHT_DEFAULT_USED"]}})
            formula.append({"test_id": f"{cid}_NOT_INUNDATED", "input": req(building, water, flood_depth_above_grade_ft=0),
                            "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": 0.0,
                                         "metadata_flags_include": ["NOT_INUNDATED_ABOVE_GRADE"]}})
            hi = p[-1][0]
            withheld.append({"test_id": f"{cid}_ABOVE_RANGE", "input": req(building, water, flood_depth_above_first_floor_ft=hi + 0.0001),
                             "expected": {"status": "withheld", "reason_code": "ABOVE_SOURCE_VALID_RANGE"}})
            formula.append({"test_id": f"{cid}_BELOW_RANGE_ZERO", "input": req(building, water, flood_depth_above_first_floor_ft=p[0][0] - 0.5),
                            "expected": {"status": "conditional", "curve_id": cid, "failure_unit_damage_ratio": 0.0,
                                         "metadata_flags_include": ["BELOW_SOURCE_RANGE_ZERO"]}})
        lo_p, hi_p = pts[(coast, "lower_bound")], pts[(coast, "upper_bound")]
        formula.append({"test_id": f"{coast}_BOUNDS_4FT", "input": req(building, COAST, flood_depth_above_first_floor_ft=4.0),
                        "expected": {"status": "conditional", "curve_id": coast, "failure_unit_damage_ratio": interp(pts[(coast, "point")], 4.0),
                                     "scenario_drs": {"naccs_min_building_variant": interp(lo_p, 4.0), "naccs_max_building_variant": interp(hi_p, 4.0)}}})
        withheld.append({"test_id": f"{building}_UNKNOWN_WATER_WITHHELD", "input": req(building, UNKNOWN, flood_depth_above_first_floor_ft=2.0),
                         "expected": {"status": "withheld", "reason_code": "FLOOD_WATER_TYPE_UNKNOWN"}})
    formula.append({"test_id": "FFH_OVERRIDE_HOUSE_FRESH", "input": req("RE_RES_SFD_1S_SLAB", FRESH, flood_depth_above_grade_ft=3.0, first_floor_height_ft=1.0),
                    "expected": {"status": "conditional", "curve_id": "FRE_RES_FRESH_HAZUS_DF129",
                                 "failure_unit_damage_ratio": interp(pts[("FRE_RES_FRESH_HAZUS_DF129", "point")], 2.0)}})
    withheld.append({"test_id": "CONTENTS_WITHHELD", "input": {**req("RE_RES_SFD_1S_SLAB", FRESH, flood_depth_above_first_floor_ft=2.0), "failure_unit_id": CONTENTS},
                     "expected": {"status": "withheld", "reason_code": "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT"}})
    base = req("RE_RES_SFD_1S_SLAB", FRESH, flood_depth_above_first_floor_ft=2.0)
    for tid, inp, code in [
        ("PATHWAY_REQUIRED", {k: v for k, v in base.items() if k != "pathway_id"}, "PATHWAY_ID_REQUIRED"),
        ("WAVE_PATHWAY_NOT_IN_ARTIFACT", {**base, "pathway_id": "flood_wave_velocity"}, "PATHWAY_ID_UNKNOWN"),
        ("BUILDING_REQUIRED", {k: v for k, v in base.items() if k != "reference_building_id"}, "REFERENCE_BUILDING_ID_REQUIRED"),
        ("BUILDING_UNKNOWN", {**base, "reference_building_id": "RE_HOSPITAL"}, "REFERENCE_BUILDING_ID_UNKNOWN"),
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
        "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1",
        "artifact_schema_version": "damage_curve_record_bundle.v3", "artifact_status": "noncanonical_proposal",
        "absolute_tolerance": 1e-12,
        "equation": {"runtime": "straight lines between published points of the selected record",
                     "bridge": "depth above floor = depth above grade - first-floor height; depth above grade <= 0 returns 0",
                     "ranges": "freshwater -4..24 ft, coastal -1..10 ft above the floor; below returns 0; above withholds"},
        "formula_known_answer_tests": formula, "withheld_tests": withheld, "error_tests": errors,
        "contract_assertions": [
            {"assertion_id": "FRE_LIBRARIES_NEVER_BLENDED", "expected": "freshwater and coastal records are never averaged or substituted"},
            {"assertion_id": "FRE_BOUNDS_NOT_PROBABILITY", "expected": "NACCS Min/Max bounds are building-variant bounds, not a spread for PML/VaR"},
            {"assertion_id": "FRE_NO_DOLLARS_V0_1", "expected": "no scenario dollars until a per-area replacement cost new is selected"},
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
        ["flood_real_estate model v0.1 / docs r1 — noncanonical proposal (review workbook)"],
        ["Generated by scripts/reference_helpers/build_flood_real_estate_v0_1_package.py; do not edit by hand."],
        ["Damage ratio = fraction of structure replacement cost new; depth in ft above the first finished floor."],
        ["Straight lines between published points; freshwater -4..24 ft, coastal -1..10 ft; above withholds."],
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
    sheet("curve_records", ["curve_id", "reference_building_id", "flood_water_type", "band", "depth_above_floor_ft", "damage_ratio"],
          [[r["curve_id"], r["selector_match"]["reference_building_id"], r["selector_match"]["flood_water_type"],
            r["selector_match"]["band"], x, y] for r in recs for x, y in r["parameters"]["points"]])
    sheet("reference_buildings", ["reference_building_id", "first_floor_height_ft", "freshwater_record", "coastal_record"],
          [[b, v[0], v[1], v[2]] for b, v in BUILDINGS.items()])
    for name, fname in [("sources", f"SOURCE_REGISTER_{TAG}.csv"), ("claims", f"CLAIM_PARAMETER_REGISTER_{TAG}.csv"),
                        ("parameter_tiers", f"PARAMETER_TIER_TABLE_{TAG}.csv"), ("value_crosswalk", f"VALUE_CROSSWALK_{TAG}.csv")]:
        data = rows(fname)
        sheet(name, list(data[0]), [list(r.values()) for r in data])
    sheet("known_answer_tests", ["test_id", "kind", "expected"],
          [[t["test_id"], k, json.dumps(t.get("expected", t.get("expected_error_code")))]
           for k in ("formula_known_answer_tests", "withheld_tests", "error_tests") for t in kats[k]])
    for s in wb.worksheets:
        s.column_dimensions["A"].width = 42
    wb.properties.creator = "flood_real_estate builder"
    import datetime
    fixed = datetime.datetime(2026, 10, 11)
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
