<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
scope: Derivation dossier for the noncanonical tropical-cyclone wind × real estate model-v0.2 proposal, following the cell dossier template; detail lives in the linked step documents. Supersedes the model-v0.1 dossier for the current proposal.
-->

# tropical_cyclone_wind_real_estate curve derivation dossier — model v0.2 / docs r1

Status: **proposed, noncanonical, not in the artifact index.** Owner review pending. Artifact:
[`tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json`](tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json).
Model v0.1 ([dossier](tropical_cyclone_wind_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md)) is kept
unchanged for reproducibility.

## What changed from model v0.1

| Change | Decision | Evidence |
|---|---|---|
| Records bound to the Hazard reference profiles r1; shared IDs with `flood_real_estate` v0.2 | D-TCRE-22 | TCRE-S010, [profile binding](PROFILE_BINDING_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md) |
| New office `RE_COM_OFFICE_3S_SLAB` = Hazus SECBM, single-ply membrane, medium window area | D-TCRE-23 | TCRE-C025, C026, C030 |
| Warehouse roof deck new or average (v0.1: old) | D-TCRE-24 | TCRE-C027, C028, C030 |
| House unchanged; code-built connections a stated sensitivity; dips allowed at any speed up to 0.005 | D-TCRE-25 | TCRE-C029, C031 |
| Retail `RE_COM_LOWRISE` unchanged (SECBL), bound to no profile | D-TCRE-15, D-TCRE-22 | — |

## 1. Scope, asset boundary, and failure mechanisms

Direct physical damage to the structure of the reference buildings (house, warehouse, three-storey office; retail
kept) from tropical-cyclone wind, as a fraction of structure replacement cost new. The Hazus loss already combines
wind pressure, windborne debris and rain entering through wind damage (D-TCRE-04). Storm surge and rainfall flooding
(`flood_real_estate`), cyclone-spawned tornadoes, tree fall (deferred), contents and business interruption are out
of scope. Detail: [scope README](README_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md).

## 2. Failure-unit decomposition and coverage

`TCRE_BUILDING_STRUCTURE` (primary, whole-building Hazus loss); `TCRE_BUILDING_CONTENTS` (withheld, deferred).

## 3. Source-native hazard axis and local exposure bridge

Peak 3-second gust at 10 m in open terrain, mph (D-TCRE-03). Terrain is a required selector with five Hazus classes,
never defaulted and never also applied to the gust (D-TCRE-06).

## 4. Source register summary

Ten sources, TCRE-S001 to S010: [source register](SOURCE_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
adding the Hazard reference profiles r1 (TCRE-S010).

## 5. Claim/parameter provenance map

Thirty-one claims, TCRE-C001 to C031: [claim register](CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv).

## 6. Evidence and legacy numerical pressure test

The v0.1 [pressure test](PRESSURE_TEST_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md) stands for house
and retail. The v0.2 [variant sensitivity](VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv),
generated from the FEMA extract and cross-checked against SimCenter, adds the office alternatives, the old warehouse
deck and the code-built house connections.

## 7. Y-axis and row-level value crosswalk

[Value crosswalk](VALUE_CROSSWALK_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv): structure replacement
cost new, 100% to one unit, shared with `flood_real_estate`. Hazus does not itemize "building"; the covered fraction
of each profile budget is returned as not stated by the source.

## 8. Site-condition adapter and double-counting matrix

Terrain is the only site condition (selector). Debris and rain ingress are inside the Hazus record: no separate
pathway. Wind and flood damage on one building in one storm together stay at or below 100% of structure value
(consumer, D-TCRE-11).

## 9. Curve-form decision

Straight lines between the published 5-mph points ([curve form decision](CURVE_FORM_DECISION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md),
D-TCRE-17); dips up to 0.005 kept at any speed (D-TCRE-25); 0 to 50 mph returns 0, above 250 mph withheld (D-TCRE-18).

## 10. Parameter derivation and tiers

Ordinates T2 (FEMA extract, identical to SimCenter's Hazus 5.1 copy). Wind characteristics: profile values where the
Hazard profile states them (office storeys, roof, windows, shutters; warehouse roof age), else the most common
(T4 assumptions from T2 frequencies).

## 11. Seven-step audit

As v0.1 ([seven-step audit](SEVEN_STEP_AUDIT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)): steps 1–6
proposed, step 7 partial (DR supportable, dollars withheld pending consumer value qualification).

## 12. Derivation rationale / combination narrative

Published FEMA Hazus building-loss tables are adopted, not derived. Each reference building takes the Hazus type and
characteristics that match its Hazard profile: where the profile states a characteristic it decides; where it does
not, the national most-common value is used and its sensitivity stated. The house's connections are left at the most
common values because Hazus assigns them by local code, which varies across the cells the house is placed in.

## 13. Capability and fail-closed decision

[Capability declaration](tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__capability.json): failure-unit DR
conditional; only the reference characteristics published (other values withheld); scenario dollars withheld; annual
and tail metrics consumer-owned; promotion gate blocked.

## 14. Open seams and update triggers

```text
- house connections by location (code, design wind)  -> Hazard supplies a code or design-wind zone per cell
- warehouse large doors                              -> a source with opening variants for metal buildings
- tree fall on the house                             -> Hazard tree data per cell
- value coverage not itemized                        -> Hazard value qualification
- terrain mapping, wind + flood combination          -> Hazard, at cutover
```

## 15. Validation/QC

[Validation report](VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md), produced by
`scripts/reference_helpers/validate_tropical_cyclone_wind_real_estate_v0_2_package.py`.
