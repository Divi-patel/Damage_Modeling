---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Exact current request guide; validation/documentation repair without curve changes
---

# Request Flood × standalone Substation

```yaml
cell_id: flood_substation
consumer_pin: flood_substation@model_v1_0__docs_r1
damage_code_id: FLOOD_SUBSTATION_DEPTH_SCREENING_V1
artifact_schema: damage_curve_record_bundle.v3
artifact_sha256: f001eb0191439a1345a7a794995c684ef731f777c4b3e1eff0298de592999f30
```

[Canonical flood_substation__model_v1_0__docs_r1__curve_artifact.json](../../cells/flood_substation/current/flood_substation__model_v1_0__docs_r1__curve_artifact.json) · [Runtime index](../../contracts/machine_readable_artifact_index.json).

This is a source-native **whole electrical-assembly** screening response. It
supplies no independently calibrated equipment curves or response to changes in
the reference station's mounting elevations.

Supply `sub_peril` and `flood_depth_above_substation_grade_ft`, using unit
`FW_HAZUS_GSU_SUBSTATION_ASSEMBLY`. The historical prefix preserves source
lineage. Supported demand is finite grade-relative depth from 0 through 10 ft.
Do not subtract equipment elevations from this assembly axis. Same-depth
Coastal use retains the documented transfer flag; it is not a saline component
model.

A [known answer](../../cells/flood_substation/current/known_answers.json) is 3.5 ft → DR 0.065, linearly between the
source's 3 ft and 4 ft knots. Negative depths reject. Missing source or depth
above 10 ft withholds; never clamp high water to the last ordinate.

Apply the DR to the separately pinned same-station assembly value. Do not use
whole-plant TIV, capacity aliases or extra losses already inside the assembly.
Hazard owns frequency, original missing mass, annual caps and fixed-mass tails.
Damage alone emits no EAL/PML/TVaR or complete-risk result. [Consumer contract](../../cells/flood_substation/current/metadata.md)
and [derivation](../../cells/flood_substation/current/derivation.md) own the exact applicability and limits.
