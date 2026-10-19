"""Profile binding for the noncanonical hail × real estate model-v0.1 proposal.

Binds the model-v0.1 records to the Hazard reference profiles r1 (one row per profile and failure unit, including the
withheld units) and writes PROFILE_BINDING_hail_real_estate__model_v0_1__docs_r1.csv in the cell's proposed/ folder.
Standard library only. Does not change the artifact.

    python scripts/reference_helpers/hail_real_estate_profile_binding.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "hail_real_estate__model_v0_1__docs_r1"
PROPOSED = ROOT / "docs/cells/hail_real_estate/proposed"
ARTIFACT = PROPOSED / f"{TAG}__curve_artifact.json"
OUT = PROPOSED / f"PROFILE_BINDING_{TAG}.csv"
PIN = ["r1", "aamani-ai/Hazard_Modeling", "8b0d61c88fbcf85daa1c098516cee22398cdb524",
       "docs/plans/_cross_cutting/real_estate_conus/reference_candidates.yml", "a74fb72b0a2edce593b5505e0fd8852f4c0253f8"]
ROOF, WALLS, EQUIP, CONTENTS = "HRE_ROOF_COVER", "HRE_WALLS_AND_WINDOWS", "HRE_EXPOSED_EQUIPMENT", "HRE_BUILDING_CONTENTS"
DEMAND = ("mesh_diameter_mm: Hazard's MESH75 hail diameter (mm) per native pixel, as delivered, read as the largest "
          "hailstone at the building; Hazard sends no damage below raw MESH 25.4 mm, so the smallest nonzero input is 38.98 mm")
DOMAIN = "0 to 203.2 mm straight lines between 1-mm knots; above 203.2 withheld (ABOVE_SOURCE_VALID_RANGE); negative is an error"
OUTPUT = {ROOF: "failure_unit_damage_ratio: probability the roof cover needs replacing (fraction of the roof cover's replacement cost) for one event",
          WALLS: "failure_unit_damage_ratio: expected replaced fraction of the hail-vulnerable walls and windows for one event (Tier-4 screening)",
          EQUIP: "withheld (not zero)", CONTENTS: "withheld (not zero)"}
UNC = "none supplied (point value only); no sampleable spread; band reading, low/high cases and cost shares in SENSITIVITY"
DENOM = {ROOF: "replacement cost of the same building's roof cover; share of structure replacement cost new in failure_units[].share_of_structure_rcn",
         WALLS: "replacement cost of the same building's hail-vulnerable wall cladding and windows; share in failure_units[].share_of_structure_rcn",
         EQUIP: "not allocated", CONTENTS: "contents value (deferred)"}
COVERED = {ROOF: "roof_assembly (roof cover; office roof insulation)", WALLS: "walls_and_openings (house vinyl siding and windows; warehouse and office windows)",
           EQUIP: "fixed_services (outdoor AC condenser; rooftop units) — withheld", CONTENTS: "contents — withheld"}
EXCLUDED = ("cosmetic denting (metal roof, metal walls, overhead doors, gutters); fin denting; interior leakage after a roof breach; "
            "deck punctures; frame; foundation; interiors; land; site works; business interruption; wind and flood from the same storm")
OVERLAP = ("units do not overlap (roof cover vs walls and windows); building level = sum of unit DR x unit share; hail and wind or flood "
           "on one building in one event together at most 100% of structure value (consumer)")
APPLIC = {ROOF: "qualified_proxy", WALLS: "screening_t4", EQUIP: "unavailable", CONTENTS: "unavailable"}
REASON = {
    ("RE_RES_SFD_1S_SLAB", ROOF): "Profile roof is asphalt shingle on wood sheathing, 10 years old; Haag thresholds for 11-year-old laminated shingles (1.25-2.0 in) apply; shingle type (laminated vs 3-tab) not stated in the profile.",
    ("RE_IND_WAREHOUSE", ROOF): "Profile roof is standing-seam metal, 10 years old; Haag steel-panel rupture threshold 2.5 in applies to functional damage; gauge and coating not stated; cosmetic denting excluded.",
    ("RE_COM_OFFICE_3S_SLAB", ROOF): "Profile roof is TPO single-ply on insulated metal deck, 10 years old; Haag thermoplastic single-ply range 1-2 in applies; attachment, thickness and cover board not stated.",
    ("RE_RES_SFD_1S_SLAB", WALLS): "Profile walls are vinyl siding on wood sheathing with 15% windows; Tier-4 judgment sizes, hail-facing shares and costs.",
    ("RE_IND_WAREHOUSE", WALLS): "Profile walls are insulated metal panels (dents, excluded) with 2% windows; Tier-4 windows only.",
    ("RE_COM_OFFICE_3S_SLAB", WALLS): "Profile walls are masonry veneer (hail-resistant, excluded) with 33% windows; Tier-4 windows only.",
}
for b, eq in (("RE_RES_SFD_1S_SLAB", "one outdoor AC condenser"), ("RE_IND_WAREHOUSE", "one packaged rooftop unit"),
              ("RE_COM_OFFICE_3S_SLAB", "six packaged rooftop units")):
    REASON[(b, EQUIP)] = f"Profile has {eq}; fin denting is mostly cosmetic or comb-repairable and no functional hail evidence by size was found; withheld, not zero."
    REASON[(b, CONTENTS)] = "Contents are a separate deferred unit."
EVID = {ROOF: {"RE_RES_SFD_1S_SLAB": "HRE-S001;HRE-S013;HRE-S006;HRE-S007;HRE-C001;HRE-C002;HRE-C008;HRE-C009",
               "RE_IND_WAREHOUSE": "HRE-S002;HRE-S003;HRE-S004;HRE-S007;HRE-C004;HRE-C005;HRE-C021;HRE-C022",
               "RE_COM_OFFICE_3S_SLAB": "HRE-S002;HRE-S004;HRE-S005;HRE-S006;HRE-S007;HRE-C004;HRE-C006;HRE-C007;HRE-C010"},
        WALLS: {b: "HRE-S004;HRE-S007;HRE-C006;HRE-C023" for b in ("RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB")},
        EQUIP: {b: "HRE-S011;HRE-C016" for b in ("RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB")},
        CONTENTS: {b: "" for b in ("RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB")}}
OPEN = {
    ("RE_RES_SFD_1S_SLAB", ROOF): "Shingle type: 3-tab would start damage at 1.0 in (high case).",
    ("RE_IND_WAREHOUSE", ROOF): "Roof share 12% is judgment (9-15%); full-damage size 3.5 in is judgment.",
    ("RE_COM_OFFICE_3S_SLAB", ROOF): "TPO attachment and cover board decide the low case (adhered on cover board: 1.5-2.0 in).",
}
HEAD = ["profile_id", "profile_revision", "profile_repository", "profile_commit", "profile_file", "profile_file_git_blob",
        "damage_cell", "damage_code_id", "model_version", "damage_selector_reference_building_id", "pathway_id",
        "failure_unit_id", "record_ids", "unit_share_of_structure_rcn", "applicability", "applicability_reason",
        "demand_variable", "valid_domain_and_behavior", "output_semantics", "uncertainty_meaning", "source_denominator",
        "covered_groups", "excluded_groups", "overlap_treatment", "evidence_ids", "open_items"]


def main() -> None:
    art = json.loads(ARTIFACT.read_text())
    shares = {u["id"]: u.get("share_of_structure_rcn", {}) for u in art["failure_units"]}
    out = [HEAD]
    for pw in art["pathways"]:
        p = pw["pathway_id"]
        for sel, profile in pw["reference_profile_binding"].items():
            for unit in (ROOF, WALLS, EQUIP, CONTENTS):
                recs = [r["curve_id"] for r in pw["curve_records"]
                        if r["failure_unit_id"] == unit and r["selector_match"]["reference_building_id"] == sel]
                assert len(recs) == (1 if unit in (ROOF, WALLS) else 0), (sel, unit)
                share = shares[unit].get(sel, "")
                out.append([profile, *PIN, art["cell_id"], art["damage_code_id"], art["semantic_damage_model_version"], sel, p,
                            unit, ";".join(recs), share, APPLIC[unit], REASON[(sel, unit)],
                            DEMAND if recs else "", DOMAIN if recs else "", OUTPUT[unit], UNC if recs else "",
                            DENOM[unit], COVERED[unit], EXCLUDED, OVERLAP, EVID[unit][sel], OPEN.get((sel, unit), "")])
    with OUT.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(out)
    print("wrote", OUT.name, f"({len(out) - 1} rows)")


if __name__ == "__main__":
    main()
