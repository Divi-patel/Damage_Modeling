"""Profile binding for the noncanonical wildfire × real estate model-v0.1 proposal.

Binds the model-v0.1 records to the Hazard reference profiles r1 (one row per profile) and writes
PROFILE_BINDING_wildfire_real_estate__model_v0_1__docs_r1.csv in the cell's proposed/ folder.
Standard library only. Does not change the artifact.

    python scripts/reference_helpers/wildfire_real_estate_profile_binding.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "wildfire_real_estate__model_v0_1__docs_r1"
PROPOSED = ROOT / "docs/cells/wildfire_real_estate/proposed"
ARTIFACT = PROPOSED / f"{TAG}__curve_artifact.json"
OUT = PROPOSED / f"PROFILE_BINDING_{TAG}.csv"
PIN = ["r1", "aamani-ai/Hazard_Modeling", "8b0d61c88fbcf85daa1c098516cee22398cdb524",
       "docs/plans/_cross_cutting/real_estate_conus/reference_candidates.yml", "a74fb72b0a2edce593b5505e0fd8852f4c0253f8"]
DEMAND = ("conditional_flame_length_class_state: exact FSim conditional flame-length class state 0-6 (0 = no event; "
          "1 < 2 ft ... 6 12+ ft) from USFS RDS-2016-0034-3 at the building location, with source_wildfire_product_id "
          "USFS_RDS_2016_0034_3_270M; burn probability is frequency (Hazard) and never a damage input")
DOMAIN = ("integers 0-6 evaluate by exact lookup; state 0 returns 0; fractional, non-numeric or out-of-range states are "
          "errors (INVALID_CLASS_STATE); no interpolation, no clamp")
OUTPUT = ("failure_unit_damage_ratio: expected repair cost as a fraction of structure value given a fire at the "
          "building location in that class (USFS relative structure loss, read as a repair-cost ratio)")
UNC = ("none supplied (point value only); no sampleable spread; lifeform (tree / grass) and building-factor ranges in "
       "SENSITIVITY; outcomes are near all-or-nothing (DINS: 92% of damaged houses destroyed)")
DENOM = "structure replacement cost new of the same building (the source loss scale runs from no damage to complete loss of the structure)"
COVERED = "foundation_and_floor;structural_frame;roof_assembly;walls_and_openings;fixed_services;interiors (as one whole-building assembly)"
EXCLUDED = "contents;land;landscaping;site works;vehicles;smoke or ash contamination without fire damage;post-fire debris flow and erosion;business interruption"
FRACTION = "not stated by the source: whole-structure loss with no component list; not set to 1.0 here"
OVERLAP = ("single assembly; embers, radiant heat, flame contact and building-to-building spread inside the one response "
           "(no add-on); all perils on one building in one event together at most 100% of structure value (consumer)")
REASON = {
    "RE_RES_SFD_1S_SLAB": ("USFS response for a home used directly: one-storey wood-frame house with vinyl siding, asphalt "
                           "shingles and a vented attic without ember-resistant vents, matching the DINS house group "
                           "(wood/vinyl siding, asphalt roof); no mitigation or defensible-space credit."),
    "RE_IND_WAREHOUSE": ("Qualified: house response x 0.8, the CAL FIRE DINS same-fire ratio of metal-wall metal-roof "
                         "commercial buildings to houses (0.79). The profile's insulated metal panels and standing-seam roof "
                         "match the group; size (100,000 ft2), sprinklers and eight overhead doors are not in DINS."),
    "RE_COM_OFFICE_3S_SLAB": ("Qualified: house response x 0.9, the CAL FIRE DINS same-fire ratio of multi-storey "
                              "stucco/brick/cement commercial buildings to houses (0.93). The profile's masonry veneer and "
                              "three storeys match the group; TPO roof, 33% glazing and sprinklers are not resolved by DINS."),
}
APPLIC = {"RE_RES_SFD_1S_SLAB": "exact_match", "RE_IND_WAREHOUSE": "qualified_proxy", "RE_COM_OFFICE_3S_SLAB": "qualified_proxy"}
EVID = {
    "RE_RES_SFD_1S_SLAB": "WFRE-S001;WFRE-S003;WFRE-S004;WFRE-C001;WFRE-C004;WFRE-C008;WFRE-C012",
    "RE_IND_WAREHOUSE": "WFRE-S001;WFRE-S002;WFRE-S003;WFRE-S004;WFRE-C001;WFRE-C004;WFRE-C009;WFRE-C010",
    "RE_COM_OFFICE_3S_SLAB": "WFRE-S001;WFRE-S002;WFRE-S003;WFRE-S004;WFRE-C001;WFRE-C004;WFRE-C009;WFRE-C010",
}
OPEN = {
    "RE_RES_SFD_1S_SLAB": "Shrub default (tree +5 points, grass -10 to -15 points). Flame-length class carries limited information about house loss (WFRE-C011).",
    "RE_IND_WAREHOUSE": "Shrub default. Factor range 0.3 (pooled) to 1.0; same-fire 90% range 0.61-0.99.",
    "RE_COM_OFFICE_3S_SLAB": "Shrub default. Factor range 0.4 (pooled) to 1.0; same-fire 90% range 0.66-1.38.",
}
HEAD = ["profile_id", "profile_revision", "profile_repository", "profile_commit", "profile_file", "profile_file_git_blob",
        "damage_cell", "damage_code_id", "model_version", "damage_selector_reference_building_id", "pathway_id",
        "record_ids", "applicability", "applicability_reason", "building_factor", "demand_variable",
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
                        recs[0], APPLIC[sel], REASON[sel], pw["building_factors"][sel]["factor_on_house_curve"], DEMAND,
                        DOMAIN, OUTPUT, UNC, DENOM, COVERED, EXCLUDED, FRACTION, OVERLAP, EVID[sel], OPEN[sel]])
    with OUT.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(out)
    print("wrote", OUT.name, f"({len(out) - 1} rows)")


if __name__ == "__main__":
    main()
