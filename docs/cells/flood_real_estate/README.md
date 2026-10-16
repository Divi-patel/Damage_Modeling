<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-16
status: draft
-->

# flood_real_estate

Current cell: **flood × real estate**, a new **scaffold** whose current proposal is semantic damage-model
`model v0.2`, documentation revision `docs r1`. Model v0.1 is kept unchanged beside it (it is the revision Hazard
pinned at intake). It publishes **no runtime curve yet**. It is not in the artifact index, not in a package
release, and does not change any Hazard pin.

## What this cell is for

Direct physical flood damage to the **structure** of the buildings the real-estate CONUS screening grid will
price: the Hazard reference profiles r1 — a one-storey house, a one-storey warehouse and a three-storey office —
plus the earlier retail reference, kept but bound to no profile. Damage is a fraction of the structure's
**replacement cost new**. The curves are adopted from published US libraries (FEMA Hazus flood depth-damage
functions; USACE NACCS 2015 for retail coastal surge only). They are not derived from component evidence the way the
solar and wind cells were.

## Start here

- [Scope and cell definition (step 0/1)](proposed/README_flood_real_estate__model_v0_1__docs_r1.md)
- [Change classification](proposed/CHANGE_CLASSIFICATION_flood_real_estate__model_v0_1__docs_r1.md)
- [Decision log](proposed/DECISION_LOG_flood_real_estate__model_v0_1__docs_r1.md) (D-FRE-01 to D-FRE-28)
- [Existing-coverage check (step 2)](proposed/COVERAGE_NOTE_flood_real_estate__model_v0_1__docs_r1.md)
- [Source verification (step 3)](proposed/SOURCE_VERIFICATION_flood_real_estate__model_v0_1__docs_r1.md),
  with the [source register](proposed/SOURCE_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv) and
  [claim register](proposed/CLAIM_PARAMETER_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv) (shared by both models)
- [Evidence pressure test (step 4)](proposed/PRESSURE_TEST_flood_real_estate__model_v0_1__docs_r1.md), with the
  [parameter tier table](proposed/PARAMETER_TIER_TABLE_flood_real_estate__model_v0_1__docs_r1.csv)
- [Curve records and form (step 5)](proposed/CURVE_FORM_DECISION_flood_real_estate__model_v0_1__docs_r1.md) and the
  [candidate-curves chart](previews/flood_real_estate_v0_1_candidate_curves.png)
- [Reference buildings and value link (step 6)](proposed/REFERENCE_BUILDINGS_flood_real_estate__model_v0_1__docs_r1.md),
  [value crosswalk](proposed/VALUE_CROSSWALK_flood_real_estate__model_v0_1__docs_r1.csv),
  [seven-step audit](proposed/SEVEN_STEP_AUDIT_flood_real_estate__model_v0_1__docs_r1.md),
  [NSI sample](proposed/NSI_SAMPLE_flood_real_estate__model_v0_1__docs_r1.csv)
- Evidence after step 7:
  [NFIP claims check](proposed/NFIP_CLAIMS_CHECK_flood_real_estate__model_v0_1__docs_r1.md) (with the
  [band table](proposed/NFIP_CLAIMS_COMPARISON_flood_real_estate__model_v0_1__docs_r1.csv),
  [sensitivity table](proposed/NFIP_CLAIMS_SENSITIVITY_flood_real_estate__model_v0_1__docs_r1.csv),
  [by-storeys table](proposed/NFIP_CLAIMS_BY_STOREYS_flood_real_estate__model_v0_1__docs_r1.csv),
  [pull manifest](proposed/NFIP_CLAIMS_PULL_MANIFEST_flood_real_estate__model_v0_1__docs_r1.json) and
  [chart](previews/flood_real_estate_v0_1_nfip_claims_check.png)) and the
  [office flood research](proposed/OFFICE_FLOOD_RESEARCH_flood_real_estate__model_v0_1__docs_r1.md)

**Current package — model v0.2** (D-FRE-26 to D-FRE-28):
[curve artifact](proposed/flood_real_estate__model_v0_2__docs_r1__curve_artifact.json),
[capability](proposed/flood_real_estate__model_v0_2__docs_r1__capability.json),
[ordinates](proposed/CURVE_ORDINATES_flood_real_estate__model_v0_2__docs_r1.csv),
[known-answer tests](proposed/known_answer_tests_flood_real_estate__model_v0_2__docs_r1.json),
[workbook](proposed/damage_curve_records_flood_real_estate__model_v0_2__docs_r1.xlsx),
[derivation dossier](proposed/flood_real_estate_curve_derivation_dossier__model_v0_2__docs_r1.md),
[metadata spec](proposed/flood_real_estate_damage_code_metadata_spec__model_v0_2__docs_r1.md),
[profile binding](proposed/PROFILE_BINDING_flood_real_estate__model_v0_2__docs_r1.md) (with the
[binding table](proposed/PROFILE_BINDING_flood_real_estate__model_v0_2__docs_r1.csv) and
[floor-height sensitivity](proposed/FLOOR_HEIGHT_SENSITIVITY_flood_real_estate__model_v0_2__docs_r1.csv)),
[validation report](proposed/VALIDATION_REPORT_flood_real_estate__model_v0_2__docs_r1.md)

**Previous package — model v0.1** (kept for reproducibility):
[curve artifact](proposed/flood_real_estate__model_v0_1__docs_r1__curve_artifact.json),
[capability](proposed/flood_real_estate__model_v0_1__docs_r1__capability.json),
[ordinates](proposed/CURVE_ORDINATES_flood_real_estate__model_v0_1__docs_r1.csv),
[known-answer tests](proposed/known_answer_tests_flood_real_estate__model_v0_1__docs_r1.json),
[workbook](proposed/damage_curve_records_flood_real_estate__model_v0_1__docs_r1.xlsx),
[derivation dossier](proposed/flood_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md),
[metadata spec](proposed/flood_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md),
[validation report](proposed/VALIDATION_REPORT_flood_real_estate__model_v0_1__docs_r1.md)

## Status

```yaml
cell_id: flood_real_estate
lifecycle_state: scaffold   # draft needs owner scope acceptance (CELL_LIFECYCLE gate); capability declaration exists
semantic_damage_model_version: model v0.2   # current proposal; model v0.1 kept unchanged
released_model_version: null
promotion_status: proposed
review_status: not_yet_reviewed
documentation_revision: docs r1
documentation_status: working_revision
canonical_runtime_artifact: false
package_release: unreleased
package_inclusion_status: not_included
runtime_reason: NO_RUNTIME_CURVE
```

## Not done yet

Model v0.2 (7 records, 185 known-answer tests) passes its validator and stays out of the artifact index. House,
warehouse and office each have one FEMA Hazus record for all still water (D-FRE-28), bound to the Hazard reference
profiles r1; Hazard's common v3 loader routes them without ambiguity (validation report v0.2 §4). Still open: owner
review of the scope and selections, the return package for Hazard (one card per profile and a worked example), the
consumer's value qualification of each reference budget, the dry-ground rule and record ranges at cutover, the
office height bias and the thin warehouse coastal evidence, and the EGM document behind DF 129.
