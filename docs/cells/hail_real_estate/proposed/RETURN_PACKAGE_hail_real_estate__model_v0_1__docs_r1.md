<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# Return package for Hazard — hail × real estate, model v0.1

This is the Damage return for hail on the three Hazard reference profiles r1, in the fields the profile handoff asks
for: one card per profile. Everything is a **noncanonical proposal** (model v0.1 / docs r1, promotion gate blocked),
and nothing is admitted at runtime. The binding table is
[PROFILE_BINDING](PROFILE_BINDING_hail_real_estate__model_v0_1__docs_r1.csv).

## 1. Summary

| Profile | Roof cover record (share of structure value) | Walls & windows record, Tier-4 (share) | Withheld |
|---|---|---|---|
| `re_house_1s_wood_slab` | `HRE_RES_ROOF_ASPHALT_SHINGLE_LAMINATED` (3.75%) | `HRE_RES_WALLS_WINDOWS_T4` (6.07%) | AC condenser; contents |
| `re_warehouse_1s_steel_slab` | `HRE_IND_ROOF_STANDING_SEAM_STEEL` (12%) | `HRE_IND_WINDOWS_T4` (0.57%) | rooftop unit; contents |
| `re_office_3s_slab` | `HRE_OFF_ROOF_TPO_MEMBRANE_AND_INSULATION` (2.7%) | `HRE_OFF_WINDOWS_T4` (5.34%) | six rooftop units; contents |

Shared by all three cards:

| Item | Content |
|---|---|
| Profile pin | Hazard reference profiles **r1**, `aamani-ai/Hazard_Modeling` commit `8b0d61c88fbcf85daa1c098516cee22398cdb524`, `reference_candidates.yml` (git blob `a74fb72b0a2edce593b5505e0fd8852f4c0253f8`); source HRE-S007 |
| Damage artifact | `hail_real_estate` model v0.1 / docs r1, [`hail_real_estate__model_v0_1__docs_r1__curve_artifact.json`](hail_real_estate__model_v0_1__docs_r1__curve_artifact.json) (sha256 in the [validation report](VALIDATION_REPORT_hail_real_estate__model_v0_1__docs_r1.md)), branch `cell/hail-real-estate` of `aamani-ai/Damage_Modeling` |
| Pathway, units | `hail_impact`. Priced units: `HRE_ROOF_COVER` and `HRE_WALLS_AND_WINDOWS`; the walls unit needs `screening_assumption_set_id = HRE_T4_WALLS_WINDOWS_SCREENING_2026_10_18`. `HRE_EXPOSED_EQUIPMENT` and `HRE_BUILDING_CONTENTS` are withheld, not zero |
| Demand | `mesh_diameter_mm`: Hazard's MESH75 per native pixel, as delivered (the same field as hail × solar), read as the largest hailstone at the building. No bridge in Damage. Hazard's smallest nonzero input is 38.98 mm |
| Domain | 0–203.2 mm, straight lines between 1-mm knots; above 203.2 mm → withheld `ABOVE_SOURCE_VALID_RANGE`; negative → error |
| Output | Conditional replaced fraction of **the unit's own value** for one event (roof: chance the cover is replaced). Building level = unit DR × unit share. Not a damage-state probability of the whole building |
| Uncertainty | Point value only; band readings, low/high cases and cost shares in [SENSITIVITY](SENSITIVITY_hail_real_estate__model_v0_1__docs_r1.csv); a scenario band, not sampleable |
| Value | Unit replacement cost, with shares of structure replacement cost new (shared with flood, hurricane and convective). Cosmetic denting, interior leakage, frame, interiors, contents, land and BI are not priced |
| Overlap | Roof and walls units are disjoint. Hail and wind or flood on one building in one event: at most 100% of structure value, and no double replacement of one roof cover (consumer) |
| Consumer probe | Hazard `damage_loader.py` (main `20de377`, blob `4bdadaa1`): 198 of 206 known-answer requests agree, including every priced and withheld value. The eight differences are error-code names ([validation report](VALIDATION_REPORT_hail_real_estate__model_v0_1__docs_r1.md) §4) |
| Reproduce | `derive_hail_real_estate_curves.py`; `hail_real_estate_nri_check.py`; `build_hail_real_estate_v0_1_package.py`; `hail_real_estate_profile_binding.py`; `validate_hail_real_estate_v0_1_package.py` |
| Missing profile detail | Shingle type, TPO attachment and cover board, and steel panel gauge. Each is covered by a low or high case |

## 2. Card — `re_house_1s_wood_slab`

| Field | Content |
|---|---|
| Applicability | Roof: asphalt shingles, 10 years old. Haag thresholds for 11-year-old laminated shingles apply (qualified proxy; type not stated). Walls & windows: vinyl siding and 15% windows (Tier-4) |
| Evidence | HRE-S001 (Haag AMS 2002, Tables 2–3), S013 (IIBEC 2013), S006 (Hazus Table 8-5); HRE-C001, C002, C008, C009; walls C023 |
| Roof cover (unit DR / building %) | 1.25 in 0.05 / 0.19%; MESH75 floor 38.98 mm 0.42 / 1.56%; 1.75 in 0.76 / 2.85%; 2 in 0.95 / 3.56%; 2.5 in and above 1.00 / 3.75% |
| Walls & windows (building %) | 1.5 in 0.53%; 2 in 1.80%; 2.5 in 2.17% (ceiling 2.21%) |
| Uncertainty | 3-tab shingles (high): 1.39% at 1.25 in, 2.89% at 1.5 in. No Hazus repair factor (low): ceiling 3.0% |
| Open | Shingle type and impact rating (assumed laminated, not impact-rated) |

## 3. Card — `re_warehouse_1s_steel_slab`

| Field | Content |
|---|---|
| Applicability | Roof: standing-seam steel, 10 years old. The Haag rupture threshold of 2.5 in applies to functional damage (qualified proxy; gauge not stated). Cosmetic denting excluded. Windows (2% of wall) Tier-4; metal wall panels and overhead doors excluded (dents) |
| Evidence | HRE-S002, S003, S004, S007; HRE-C004, C005, C021, C022 |
| Roof cover (unit DR / building %) | below 2.5 in about 0; 2.5 in 0.05 / 0.60%; 3 in 0.55 / 6.66%; 3.5 in 0.95 / 11.40%; 4 in 1.00 / 12.0% |
| Uncertainty | Roof share 9–15% (judgment). Full damage at 3.0 or 4.0 in. Counting cosmetic denting from 1.5 in (not adopted) would give 6.99% at 2 in |
| Note | Under Hazard's MESH75, inputs above 63.5 mm need raw MESH above about 83 mm, so the warehouse roof is rarely damaged. Its yearly loss comes almost entirely from windows |

## 4. Card — `re_office_3s_slab`

| Field | Content |
|---|---|
| Applicability | Roof: TPO membrane on insulated metal deck, 10 years old. The Haag thermoplastic single-ply range of 1–2 in applies (qualified proxy; attachment not stated); insulation is replaced with the membrane. Windows (33% of wall) Tier-4; masonry veneer excluded |
| Evidence | HRE-S002, S004, S005, S006 (Table 8-11); HRE-C004, C006, C007, C010 |
| Roof cover (unit DR / building %) | 1 in 0.05 / 0.13%; 1.25 in 0.28 / 0.75%; MESH75 floor 0.65 / 1.76%; 2 in 0.95 / 2.57%; 2.5 in and above 1.00 / 2.70% |
| Windows (building %) | 2 in 0.78%; 2.5 in 1.27% (ceiling 1.33%) |
| Uncertainty | Adhered membrane on a cover board (low): 0.08% at 1.5 in, 1.57% at 2 in. Membrane failing at 1.0–1.5 in (high): 2.57% at 1.5 in |

## 5. Short example — house, 2-inch hail

```text
requests : hail_impact, RE_RES_SFD_1S_SLAB, mesh_diameter_mm = 50.8
           HRE_ROOF_COVER                                   -> DR 0.9497 (HRE_RES_ROOF_ASPHALT_SHINGLE_LAMINATED)
           HRE_WALLS_AND_WINDOWS + screening acknowledgement -> DR 0.2958 (HRE_RES_WALLS_WINDOWS_T4)
building : 0.9497 x 3.75% + 0.2958 x 6.0689% = 3.56% + 1.80% = 5.36% of structure value
dollars  : 0.0536 x $405,000 = $21,700 (roof $14,400), if Hazard qualifies the full budget as covered
```

## 6. Items for the Hazard team

These come from the [NRI check](hail_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md) (§13).

1. **MESH75 floor.** Every severe pixel enters damage at 38.98 mm or more, at or above the shingle and TPO onsets.
   With MESH75, house roof yearly loss is 73 times NRI in the median cell. With the earlier Version-1 transform
   (raw × 25.4/35.56) it is 1.2 times. The transform moves building loss by a factor of about 90, far more than any
   Damage choice.
2. **Point frequency.** In the median Plains cell, the house roof would be replaced about once every 5 years (once
   every 33 years in the median CONUS cell). That rests on 5.7 years of raw MRMS MESH, which over-detects severe
   hail.
3. **NRI as a floor.** NRI's national hail building loss sums to about $0.67B a year on Hazard's grid, far below
   insured US severe-convective-storm losses (about $54B in 2023). Ranking agreement (0.70) is the more useful
   signal.
4. **Footprint.** The per-pixel rule applies unchanged to small buildings. A building sits in one pixel, so its yearly
   loss is the pixel's.
