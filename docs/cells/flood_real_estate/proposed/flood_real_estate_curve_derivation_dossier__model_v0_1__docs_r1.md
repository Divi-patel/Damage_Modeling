<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
scope: Derivation dossier for the noncanonical flood × real estate model-v0.1 proposal, following the cell dossier template; detail lives in the linked step documents.
-->

# flood_real_estate curve derivation dossier — model v0.1 / docs r1

Status: **proposed, noncanonical, not in the artifact index.** Owner review pending. Artifact:
[`flood_real_estate__model_v0_1__docs_r1__curve_artifact.json`](flood_real_estate__model_v0_1__docs_r1__curve_artifact.json).

## 1. Scope, asset boundary, and failure mechanisms

Direct physical damage to the structure of three reference buildings (house, small low-rise commercial, one-story
warehouse) from still floodwater, as a fraction of structure replacement cost new. Contents, land, site works,
business interruption and wave/velocity damage are out of scope.
Detail: [scope README](README_flood_real_estate__model_v0_1__docs_r1.md) §1–2.

### 1A. Pathway architecture

One built pathway, `flood_inundation_contact` (riverine, pluvial and coastal still water). `flood_wave_velocity`
is declared and deferred (withheld, not zero). Flood source is not a pathway; water type is a conditioner
(D-FRE-04 to -06).

## 2. Failure-unit decomposition and coverage

`FRE_BUILDING_STRUCTURE` (primary, whole-building source atom); `FRE_BUILDING_CONTENTS` (withheld, deferred).
Subsystem and component codes are proposals awaiting platform codes (D-FRE-09).

## 3. Source-native hazard axis and local exposure bridge

Depth above the first finished floor, in feet (both libraries). Bridge: depth above grade minus first-floor height
(NSI 2026 defaults 0.75 / 0.25 / 0.25 ft, D-FRE-22). Depth above grade of 0 or less is not inundated (D-FRE-24).

## 4. Source register summary

Eleven sources, FRE-S001 to S011: [source register](SOURCE_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv).
Spine: FEMA Hazus 7.0 Table 5-2 defaults and USACE NACCS 2015 tables; working data via Pollack (2023); integrity
confirmed against the NACCS report, USACE `go-consequences`, and the FEMA Hazus 6.1 extract
([source verification](SOURCE_VERIFICATION_flood_real_estate__model_v0_1__docs_r1.md)).

## 5. Claim/parameter provenance map

Twenty-five claims, FRE-C001 to C025: [claim register](CLAIM_PARAMETER_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv).

## 6. Evidence and legacy numerical pressure test

[Pressure test](PRESSURE_TEST_flood_real_estate__model_v0_1__docs_r1.md): proposed selections, the freshwater vs
coastal library gap (not adjusted), and the FEMA DF 658 coastal alternative. Legacy `Real Estate_Hail` rejected
(D-FRE-11).

## 7. Y-axis and row-level value crosswalk

[Value crosswalk](VALUE_CROSSWALK_flood_real_estate__model_v0_1__docs_r1.csv): structure replacement cost new,
100% to one unit; per-area cost open (D-FRE-23).

## 8. Site-condition adapter and double-counting matrix

[Seven-step audit](SEVEN_STEP_AUDIT_flood_real_estate__model_v0_1__docs_r1.md) step 6: first-floor height in the
bridge only; no protection credit; libraries never blended; waves withheld.

## 9. Curve-form decision

Straight lines between published points ([curve form decision](CURVE_FORM_DECISION_flood_real_estate__model_v0_1__docs_r1.md),
D-FRE-20); below the published range 0, above withheld (D-FRE-21).

## 10. Parameter derivation and tiers

[Parameter tier table](PARAMETER_TIER_TABLE_flood_real_estate__model_v0_1__docs_r1.csv): ordinates T2 with transfer
limits; first-floor heights T2 (house) and T3 (commercial, warehouse); water-type routing T3; value per area and the
library gap are open seams.

## 11. Seven-step audit

Steps 1–6 proposed, step 7 partial (DR supportable, dollars withheld):
[seven-step audit](SEVEN_STEP_AUDIT_flood_real_estate__model_v0_1__docs_r1.md).

## 12. Derivation rationale / combination narrative

Published agency tables are adopted, not derived: the Hazus default per occupancy for freshwater and the matching
NACCS prototype for coastal surge, each kept separate. No smoothing, blending, uplift or extrapolation is applied.
First-floor heights follow NSI 2026 so one national rule serves both water types.

## 13. Capability and fail-closed decision

[Capability declaration](flood_real_estate__model_v0_1__docs_r1__capability.json): failure-unit DR conditional;
scenario dollars withheld; NACCS bounds emitted as a non-probabilistic building-variant envelope; annual and tail
metrics consumer-owned and withheld; promotion gate blocked pending owner review.

## 14. Open seams and update triggers

```text
- freshwater vs coastal library gap                 -> NFIP claims comparison
- per-area replacement cost new                      -> owner selects a source (D-FRE-23)
- commercial / industrial first-floor default (T3)   -> NSI documentation
- wave / velocity pathway                            -> Hazard wave inputs and curated curves
- platform codes and routing                         -> platform team
- consumer integration (record ranges, water routing)-> Hazard, at cutover (validation report §4)
```

## 15. Validation/QC

[Validation report](VALIDATION_REPORT_flood_real_estate__model_v0_1__docs_r1.md), produced by
`scripts/reference_helpers/validate_flood_real_estate_v0_1_package.py`.
