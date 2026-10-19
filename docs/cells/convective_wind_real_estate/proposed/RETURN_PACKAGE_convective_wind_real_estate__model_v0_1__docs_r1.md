<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-19
status: draft
-->

# Return package for Hazard — convective wind × real estate, model v0.1

The Damage return for convective wind (straight-line wind and tornado) on the three Hazard reference profiles r1,
in the fields the profile handoff asks for: one card per profile, both pathways on each card. Everything is a
**noncanonical proposal** (model v0.1 / docs r1, promotion gate blocked); nothing is admitted at runtime. The binding
table is [PROFILE_BINDING](PROFILE_BINDING_convective_wind_real_estate__model_v0_1__docs_r1.csv).

## 1. Summary

| Profile | Straight-line record | Tornado record | Applicability |
|---|---|---|---|
| `re_house_1s_wood_slab` | `CWRE_RES_EF_FR12_STRAIGHT_LINE_ONSET96` | `CWRE_RES_EF_FR12_TORNADO` | tornado exact match (EF FR12); straight-line qualified proxy (T4 transfer) |
| `re_warehouse_1s_steel_slab` | `CWRE_IND_EF_MBS_STRAIGHT_LINE_ONSET96` | `CWRE_IND_EF_MBS_TORNADO` | tornado exact match (EF MBS); straight-line qualified proxy |
| `re_office_3s_slab` | `CWRE_OFF_EF_LRB_STRAIGHT_LINE_ONSET96` | `CWRE_OFF_EF_LRB_TORNADO` | tornado exact match (EF LRB); straight-line qualified proxy |

Shared by all three cards:

| Item | Content |
|---|---|
| Profile pin | Hazard reference profiles **r1**, `aamani-ai/Hazard_Modeling` commit `8b0d61c88fbcf85daa1c098516cee22398cdb524`, `reference_candidates.yml` (git blob `a74fb72b0a2edce593b5505e0fd8852f4c0253f8`); source CWRE-S004 |
| Damage artifact | `convective_wind_real_estate` model v0.1 / docs r1, [`convective_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json`](convective_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json) (sha256 in the [validation report](VALIDATION_REPORT_convective_wind_real_estate__model_v0_1__docs_r1.md)), branch `cell/convective-wind-real-estate` of `aamani-ai/Damage_Modeling` |
| Pathways, unit | `straight_line_convective` and `tornado_direct_hit`; failure unit `CWRE_BUILDING_STRUCTURE` (contents withheld) |
| Demand | Straight-line: `convective_gust_3s_10m_mph` (ASCE 7-22 3-s gust, 10 m, Exposure C, as delivered). Tornado: `tornado_gust_3s_10m_mph` (Hazard's EF band midpoint gust accepted, flagged as damage-inferred). No terrain class; no bridge in Damage; EF ratings are not inputs |
| Domain | 0–255 mph straight lines between 1-mph knots; straight-line zero at or below 96 mph; above 255 → withheld `ABOVE_SOURCE_VALID_RANGE`; negative → error |
| Output | Conditional expected repair cost / structure replacement cost new for one event, from the EF degrees of damage priced through the FEMA Hazus damage states; not a damage-state probability |
| Uncertainty | Point value only; cost, spread and onset sensitivity in [SENSITIVITY](SENSITIVITY_convective_wind_real_estate__model_v0_1__docs_r1.csv), not sampleable |
| Value | Structure replacement cost new of the same building (shared with flood and hurricane); covered fraction of the profile budget not stated by the source (Hazard's call); contents, land, site works and BI excluded |
| Overlap | One pathway per event; a TC-spawned tornado in one cell only; all perils on one building in one event ≤ 100% of structure value (consumer) |
| Consumer probe | Hazard `damage_loader.py` (main `f19c604`, blob `4bdadaa1`): 160 of 166 known-answer requests agree, including every priced and withheld value; the six differences are error-code names ([validation report](VALIDATION_REPORT_convective_wind_real_estate__model_v0_1__docs_r1.md) §4) |
| Reproduce | `derive_convective_wind_real_estate_ef_curves.py`; `build_convective_wind_real_estate_v0_1_package.py`; `convective_wind_real_estate_profile_binding.py`; `validate_convective_wind_real_estate_v0_1_package.py` |
| Missing profile detail | None changes the indicator choice |

## 2. Card — `re_house_1s_wood_slab`

| Field | Content |
|---|---|
| Applicability | EF **FR12** (one- and two-family residences, 1,000–5,000 ft²) for the one-storey 1,800 ft² wood house. Tornado: exact match. Straight-line: qualified proxy (tornado evidence transferred, onset 96 mph) |
| Evidence | CWRE-S001 (WSEC 2006, FR12 table), S002 (SPC), S003 (Hazus damage states, Table 5-44); CWRE-C003, C007, C010 |
| Values (straight-line / tornado) | 100 mph 2.0% / 7.9%; 120 mph 31.8% / 35.9%; 140 mph 83.4% / 84.4% |
| Uncertainty | "Shifted off foundation" priced as Complete instead of Extensive: 48% / 52% at 120 mph. Bounds read as 68% instead of 90%: 35% / 41% at 120 mph |
| Open | Foundation shift kept at Extensive (50%) for now (JL, D-CWRE-07), Complete as sensitivity; onset fixed, not by location |

## 3. Card — `re_warehouse_1s_steel_slab`

| Field | Content |
|---|---|
| Applicability | EF **MBS** (metal building systems; examples warehouses; large overhead doors) for the one-storey steel warehouse with eight overhead doors. Tornado: exact match. Straight-line: qualified proxy |
| Evidence | CWRE-S001 (MBS table), S002, S003 (Table 5-74); CWRE-C004, C008, C010 |
| Values (straight-line / tornado) | 100 mph 2.7% / 9.7%; 120 mph 30.8% / 35.7%; 140 mph 66.9% / 69.2% |
| Uncertainty | Light-damage costs halved or doubled: within 1 point at 120 mph. The EF indicator fails column anchorage and purlins near 117 mph, so this building rises earlier than in the hurricane curves |

## 4. Card — `re_office_3s_slab`

| Field | Content |
|---|---|
| Applicability | EF **LRB** (low-rise building, 1–4 storeys; examples office buildings; steel frame; single-ply roof) for the three-storey steel office with a TPO roof. Tornado: exact match. Straight-line: qualified proxy |
| Evidence | CWRE-S001 (LRB table), S002, S003 (Table 5-78); CWRE-C005, C009, C010 |
| Values (straight-line / tornado) | 100 mph 1.3% / 5.7%; 120 mph 11.3% / 15.3%; 140 mph 35.1% / 38.1% |
| Uncertainty | The office reaches about 50% by 160 mph and about 75% at 190 mph; its last EF degree ("complete destruction", 188 mph expected) carries half the cost, so full loss comes only above about 220 mph |

## 5. Short example — warehouse, straight-line, 120 mph

```text
request  : pathway_id = straight_line_convective, reference_building_id = RE_IND_WAREHOUSE,
           failure_unit_id = CWRE_BUILDING_STRUCTURE, convective_gust_3s_10m_mph = 120
record   : CWRE_IND_EF_MBS_STRAIGHT_LINE_ONSET96 (knot at 120 mph)
DR       : 30.8% of structure value
dollars  : 0.308 × $11.0M = $3.39M, if Hazard qualifies the full budget as covered
```

## 6. Items for the Hazard team

From the [NRI check](convective_wind_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md) (§13):

1. **Straight-line frequency.** Yearly straight-line building loss is 13–35 times NRI even with the onset. Hazard's
   straight-line rate (0.66 events a year at or above 58 mph in the median cell) is extrapolated below ASCE's lowest
   published level, the 10-year gust.
2. **Tornado hit geometry.** Tornado loss is 0.11–0.26 times NRI with an almost identical ranking; national median path
   sizes (EF1: 2.4 km × 55 m) make hits rare.
3. **Coastal overlap.** ASCE gust maps near the coast include hurricane winds; the same wind must not be priced by
   both the convective and the hurricane cell.
4. **Design gust per cell (optional).** A per-cell design gust would allow a location-specific onset; nationally it
   gives the same result as the fixed 96 mph.
