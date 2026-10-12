<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
scope: Step 2 (map existing coverage) for flood × real estate — what the library already holds, what can be reused, what is absent, and which external material is pinned for step 3.
-->

# Existing-coverage check — flood_real_estate model v0.1 / docs r1

Checked against `main` @ `02eba9b` (2026-09-30) on 2026-10-11.

## 1. Inside this repository

| Item | Finding | Consequence |
|---|---|---|
| Real-estate or building cell | **None.** All existing cells are solar or wind. | New cell. |
| Legacy real-estate curve | `Real Estate_Hail` (legacy `hazard_analysis`) exists and was **rejected** in `hail_wind` as a mislabelled buildings/cars hail array with inconsistent units. No legacy flood real-estate array was found. | Not evidence (D-FRE-11). |
| Hazus flood manual | Already cited as `FEMA_HAZUS_FLOOD` in the archived `flood_solar` v0.1 dossier (Hazus Flood Technical Manual 6.1). | Reuse the citation; register a cell-local source ID in step 3. |
| Hazus whole-facility precedent | `flood_wind` model v1.0 releases one source-native Hazus-MH 2.1 whole-substation table as a single assembly atom, with a 0–10 ft valid range, no extrapolation, and withholding of salt or unknown water. | Template for a whole-building Hazus atom, range handling and water-type gating. |
| Flood pathway pattern | `flood_solar` and `flood_wind` both use depth-contact inundation and keep scour/velocity separate. Neither splits by flood source. | D-FRE-04, D-FRE-06. |
| Value basis | `docs/method/value_basis/solar_wind_value_breakdown.xlsx` covers solar and wind only, in $/kW. | A building replacement-cost basis ($/m²) is new work (step 6). |
| Engineering vocabulary | `substrate_decomposition.md` (source-drop context) covers solar, wind, BESS and thermal. There is no building subsystem. | Proposed codes, owner platform (D-FRE-09). |
| Schemas | `docs/contracts/schemas/*` carry no asset-type field and nothing solar- or wind-specific. | No schema change is expected for a building curve. |
| Coverage plan | `docs/plans/hazard_asset_coverage/` tracks ten solar/wind pairs, built one at a time (D-002). Real estate is not in it. | Owner decision whether to add it; noted in change classification. |

## 2. External material pinned for step 3

| Material | Location | Pin |
|---|---|---|
| Hazus flood depth-damage table | Plymouth trial branch `origin/feature/plymouth_trial` @ `09b95acb` (Hazard_Modeling), `…/feature_cache/change_log/refs/ddf/haz_fl_dept.csv`; same file in GCS `gs://flood-model-data/_asset_level_cache/plymouth_trial/raw_damage_curves/` | sha256 `863397b877aa7022d17239d527e0ea264dd9fd6431d3b6facdfbaa4add3b94a8`; md5 `9557d9ffae387cb9e058667abb6ea941` |
| NACCS 2015 depth-damage table | same branch and GCS folder, `naccs_ddfs.csv` | sha256 `58d4ffbc400ee1cb68dd2029fa3b1ac732fb8fceefb4165c91d06d8978c9568a`; md5 `7b3e15aa7f6856e2b71120c4d5e22fc8` |
| Compilation source of both tables | Pollack, A. (2023). *Flood Depth-Damage Functions from HAZUS and 2015 North Atlantic Coast Comprehensive Study.* Zenodo, DOI 10.5281/zenodo.10027236, CC-BY-4.0 | Branch, GCS and Zenodo files are byte-identical (md5 matched against the Zenodo record, 2026-10-11) |
| Hazus default-curve list | `riverine_ids.csv` in the same Zenodo record and GCS folder (stated as cross-checked against Hazus 7.0 Table 5-2) | To be confirmed against the Hazus Flood Technical Manual in step 3 |
| NACCS original report | GCS `…/raw_damage_curves/10A_PhysicalDepthDmgFxSummary_26Jan2015.pdf` | Spot-check of compiled NACCS values in step 3 (the compiled table repeats values at some depths that NACCS did not publish) |
| Prior real-estate flood work | Plymouth / Salem coastal trial: methodology trial 5 on the branch; final trial 7 / v0.7 artifacts in GCS (2026-10-05) | Method reference only: curve selection by occupancy, foundation and stories; first-floor-height convention; fit catalogue. Its curves are all with-basement and do not transfer to the reference buildings. |

## 3. What is absent and must be built

```text
source and claim registers with original-publication locators      step 3
evidence judgment, parameter tiers, pressure test                  step 4
curve records, valid ranges, form decision (linear vs smooth)      step 5
reference-building assumption table; replacement-cost value basis  step 6
curve artifact, capability declaration, KATs, validation report    step 7
```
