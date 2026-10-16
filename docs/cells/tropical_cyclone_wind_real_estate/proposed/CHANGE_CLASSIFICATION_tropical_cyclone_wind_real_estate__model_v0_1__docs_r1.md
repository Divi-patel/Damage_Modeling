<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-16
status: draft
-->

# Change classification — tropical_cyclone_wind_real_estate model v0.1 / docs r1

```yaml
change_class: NEW_CELL_SCAFFOLD
cell_id: tropical_cyclone_wind_real_estate
operating_mode: inside_repo
outputs_can_change_for_same_inputs: false   # no runtime output exists
primary_workflow: docs/extra/damage_curve_skill/01_workflows/ADD_NEW_CELL_WORKFLOW.md
version_impacts:
  package_release: none
  cell_model_version: new cell starts at model v0.1
  docs_revision: docs r1
  schema_version: none
required_gates:
  - scope accepted by JL before any curve record is promoted beyond proposed
  - source and claim registers with exact locators (step 3)
  - evidence pressure test and parameter tiers (step 4)
  - curve records, form decision and known-answer tests (steps 5 and 7)
  - value crosswalk sharing the flood_real_estate replacement-cost basis (step 6)
explicit_non_changes:
  - no machine-readable artifact-index entry
  - no runtime package inclusion
  - no contract-schema edit
  - no VERSION_REGISTRY edit
  - no change to any existing cell (flood_real_estate, tropical_cyclone_wind_solar, tropical_cyclone_wind_wind)
  - no Hazard M3 or M4 edit
  - no stable src API
reviewer_notes:
  - Second real-estate cell, after flood_real_estate. Same three reference buildings and value basis.
  - Adopts published whole-building curves (FEMA Hazus hurricane) rather than deriving component curves,
    following the flood_real_estate and flood_wind source-native precedent.
  - The pathway keeps the cell name of its siblings (pathway_id tropical_cyclone_wind) but, unlike them,
    contains the source-embedded debris and rain-ingress damage (scope §4, D-TCRE-04).
  - Real estate is outside the ten-pair hazard × asset coverage plan; adding it is an owner decision.
related_change_events: []
```

## Why this is not a model release

Step 7 added a **noncanonical** bundle-v3 artifact with fifteen proposed curve records, a capability declaration
(promotion gate blocked) and 719 known-answer tests. None of it is in the artifact index, version registry or a
`current/` package, so no runtime behaviour changes and the class stays `NEW_CELL_SCAFFOLD`. A
`NEW_CELL_MODEL_RELEASE` needs owner acceptance, a selected value basis for dollars, a Hazard terrain input,
independent review and a deliberate consumer cutover (validation report §4).

## Model v0.2 (2026-10-16)

```yaml
change_class: MODEL_VERSION_BUMP_WITHIN_PROPOSAL
cell_model_version: model v0.1 -> model v0.2 (v0.1 package kept unchanged)
docs_revision: docs r1
why_a_model_bump: a new selector (office) and a changed warehouse record change runtime output, per the Damage
  release guide (parameter / curve / runtime behavior change)
decisions: [D-TCRE-22, D-TCRE-23, D-TCRE-24, D-TCRE-25]
explicit_non_changes:
  - still no artifact-index, version-registry, package or contract-schema edit
  - no change to any other cell; no Hazard edit (the common loader was only probed, read-only)
  - shared registers keep their docs-r1 file names; v0.1 extractor, builder, validator and outputs reproduce unchanged
```
