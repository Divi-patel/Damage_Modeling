<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
scope: Step 2 (map existing coverage) for tropical-cyclone wind × real estate — what the library and the Hazard consumer already hold, what can be reused, what is absent, and which external material step 3 needs.
-->

# Existing-coverage check — tropical_cyclone_wind_real_estate model v0.1 / docs r1

Checked on 2026-10-12 against Damage `main` @ `02eba9b`, the pushed flood branch
`origin/cell/flood-real-estate` @ `bc27524`, and Hazard `origin/main` @ `e8664800`.

## 1. Inside this repository

| Item | Finding | Consequence |
|---|---|---|
| Real-estate or building wind cell | **None.** All released cells are solar or wind. `flood_real_estate` (proposed, unmerged branch) is the only building cell. | New cell. |
| Reference buildings | `flood_real_estate` defines `RE_RES_SFD_1S_SLAB`, `RE_COM_LOWRISE`, `RE_IND_WAREHOUSE`, with roof cover and opening protection recorded "for hail and wind". | Reused unchanged (D-TCRE-02). |
| Hurricane axis convention | `tropical_cyclone_wind_wind` v1.2 uses `tc_peak_gust_3s_10m_kmh` (3-s gust, 10 m), rejects Saffir-Simpson category and one-minute sustained wind as inputs, and applies no height, averaging or terrain bridge. `tropical_cyclone_wind_solar` v2.1 uses a gust/design-gust ratio. | Same gust basis; unit mph to match Hazard (D-TCRE-03). |
| Pathway convention | Both sibling cells use `pathway_id: tropical_cyclone_wind` and exclude debris, rain ingress, surge, rainfall flood and TC-spawned tornado, keeping one `event_family_id` for compound events. | Same pathway ID; debris and rain ingress handled differently because the building source embeds them (D-TCRE-04). |
| Hazus hurricane source | **None in the library.** No Hazus hurricane building type (WSF, MLRM, SECB, SPMB …) or Vickery building-model reference appears in any cell. The only Vickery hit is `TCWW-S012` (Mudd & Vickery 2023, offshore wind axis bridge). | Step 3 must register the Hazus hurricane sources from scratch. |
| Whole-facility Hazus precedent | `flood_wind` releases one source-native Hazus substation atom; `flood_real_estate` proposes whole-building Hazus/NACCS records. | Template for a whole-building Hazus record and its range handling. |
| Value basis | `solar_wind_value_breakdown.xlsx` covers solar and wind only. `flood_real_estate` sets structure replacement cost new as the denominator and leaves the per-area cost open. | Shared basis and shared open seam (D-TCRE-09). |
| Engineering vocabulary | No building subsystem (standard 24). | Same proposed codes as `flood_real_estate`. |

## 2. Legacy numerical audit

The legacy `hazard_analysis` library (local copy `~/Desktop/hazards-05-27-dev/hazards`, commit `9bc9c30`,
2026-06-12; `tools/damage_curves/data/damage_curves_data.csv`, sha256
`add6f1c75fad7ec98bc49344ca277c896927ded626eb7ed0b89ed665d17b1138`) holds two real-estate wind arrays:

| Legacy curve | Metadata citation | Defects | Disposition |
|---|---|---|---|
| `hurricane_tropical_cyclone_wind_storm_residential` | "Climada" with a Google-Sheets link (`damage_curves_metadata.csv:4`) | Wind in m/s with no averaging period, height or terrain; no building type; saturates near 37% at 120 m/s; 5 m/s grid; anchored-logistic refit exists | **Not evidence** (D-TCRE-10). |
| `strong_wind_small_residential` | Unanwa et al. (`damage_curves_metadata.csv:7`) | Straight-line wind, not tropical cyclone; neighbouring convective-wind cell | Out of scope; not evidence for this cell. |

The `Real Estate_Hail` array rejected in `hail_wind` is unrelated to wind and is not used. Obsolete curve files in
`~/Downloads` (metadata/flattened CSVs, master index, Climada workbook, catalogue) are not used.

## 3. The consumer (Hazard)

| Item | Finding (Hazard `origin/main` @ `e8664800`) |
|---|---|
| Delivered intensity | 3-second peak gust at 10 m, mph (`docs/hazards/hurricane/fundamentals.md:10-14, 64-71`). |
| Source and bridge | STORM present-day return-period rasters, 10-minute sustained wind at 10 m; U3s = U10min × (1/0.88) × 1.20 (`perils/hurricane/src/hurricane/storm_return_periods.py:22-46`). Applied in the asset builders, not in M1. |
| Delivered range | STORM thresholds 20–75 m/s → about 61–229 mph. Below 20 m/s is "below support", not zero. |
| Terrain | Open terrain (Exposure C); no roughness adjustment. |
| Frequency object | Return-period based; no event catalog and no storm identity, so a same-storm wind + surge join is not possible today. |
| Sub-perils | Hurricane = wind only; surge → Flood Coastal; rainfall → Flood Pluvial. |
| Curve loading | Solar and wind-farm loaders are cell-specific (`perils/hurricane/src/hurricane/damage_v21.py`, `damage_wind.py`). The generic bundle-v3 evaluator (`drivers/deep/src/deep/damage_loader.py:230-466`) picks a record by unique selector match and checks one pathway-level `hazard_axis.valid_range` on `preferred_input_field`. |
| Real-estate assets | None in hurricane code or docs. |

**Routing consequence (for step 7).** The current generic loader routes by selectors only and checks one range per
pathway. If curve records differ by more than the reference building (wind characteristics, terrain), each such
field must be a declared selector, and every record must share the pathway's valid range — or the integration
gap is recorded, as `flood_real_estate` did in its validation report §4.

## 4. External material needed for step 3

| Material | Where | Status |
|---|---|---|
| FEMA Hazus Hurricane Model Technical Manual (6.1, or 7.x if published) | FEMA Hazus documentation page | **Manual download by JL needed** (FEMA returns HTTP 403 to scripts). Not on disk: `~/Downloads` holds the Hazus 7.1 patch notes and the earthquake 6.1 manual only. |
| `HazusWindDamFunctions_Hazus61.xlsx` | FEMA-provided extract mirrored by OS-Climate physrisk (public bucket `os-climate-physical-risk/vulnerability/`); physrisk documents it as "an extract of the damage functions used in the Hazus 6.1 Hurricane Model" provided by the FEMA Hazus team | **JL's go-ahead needed** before download (third-party mirror). If used: verify against the manual and record as a mirror of a FEMA-provided file, as `flood_real_estate` did for the flood extract. |
| Building-type and wind-characteristic definitions, default characteristic mixes | Hazus Hurricane TM (building classification chapter) and Hazus Inventory TM | To read in step 3. |
| Independent check of the Hazus functions | e.g. Vickery et al. 2006 (Natural Hazards Review, HAZUS-MH hurricane model papers), FEMA loss-avoidance studies, published Hazus validation against claims | Bounded search in step 3. |

## 5. What is absent and must be built

```text
source and claim registers with original-publication locators      step 3
evidence judgment, parameter tiers, pressure test                  step 4
curve records, valid range, form decision                          step 5
wind-characteristic and terrain assumptions; shared value basis    step 6
curve artifact, capability declaration, KATs, validation report    step 7
```
