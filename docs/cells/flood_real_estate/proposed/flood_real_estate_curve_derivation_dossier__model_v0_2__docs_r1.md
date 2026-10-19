<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
scope: Derivation dossier for the noncanonical flood × real estate model-v0.2 proposal, following the cell dossier template; detail lives in the linked step documents. Supersedes the model-v0.1 dossier for the current proposal.
-->

# flood_real_estate curve derivation dossier — model v0.2 / docs r1

Status: **proposed, noncanonical, not in the artifact index.** Owner review pending. Artifact:
[`flood_real_estate__model_v0_2__docs_r1__curve_artifact.json`](flood_real_estate__model_v0_2__docs_r1__curve_artifact.json).
Model v0.1 ([dossier](flood_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md)) is kept unchanged for
reproducibility; it is the revision Hazard pinned at intake.

## What changed from model v0.1

| Change | Decision | Evidence |
|---|---|---|
| House and warehouse use their Hazus record for coastal surge too; NACCS 5A and prototype 3 become recorded alternatives | D-FRE-28 | [NFIP claims check](NFIP_CLAIMS_CHECK_flood_real_estate__model_v0_1__docs_r1.md) |
| New office selector `RE_COM_OFFICE_3S_SLAB` with Hazus DF 431 for both water types | D-FRE-27, D-FRE-28 | [office flood research](OFFICE_FLOOD_RESEARCH_flood_real_estate__model_v0_1__docs_r1.md) |
| Retail record `RE_COM_LOWRISE` unchanged and bound to no profile | D-FRE-26 | [profile binding](PROFILE_BINDING_flood_real_estate__model_v0_2__docs_r1.md) |
| Records bound to the Hazard reference profiles r1 | D-FRE-26 | profile binding |

## 1. Scope, asset boundary, and failure mechanisms

Direct physical damage to the structure of the reference buildings (house, warehouse, three-storey office; retail
kept) from still floodwater, as a fraction of structure replacement cost new. Contents, land, site works,
business interruption and wave/velocity damage are out of scope.
Detail: [scope README](README_flood_real_estate__model_v0_1__docs_r1.md) §1–2; targets: Hazard reference profiles r1
(FRE-S013).

### 1A. Pathway architecture

One built pathway, `flood_inundation_contact` (riverine, pluvial and coastal still water). `flood_wave_velocity`
is declared and deferred (withheld, not zero). Water type is an event conditioner; it routes records only for
retail (D-FRE-04 to -06, D-FRE-28).

## 2. Failure-unit decomposition and coverage

`FRE_BUILDING_STRUCTURE` (primary, whole-building source atom); `FRE_BUILDING_CONTENTS` (withheld, deferred).

## 3. Source-native hazard axis and local exposure bridge

Depth above the first finished floor, in feet. Bridge: depth above grade minus first-floor height (house 0.75 ft;
retail, warehouse and office 0.25 ft; D-FRE-22). Depth above grade of 0 or less is not inundated (D-FRE-24); a
consumer sending floor-relative depth applies that rule itself ([profile binding](PROFILE_BINDING_flood_real_estate__model_v0_2__docs_r1.md) §3).

## 4. Source register summary

Thirteen sources, FRE-S001 to S013: [source register](SOURCE_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv),
adding the NFIP claims (FRE-S012) and the Hazard reference profiles (FRE-S013) to the v0.1 set.

## 5. Claim/parameter provenance map

Thirty-seven claims, FRE-C001 to C037: [claim register](CLAIM_PARAMETER_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv).

## 6. Evidence and legacy numerical pressure test

The v0.1 [pressure test](PRESSURE_TEST_flood_real_estate__model_v0_1__docs_r1.md) proposed NACCS for coastal surge; the
[NFIP claims check](NFIP_CLAIMS_CHECK_flood_real_estate__model_v0_1__docs_r1.md) tested it against paid claims and the
coastal choice was changed (D-FRE-28). The office candidates and the height effect are in the
[office flood research](OFFICE_FLOOD_RESEARCH_flood_real_estate__model_v0_1__docs_r1.md).

## 7. Y-axis and row-level value crosswalk

[Value crosswalk](VALUE_CROSSWALK_flood_real_estate__model_v0_1__docs_r1.csv): structure replacement cost new, 100% to
one unit. The sources do not itemize "structure"; the covered fraction of each profile budget is returned as not
stated by the source (D-FRE-26).

## 8. Site-condition adapter and double-counting matrix

[Seven-step audit](SEVEN_STEP_AUDIT_flood_real_estate__model_v0_1__docs_r1.md) step 6: first-floor height in the bridge
only; no protection credit; retail libraries never blended; waves withheld.

## 9. Curve-form decision

Straight lines between published points ([curve form decision](CURVE_FORM_DECISION_flood_real_estate__model_v0_1__docs_r1.md),
D-FRE-20); below the published range 0, above withheld (D-FRE-21). DF 431 uses the same form.

## 10. Parameter derivation and tiers

[Parameter tier table](PARAMETER_TIER_TABLE_flood_real_estate__model_v0_1__docs_r1.csv): ordinates T2 with transfer
limits; first-floor heights T2 (house) and T3 (others); coastal use of the Hazus records rests on T1 claims comparison
(not calibration).

## 11. Seven-step audit

As v0.1: steps 1–6 proposed, step 7 partial (DR supportable, dollars withheld pending consumer value
qualification).

## 12. Derivation rationale / combination narrative

Published agency tables are adopted, not derived. For house, warehouse and office, the Hazus default for the
occupancy serves all still water: NFIP coastal-surge claims are closer to it than to the NACCS prototypes, and FEMA
assigns the commercial defaults to coastal zones itself. The office curve is FEMA's COM4 default as published; its
height bias is recorded, not corrected. Retail keeps Hazus for freshwater and NACCS for coastal surge, never blended.
No smoothing, blending, uplift or extrapolation is applied.

## 13. Capability and fail-closed decision

[Capability declaration](flood_real_estate__model_v0_2__docs_r1__capability.json): failure-unit DR conditional;
scenario dollars withheld; NACCS bounds only for the retail coastal record; annual and tail metrics consumer-owned
and withheld; promotion gate blocked pending owner review.

## 14. Open seams and update triggers

```text
- coastal use of riverine curves (house, warehouse, office) -> coastal claims from outside the Gulf, wave-zone study
- office height bias (about x1.6 on 3+ floor claims)       -> height-specific commercial curves or office claims
- warehouse coastal (14 claims)                             -> more coastal warehouse evidence
- value coverage not itemized                               -> Hazard value qualification
- commercial / industrial first-floor default (T3)          -> NSI documentation
- wave / velocity pathway                                   -> Hazard wave inputs and curated curves
- consumer integration (ranges, retail routing, dry rule)   -> Hazard, at cutover
```

## 15. Validation/QC

[Validation report](VALIDATION_REPORT_flood_real_estate__model_v0_2__docs_r1.md), produced by
`scripts/reference_helpers/validate_flood_real_estate_v0_2_package.py`.
