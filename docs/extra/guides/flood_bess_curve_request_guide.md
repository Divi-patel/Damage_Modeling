---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Exact current request guide; validation/documentation repair without curve changes
---

# Request Flood × utility-scale BESS

```yaml
cell_id: flood_bess
consumer_pin: flood_bess@model_v1_0__docs_r1
damage_code_id: BESS_FLOOD_INUNDATION_SCREENING_V1
artifact_schema: damage_curve_record_bundle.v2
artifact_sha256: c9bc9194accb3adbc2c05a9720b4945dd5a969bd7288eb600d5e901aa0185d24
```

[Canonical curve_artifact.json](../../cells/flood_bess/current/curve_artifact.json) · [Runtime index](../../contracts/machine_readable_artifact_index.json).

Use the grouped response for the selected outdoor LFP reference and its **same
covered hardware values**. An active-enclosure DR of one is not 100% of an
entire enclosure or plant. Read [value binding](../../cells/flood_bess/current/value_binding.json); residual property
cannot be redistributed into the covered units.

Supply a unique physical instance, `unit_kind` (`battery_enclosures` or `pcs`),
finite nonnegative local-grade `depth_m`, explicit `water_condition`
(`freshwater_screening` or `saline_screening`), and policy
`BESS_FLOOD_SCREENING_V1`. Apply the assumed 0.30 m entry once. Freshwater
battery response is binary strictly above entry; PCS retains its depth-shape
proxy above entry. Saline covered hardware replacement is binary strictly above
entry. High-depth response saturates only at that unit's covered value.

[Known answers](../../cells/flood_bess/current/known_answers.json) include enclosure depth 0.30 m → DR 0 and
0.3000001 m → DR 1. Use the declared state bridge; a generic continuous evaluator
must not interpolate across that binary transition. Unknown chemistry or missing
depth withholds instead of selecting a default or safe zero.

The [contract](../../cells/flood_bess/current/metadata.md) and [derivation](../../cells/flood_bess/current/derivation.md) govern source and
value. Annual use requires Hazard's qualified frequency, common event, fixed
location, original missing mass, separate unit caps and annual tails. The
current capability governs annual admission; historical conditional KAT wording
does not supersede it. No autonomous event, wave/scour/debris, BI or complete-
property response is added.
