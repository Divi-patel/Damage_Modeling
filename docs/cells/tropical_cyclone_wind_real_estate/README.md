<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-16
status: draft
-->

# tropical_cyclone_wind_real_estate

Current cell: **tropical-cyclone (hurricane) wind × real estate**, a new **scaffold** whose current proposal is
semantic damage-model `model v0.2`, documentation revision `docs r1`; model v0.1 is kept unchanged beside it. It publishes **no runtime curve yet**. It is not in the artifact
index, not in a package release, and does not change any Hazard pin.

## What this cell is for

Direct physical wind damage to the **structure** of the buildings that `flood_real_estate` prices: the Hazard
reference profiles r1 — a one-storey house, a one-storey warehouse and a three-storey office — plus the earlier
retail reference, kept but bound to no profile. Damage is a
fraction of the structure's **replacement cost new**. The curves are to be adopted from a published US library
(FEMA Hazus hurricane building functions), not derived from component evidence.

## Start here

- [Scope and cell definition (step 0/1)](proposed/README_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)
- [Change classification](proposed/CHANGE_CLASSIFICATION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)
- [Decision log](proposed/DECISION_LOG_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)
- [Existing-coverage check (step 2)](proposed/COVERAGE_NOTE_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)
- [Source verification (step 3)](proposed/SOURCE_VERIFICATION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md),
  with the [source register](proposed/SOURCE_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv) and
  [claim register](proposed/CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv)
- [Evidence pressure test (step 4)](proposed/PRESSURE_TEST_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md), with the
  [parameter tier table](proposed/PARAMETER_TIER_TABLE_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv) and
  [variant sensitivity](proposed/VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv)
- [Curve records and form (step 5)](proposed/CURVE_FORM_DECISION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md), with the
  [ordinates](proposed/CURVE_ORDINATES_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv) and the
  [candidate-curves chart](previews/tropical_cyclone_wind_real_estate_v0_1_candidate_curves.png)
- [Reference buildings and value link (step 6)](proposed/REFERENCE_BUILDINGS_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md),
  [value crosswalk](proposed/VALUE_CROSSWALK_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
  [seven-step audit](proposed/SEVEN_STEP_AUDIT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)
- Package (step 7): [curve artifact](proposed/tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json),
  [capability](proposed/tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__capability.json),
  [known-answer tests](proposed/known_answer_tests_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.json),
  [workbook](proposed/damage_curve_records_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.xlsx),
  [derivation dossier](proposed/tropical_cyclone_wind_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md),
  [metadata spec](proposed/tropical_cyclone_wind_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md),
  [validation report](proposed/VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)

**Current package — model v0.2** (D-TCRE-22 to D-TCRE-25):
[curve artifact](proposed/tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json),
[capability](proposed/tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__capability.json),
[ordinates](proposed/CURVE_ORDINATES_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv),
[variant sensitivity](proposed/VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv),
[known-answer tests](proposed/known_answer_tests_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.json),
[workbook](proposed/damage_curve_records_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.xlsx),
[derivation dossier](proposed/tropical_cyclone_wind_real_estate_curve_derivation_dossier__model_v0_2__docs_r1.md),
[metadata spec](proposed/tropical_cyclone_wind_real_estate_damage_code_metadata_spec__model_v0_2__docs_r1.md),
[profile binding](proposed/PROFILE_BINDING_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md) (with the [binding table](proposed/PROFILE_BINDING_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv)),
[validation report](proposed/VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md),
[**return package for Hazard**](proposed/RETURN_PACKAGE_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.md) (one card per profile)

The links above the v0.2 block are the step documents and the model-v0.1 package, kept for reproducibility.

## Status

```yaml
cell_id: tropical_cyclone_wind_real_estate
lifecycle_state: scaffold   # capability declaration exists; proposed artifact is review-only
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

Model v0.2 (20 Hazus records, 954 known-answer tests) passes its validator and stays out of the artifact index.
House, warehouse and office are bound to the Hazard reference profiles r1, and the return package for Hazard is
written. Still open: owner review of the scope and selections, the consumer's value qualification of each reference
budget, a terrain-class field on the Hazard side, a code or design-wind zone per cell for the house connections, tree
fall, and the consumer integration differences in the validation report §4.
