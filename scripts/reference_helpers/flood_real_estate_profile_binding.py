"""Profile binding for the noncanonical flood × real estate model-v0.1 proposal.

Binds the proposed curve records to the Hazard reference profiles r1 (one row per profile × pathway × water
type, including explicit gaps) and computes the floor-height sensitivity each profile asks for, by calling the
reference evaluator. Writes, inside the cell's `proposed/` folder:

    PROFILE_BINDING_<tag>.csv
    FLOOR_HEIGHT_SENSITIVITY_<tag>.csv

    python scripts/reference_helpers/flood_real_estate_profile_binding.py

Standard library only. Does not change the artifact.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import flood_real_estate_curve_eval as ev  # noqa: E402

ROOT = HERE.parents[1]
TAG = "flood_real_estate__model_v0_1__docs_r1"
PROPOSED = ROOT / "docs/cells/flood_real_estate/proposed"
ARTIFACT = PROPOSED / f"{TAG}__curve_artifact.json"
OUT_BINDING = PROPOSED / f"PROFILE_BINDING_{TAG}.csv"
OUT_SENS = PROPOSED / f"FLOOR_HEIGHT_SENSITIVITY_{TAG}.csv"

PIN = {  # Hazard reference profiles r1 (source FRE-S013)
    "profile_revision": "r1",
    "profile_repository": "aamani-ai/Hazard_Modeling",
    "profile_commit": "8b0d61c88fbcf85daa1c098516cee22398cdb524",
    "profile_file": "docs/plans/_cross_cutting/real_estate_conus/reference_candidates.yml",
    "profile_file_git_blob": "a74fb72b0a2edce593b5505e0fd8852f4c0253f8",
}
PATHWAY, WAVE = "flood_inundation_contact", "flood_wave_velocity"
FRESH, COAST = "freshwater_riverine_or_pluvial", "coastal_surge_saline"

DEMAND = ("flood_depth_above_grade_ft (preferred: the evaluator converts once with the reference first-floor height) "
          "or flood_depth_above_first_floor_ft (already converted by Hazard; never shifted again)")
DRY = ("depth above grade <= 0 returns 0 (D-FRE-24) only when depth is sent above grade; below the record range returns 0; "
       "above the record range withholds (ABOVE_SOURCE_VALID_RANGE); unknown water type withholds (FLOOD_WATER_TYPE_UNKNOWN)")
DENOM = "structure value of the same building (Hazus: structure replacement value; NACCS: structure value); components not itemized by the source"
COVERED = "foundation_and_floor;structural_frame;roof_assembly;walls_and_openings;fixed_services;interiors (as one source-native assembly)"
EXCLUDED = "contents;land;site works;business interruption;process equipment"
FRACTION = "not stated by the source: the ratio is of whole-structure value with no component list; not set to 1.0 here"
OVERLAP = "single assembly; no component response may be added for the same pathway and event"
POINT_OUT = "failure_unit_damage_ratio (expected repair/replacement fraction of structure value), conditional on the event"

ROWS = [
    # profile, selector, pathway, water, point record, bound records, applicability, reason, uncertainty, evidence, open
    ("re_house_1s_wood_slab", "RE_RES_SFD_1S_SLAB", PATHWAY, FRESH, "FRE_RES_FRESH_HAZUS_DF129", "",
     "exact_match",
     "Matches every key the source selects on: Hazus RES1, one storey, no basement (Table 5-2 default). The curve is the "
     "class average for that key; wood frame, 20-year age, no garage and 1,800 ft2 are not source keys and do not change it.",
     "none supplied (point value only); no sampleable spread",
     "FRE-S002;FRE-S003;FRE-S010;FRE-C002;FRE-C026;FRE-S012",
     "Class average, not calibrated to the profile. NFIP claims sit 9-12 points above at 0-2 ft above the floor, mostly a "
     "floor-height sensitivity (FRE-C031)."),
    ("re_house_1s_wood_slab", "RE_RES_SFD_1S_SLAB", PATHWAY, COAST, "FRE_RES_COAST_NACCS_5A",
     "FRE_RES_COAST_NACCS_5A_MIN;FRE_RES_COAST_NACCS_5A_MAX",
     "qualified_proxy",
     "NACCS prototype 5A most-likely building matches the profile: one storey, wood frame, slab, 15-30 years (profile 20). "
     "Transfer limits: North Atlantic prototype; the profile is placed CONUS-wide.",
     "Min/Max are the NACCS building-variant envelope; scenario bounds, not quantiles; do not sample",
     "FRE-S004;FRE-C005;FRE-C007;FRE-C027;FRE-S012",
     "NFIP coastal claims (95% Gulf states) sit 12-23 points above the point curve at 0-2 ft; coastal source decision "
     "D-FRE-18 open."),
    ("re_warehouse_1s_steel_slab", "RE_IND_WAREHOUSE", PATHWAY, FRESH, "FRE_IND_FRESH_HAZUS_DF341", "",
     "exact_match",
     "Matches every key the source selects on: Hazus COM2 (wholesale trade / warehouse), no basement. The curve is the class "
     "average; 100,000 ft2, the 4,000 ft2 office fitout inside it and the equipment heights are not source keys.",
     "none supplied (point value only); no sampleable spread",
     "FRE-S002;FRE-S003;FRE-S010;FRE-C002;FRE-C026;FRE-S012",
     "Only 365 NFIP claims compared, all under 3 ft above the floor. Equipment elevations (switchboard 0.5 ft, heaters 20 ft) "
     "are not used: the curve is a whole-building average."),
    ("re_warehouse_1s_steel_slab", "RE_IND_WAREHOUSE", PATHWAY, COAST, "FRE_IND_COAST_NACCS_P3",
     "FRE_IND_COAST_NACCS_P3_MIN;FRE_IND_COAST_NACCS_P3_MAX",
     "qualified_proxy",
     "NACCS prototype 3 most-likely building matches the construction: one storey, steel or light-metal frame, slab. "
     "Transfer limits: North Atlantic prototype; NACCS assumes a 1 ft floor height, the profile 0.25 ft.",
     "Min/Max are the NACCS building-variant envelope; scenario bounds, not quantiles; do not sample",
     "FRE-S004;FRE-C005;FRE-C008",
     "No usable claims evidence (25 coastal claims). Most sensitive building to floor height; coastal source decision "
     "D-FRE-18 open."),
    ("re_office_3s_slab", "", PATHWAY, FRESH, "", "", "unavailable",
     "No office record in v0.1. Hazus COM4 DF 431 ordinates are transcription-checked (29 knots) but three-storey "
     "applicability and value coverage are not yet qualified. The retail record RE_COM_LOWRISE is not an office proxy.",
     "", "FRE-S003;FRE-S005", "Office record: next research step."),
    ("re_office_3s_slab", "", PATHWAY, COAST, "", "", "unavailable",
     "No coastal office source selected; NACCS prototype 2 is a two-storey engineered commercial building and is not "
     "assigned to the office without review.", "", "FRE-S004;FRE-C008", "Office coastal choice: next research step."),
]
for profile in ("re_house_1s_wood_slab", "re_warehouse_1s_steel_slab", "re_office_3s_slab"):
    ROWS.append((profile, "", WAVE, "any", "", "", "unavailable",
                 "Wave impact, fast flow, scour and debris are a separate, deferred pathway (D-FRE-06); withheld, not zero.",
                 "", "FRE-C021", "Needs wave height or flow speed from Hazard and a curated wave curve."))

HEAD = ["profile_id", "profile_revision", "profile_repository", "profile_commit", "profile_file", "profile_file_git_blob",
        "damage_cell", "damage_code_id", "model_version", "damage_selector_reference_building_id", "pathway_id",
        "flood_water_type", "point_record_id", "bound_record_ids", "applicability", "applicability_reason",
        "demand_variable", "valid_domain_ft_above_floor", "dry_and_out_of_domain_behavior", "reference_first_floor_height_ft",
        "output_semantics", "uncertainty_meaning", "source_denominator", "covered_groups", "excluded_groups",
        "covered_fraction_status", "overlap_treatment", "evidence_ids", "open_items"]


def main() -> None:
    art = json.loads(ARTIFACT.read_text())
    pw = art["pathways"][0]
    recs = {r["curve_id"]: r for r in pw["curve_records"]}
    ffh = pw["reference_first_floor_height_ft"]
    out = [HEAD]
    for profile, sel, pathway, water, point, bounds, app, reason, unc, evid, open_ in ROWS:
        numeric = app != "unavailable"
        if numeric:
            r = recs[point]
            assert r["selector_match"] == {"reference_building_id": sel, "flood_water_type": water, "band": "point"}, point
            domain = "{} to {}".format(*r["valid_range"])
        out.append([profile, PIN["profile_revision"], PIN["profile_repository"], PIN["profile_commit"], PIN["profile_file"],
                    PIN["profile_file_git_blob"], art["cell_id"], art["damage_code_id"], art["semantic_damage_model_version"],
                    sel, pathway, water, point, bounds, app, reason,
                    DEMAND if numeric else "", domain if numeric else "", DRY if numeric else "withheld",
                    ffh[sel] if numeric else "", POINT_OUT if numeric else "", unc,
                    DENOM if numeric else "", COVERED if numeric else "", EXCLUDED if numeric else "",
                    FRACTION if numeric else "", OVERLAP if numeric else "", evid, open_])
    with OUT_BINDING.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(out)

    # floor heights requested by each profile (floor_elevation_sensitivity_ft) plus the reference value
    heights = {"RE_RES_SFD_1S_SLAB": ("re_house_1s_wood_slab", [0.0, 0.75, 1.0, 2.0]),
               "RE_IND_WAREHOUSE": ("re_warehouse_1s_steel_slab", [0.0, 0.25, 1.0, 2.0])}
    sens = [["profile_id", "damage_selector_reference_building_id", "flood_water_type", "first_floor_height_ft",
             "is_reference_height", "depth_above_grade_ft", "depth_above_floor_ft", "curve_id", "status",
             "central_damage_ratio", "naccs_min", "naccs_max", "withheld_reason"]]
    for sel, (profile, hs) in heights.items():
        for water in (FRESH, COAST):
            for h in hs:
                for d in (0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
                    res = ev.evaluate_damage_call(art, {"pathway_id": PATHWAY, "reference_building_id": sel,
                                                        "flood_water_type": water, "flood_depth_above_grade_ft": d,
                                                        "first_floor_height_ft": h})
                    fu = res["failure_unit_results"][0]
                    sc = fu.get("scenario_drs") or {}
                    lo = next((v for k, v in sc.items() if "min" in k), "")
                    hi = next((v for k, v in sc.items() if "max" in k), "")
                    sens.append([profile, sel, water, h, h == ffh[sel], d, round(d - h, 4), fu["curve_id"], fu["status"],
                                 "" if fu["scalar_central_dr"] is None else round(fu["scalar_central_dr"], 4),
                                 "" if lo in ("", None) else round(lo, 4), "" if hi in ("", None) else round(hi, 4),
                                 ";".join(fu["withheld_reason_codes"])])
    with OUT_SENS.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(sens)
    print("wrote", OUT_BINDING.name, f"({len(out) - 1} rows)", OUT_SENS.name, f"({len(sens) - 1} rows)")


if __name__ == "__main__":
    main()
