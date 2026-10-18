"""Profile binding for the noncanonical convective wind × real estate model-v0.1 proposal.

Binds the model-v0.1 records to the Hazard reference profiles r1 (one row per profile and pathway) and writes
PROFILE_BINDING_convective_wind_real_estate__model_v0_1__docs_r1.csv in the cell's proposed/ folder.
Standard library only. Does not change the artifact.

    python scripts/reference_helpers/convective_wind_real_estate_profile_binding.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "convective_wind_real_estate__model_v0_1__docs_r1"
PROPOSED = ROOT / "docs/cells/convective_wind_real_estate/proposed"
ARTIFACT = PROPOSED / f"{TAG}__curve_artifact.json"
OUT = PROPOSED / f"PROFILE_BINDING_{TAG}.csv"
PIN = ["r1", "aamani-ai/Hazard_Modeling", "8b0d61c88fbcf85daa1c098516cee22398cdb524",
       "docs/plans/_cross_cutting/real_estate_conus/reference_candidates.yml", "a74fb72b0a2edce593b5505e0fd8852f4c0253f8"]
SL, TOR = "straight_line_convective", "tornado_direct_hit"
DEMAND = {
    SL: "convective_gust_3s_10m_mph: ASCE 7-22 3-second gust at 10 m, Exposure C, as Hazard delivers it; no averaging, height or terrain bridge in Damage",
    TOR: "tornado_gust_3s_10m_mph: 3-second gust; Hazard's EF band midpoint gust accepted as a damage-inferred bridge; an EF rating is never evaluated",
}
DOMAIN = {
    SL: "0 to 96 mph returns 0 (onset); 96 to 255 mph straight lines between 1-mph knots; above 255 withheld (ABOVE_SOURCE_VALID_RANGE); negative gust is an error",
    TOR: "0 to 255 mph straight lines between 1-mph knots (no onset); above 255 withheld (ABOVE_SOURCE_VALID_RANGE); negative gust is an error",
}
OUTPUT = ("failure_unit_damage_ratio: expected repair cost as a fraction of structure value for one event, from the EF "
          "degrees of damage priced through the Hazus damage states")
UNC = "none supplied (point value only); no sampleable spread; cost, spread and onset sensitivity in SENSITIVITY"
DENOM = "structure replacement cost new of the same building (Hazus damage-state loss ratios are of whole-building value)"
COVERED = "foundation_and_floor;structural_frame;roof_assembly;walls_and_openings;fixed_services;interiors (as one whole-building assembly)"
EXCLUDED = "contents;land;site works;business interruption;hail;tropical-cyclone wind (tropical_cyclone_wind_real_estate)"
FRACTION = "not stated by the source: the cost ratios are of whole-building value with no component list; not set to 1.0 here"
OVERLAP = {
    SL: "single assembly; each gust routed to one pathway; all perils on one building in one event together at most 100% of structure value (consumer)",
    TOR: "single assembly; tornado-specific effects inside the EF observations (no add-on); a TC-spawned tornado priced here or under hurricane, never both (consumer)",
}
REASON = {
    ("RE_RES_SFD_1S_SLAB", TOR): "EF FR12 (one- and two-family residences, 1,000-5,000 ft2) matches the profile's one-storey 1,800 ft2 wood house. Tornado degrees of damage used directly.",
    ("RE_IND_WAREHOUSE", TOR): "EF MBS (metal building systems; examples warehouses; large overhead doors) matches the profile's one-storey steel warehouse with eight overhead doors. Tornado degrees of damage used directly.",
    ("RE_COM_OFFICE_3S_SLAB", TOR): "EF LRB (low-rise 1-4 storeys; examples office buildings; steel frame; single-ply roof) matches the profile's three-storey steel office with a TPO roof. Tornado degrees of damage used directly.",
}
for b in ("RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB"):
    REASON[(b, SL)] = (REASON[(b, TOR)].replace("Tornado degrees of damage used directly.", "")
                       + "Qualified: the tornado-derived degrees of damage are transferred to straight-line wind (T4) with a 96 mph onset.")
APPLIC = {TOR: "exact_match", SL: "qualified_proxy"}
EVID = {
    "RE_RES_SFD_1S_SLAB": "CWRE-S001;CWRE-S002;CWRE-S003;CWRE-S004;CWRE-C003;CWRE-C007;CWRE-C010",
    "RE_IND_WAREHOUSE": "CWRE-S001;CWRE-S002;CWRE-S003;CWRE-S004;CWRE-C004;CWRE-C008;CWRE-C010",
    "RE_COM_OFFICE_3S_SLAB": "CWRE-S001;CWRE-S002;CWRE-S003;CWRE-S004;CWRE-C005;CWRE-C009;CWRE-C010",
}
PATH_EVID = {SL: ";CWRE-C013;CWRE-C014;CWRE-C016;CWRE-C018", TOR: ";CWRE-C012;CWRE-C015"}
OPEN = {
    ("RE_RES_SFD_1S_SLAB", SL): "Foundation shift priced as Extensive (50%); as Complete the house reads 48% instead of 32% at 120 mph. Onset fixed, not by location.",
    ("RE_RES_SFD_1S_SLAB", TOR): "Foundation shift priced as Extensive (50%); as Complete the house reads 52% instead of 36% at 120 mph.",
    ("RE_IND_WAREHOUSE", SL): "Onset fixed, not by location.",
    ("RE_IND_WAREHOUSE", TOR): "",
    ("RE_COM_OFFICE_3S_SLAB", SL): "Onset fixed, not by location.",
    ("RE_COM_OFFICE_3S_SLAB", TOR): "",
}
HEAD = ["profile_id", "profile_revision", "profile_repository", "profile_commit", "profile_file", "profile_file_git_blob",
        "damage_cell", "damage_code_id", "model_version", "damage_selector_reference_building_id", "pathway_id",
        "record_ids", "applicability", "applicability_reason", "ef_damage_indicator", "demand_variable",
        "valid_domain_and_behavior", "output_semantics", "uncertainty_meaning", "source_denominator",
        "covered_groups", "excluded_groups", "covered_fraction_status", "overlap_treatment", "evidence_ids", "open_items"]


def main() -> None:
    art = json.loads(ARTIFACT.read_text())
    out = [HEAD]
    for pw in art["pathways"]:
        p = pw["pathway_id"]
        for sel, profile in pw["reference_profile_binding"].items():
            recs = [r["curve_id"] for r in pw["curve_records"] if r["selector_match"]["reference_building_id"] == sel]
            assert len(recs) == 1, (p, sel)
            out.append([profile, *PIN, art["cell_id"], art["damage_code_id"], art["semantic_damage_model_version"], sel, p,
                        recs[0], APPLIC[p], REASON[(sel, p)], pw["ef_damage_indicators"][sel]["di"], DEMAND[p], DOMAIN[p],
                        OUTPUT, UNC, DENOM, COVERED, EXCLUDED, FRACTION, OVERLAP[p], EVID[sel] + PATH_EVID[p], OPEN[(sel, p)]])
    with OUT.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(out)
    print("wrote", OUT.name, f"({len(out) - 1} rows)")


if __name__ == "__main__":
    main()
