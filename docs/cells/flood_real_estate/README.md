<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
-->

# flood_real_estate

Current cell: **flood × real estate**, a new **scaffold** at semantic damage-model `model v0.1`, documentation
revision `docs r1`. It publishes **no runtime curve yet**. It is not in the artifact index, not in a package
release, and does not change any Hazard pin.

## What this cell is for

Direct physical flood damage to the **structure** of three reference buildings that the real-estate CONUS
screening grid will price: a single-family house, a small low-rise commercial building, and a one-story
warehouse. Damage is a fraction of the structure's **replacement cost new**. The curves are adopted from
published US libraries (FEMA Hazus flood depth-damage functions, USACE NACCS 2015). They are not derived from
component evidence the way the solar and wind cells were.

## Start here

- [Scope and cell definition (step 0/1)](proposed/README_flood_real_estate__model_v0_1__docs_r1.md)
- [Change classification](proposed/CHANGE_CLASSIFICATION_flood_real_estate__model_v0_1__docs_r1.md)
- [Decision log](proposed/DECISION_LOG_flood_real_estate__model_v0_1__docs_r1.md)
- [Existing-coverage check (step 2)](proposed/COVERAGE_NOTE_flood_real_estate__model_v0_1__docs_r1.md)
- [Source verification (step 3)](proposed/SOURCE_VERIFICATION_flood_real_estate__model_v0_1__docs_r1.md),
  with the [source register](proposed/SOURCE_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv) and
  [claim register](proposed/CLAIM_PARAMETER_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv)
- [Evidence pressure test (step 4)](proposed/PRESSURE_TEST_flood_real_estate__model_v0_1__docs_r1.md), with the
  [parameter tier table](proposed/PARAMETER_TIER_TABLE_flood_real_estate__model_v0_1__docs_r1.csv)

## Status

```yaml
cell_id: flood_real_estate
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

Steps 3–4 are drafted: Hazus Table 5-2 is confirmed and three curve selections are proposed. Two source items stay
pending (NSI defaults, EGM document). Steps 5–7 of the Damage Core lifecycle remain: curve records and form, value
link, curve artifact, capability declaration, known-answer tests, and validation.
