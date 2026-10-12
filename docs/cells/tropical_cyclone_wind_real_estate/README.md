<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
-->

# tropical_cyclone_wind_real_estate

Current cell: **tropical-cyclone (hurricane) wind × real estate**, a new **scaffold** at semantic damage-model
`model v0.1`, documentation revision `docs r1`. It publishes **no runtime curve yet**. It is not in the artifact
index, not in a package release, and does not change any Hazard pin.

## What this cell is for

Direct physical wind damage to the **structure** of the same three reference buildings that `flood_real_estate`
prices: a single-family house, a small low-rise commercial building, and a one-story warehouse. Damage is a
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

## Status

```yaml
cell_id: tropical_cyclone_wind_real_estate
lifecycle_state: scaffold
semantic_damage_model_version: model v0.1
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

Steps 0–6 are drafted: fifteen proposed Hazus records (three buildings × five terrain classes), verified identical in
two independent copies of the Hazus database. Step 7 (artifact, capability, known-answer tests, workbook, dossier,
metadata spec, validation report) is next. Still open: owner review, the per-area replacement cost (dollars withheld),
and a terrain-class field on the Hazard side.
