<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# Return package for Hazard — hurricane wind × real estate, model v0.2

The Damage return for tropical-cyclone wind on the three Hazard reference profiles r1, in the fields the profile
handoff asks for: one card per profile. The worked example for the handoff is in the flood return package
(`flood_real_estate`, warehouse); §5 here is a short hurricane example. Everything is a **noncanonical proposal**
(model v0.2 / docs r1, promotion gate blocked); nothing is admitted at runtime.

## 1. Summary

| Profile | Records (one per terrain class) | Applicability |
|---|---|---|
| `re_house_1s_wood_slab` | `TCRE_RES_HAZUS_WSF1_<TERRAIN>` | qualified proxy (connections not location-specific) |
| `re_warehouse_1s_steel_slab` | `TCRE_IND_HAZUS_SPMBL_NEWDECK_<TERRAIN>` | qualified proxy (large doors not represented) |
| `re_office_3s_slab` | `TCRE_OFF_HAZUS_SECBM_<TERRAIN>` | exact match on the stated characteristics |
| house, tree fall | none | unavailable (withheld, not zero) |

Shared by all three cards:

| Item | Content |
|---|---|
| Profile pin | Hazard reference profiles **r1**, `aamani-ai/Hazard_Modeling` commit `8b0d61c88fbcf85daa1c098516cee22398cdb524`, `reference_candidates.yml` (git blob `a74fb72b0a2edce593b5505e0fd8852f4c0253f8`); source TCRE-S010 |
| Damage artifact | `tropical_cyclone_wind_real_estate` model v0.2 / docs r1, [`tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json`](tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json) (sha256 in the [validation report](VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md)), branch `cell/hurricane-wind-real-estate` of `aamani-ai/Damage_Modeling` |
| Pathway, unit | `tropical_cyclone_wind`, failure unit `TCRE_BUILDING_STRUCTURE` (contents unit withheld) |
| Demand | `tc_peak_gust_3s_10m_mph` (peak 3-s gust, 10 m, open terrain); `hazus_terrain_class` required, mapped by Hazard from site roughness, never defaulted, never applied to the gust too |
| Domain | 0–50 mph → 0 (source zero); 50–250 mph straight lines between published 5-mph points; above 250 → withheld `ABOVE_SOURCE_VALID_RANGE` |
| Output | Conditional Hazus building loss ratio for one storm, including wind pressure, windborne debris and rain ingress through wind damage; not a damage-state probability |
| Uncertainty | Point value only; variant and terrain sensitivity stated in [VARIANT_SENSITIVITY](VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv), not sampleable |
| Value | Hazus building replacement value of the same building; one assembly covering the six requested groups; covered fraction of the profile budget **not stated by the source** (Hazard's call); contents, land, site works and BI excluded |
| Overlap | No separate debris or rain-ingress response; wind and flood damage on one building in one storm together ≤ 100% of structure value (consumer) |
| Consumer probe | Hazard `damage_loader.py` (main `509bf435`): 916 of 954 known-answer requests agree, including every priced value; the differences are those of v0.1 (below-50-mph zero, withheld variants, error-code names) ([validation report](VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md) §4) |
| Reproduce | `python scripts/reference_helpers/extract_tropical_cyclone_wind_real_estate_v0_2_hazus_ordinates.py <Hazus 6.1 wind extract> <SimCenter loss_repair.csv>`; `build_tropical_cyclone_wind_real_estate_v0_2_package.py`; `validate_tropical_cyclone_wind_real_estate_v0_2_package.py` |
| Missing profile detail | None changes the type selection. **One location detail would change the house:** the local building code or design wind speed (question for Hazard, below) |

## 2. Card — `re_house_1s_wood_slab`

| Field | Content |
|---|---|
| Applicability | **Qualified proxy.** Hazus WSF1 (wood single-family, one storey, continental US) with the profile's gable roof, shingles, no garage and no shutters. Roof-deck nailing and roof-to-wall connection are unrated in the profile; the national most-common values (6d @ 6"/12", toe-nail; no secondary water resistance) are kept (D-TCRE-25) |
| Evidence | TCRE-S001 Hazus 7.0 TM (method; §9.6.5, §9.6.9 connection rules); TCRE-S002 Hazus 6.1 extract wbID 6; TCRE-S003 SimCenter copy (identical); TCRE-C006, C010, C029 |
| Values (open / suburban) | 120 mph 31.3% / 9.3%; 140 mph 77.9% / 51.2% |
| Uncertainty | Code-built connections (8d @ 6"/12" + straps): 19.0% / 5.2% at 120 mph; shutters 18.8% at 120 mph open |
| Tests | 235 house-specific known-answer tests (every published point for 5 terrains, in-between points, ranges, characteristic defaults and variants, contents withheld) plus 16 shared contract errors; all pass |
| Open | Tree fall withheld; connections by location need a code or design-wind zone per cell |

## 3. Card — `re_warehouse_1s_steel_slab`

| Field | Content |
|---|---|
| Applicability | **Qualified proxy.** Hazus SPMBL (pre-engineered metal, over 50,000 ft²; profile 100,000 ft²) with a new-or-average roof deck (profile roof age 10 years; FEMA: installed 2008 or later), no shutters, standard metal deck (most common). Hazus has no characteristic for the eight 12 × 14 ft unprotected overhead doors |
| Evidence | TCRE-S002 wbID 1730; TCRE-S003 (identical); TCRE-C008, C027, C028, C030 |
| Values (open / suburban) | 120 mph 23.5% / 5.2%; 140 mph 73.5% / 31.6% |
| Uncertainty | Old roof deck (v0.1): 39.5% / 12.7% at 120 mph; shutters 0.5% at 120 mph open; the door openings may make the class average low |
| Tests | 235 warehouse-specific known-answer tests plus the shared contract errors; all pass |

## 4. Card — `re_office_3s_slab`

| Field | Content |
|---|---|
| Applicability | **Exact match** on every characteristic the profile states: Hazus SECBM (steel engineered commercial, 3–5 storeys), single-ply membrane (TPO), medium window area (33%; FEMA 25–40%), no shutters. Windborne-debris environment (varies by direction) and standard metal deck are the most common values; parapet and rooftop units are not Hazus characteristics. A new selector, not the retail record |
| Evidence | TCRE-S001 Appendix B (SECBM 3–5 storeys), §9.6.10 (window classes); TCRE-S002 wbID 1840; TCRE-S003 (identical); TCRE-C025, C026, C030 |
| Values (open / suburban) | 120 mph 14.0% / 10.1%; 140 mph 39.3% / 32.5% |
| Uncertainty | Built-up roof 11.5%, high window area 21.7%, shutters 8.1% at 120 mph open; v0.1 commercial SECBL 8.8%. The source reads higher in light-suburban than open terrain (17.4% at 120 mph), as for SECBL |
| Tests | 234 office-specific known-answer tests plus the shared contract errors (including a profile ID sent as a selector); all pass |

## 5. Short example — office, 120 mph, suburban

```text
request  : reference_building_id = RE_COM_OFFICE_3S_SLAB, hazus_terrain_class = suburban, tc_peak_gust_3s_10m_mph = 120
record   : TCRE_OFF_HAZUS_SECBM_SUBURBAN (Hazus SECBM wbID 1840, terrain 3), published point at 120 mph
DR       : 10.1% of building value
dollars  : 0.101 × $10.8M = $1.09M, if Hazard qualifies the full budget as covered
```

## 6. Question for the Hazard team

Can Hazard supply a building-code or design-wind zone per cell? Hazus assigns house roof nailing and roof-to-wall
connections from the local code and design wind speed. With a zone per cell the house could take the code-built
variant where it applies (about 40% lower damage at 120 mph in open terrain); without it, the national most-common
values stay.
