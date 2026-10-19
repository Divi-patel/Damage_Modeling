---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Exact current request guide; validation/documentation repair without curve changes
---

# Request Wildfire × utility-scale BESS

```yaml
cell_id: wildfire_bess
consumer_pin: wildfire_bess@model_v1_0__docs_r1
damage_code_id: BESS_WILDFIRE_SCREENING_V1
artifact_schema: damage_curve_record_bundle.v3
artifact_sha256: e2d5e817c6c5334ff6176a02f2e1edbf563195254239dd9eb9be530c85cdd491
```

[Canonical curve_artifact.json](../../cells/wildfire_bess/current/curve_artifact.json) · [Runtime index](../../contracts/machine_readable_artifact_index.json).

Use pathway `wildfire_thermal_attack`, reference selector
`BESS_LFP_R1_WILDFIRE_ORDINAL_V1`, and exact `class_state` 0–6. State 0 is a
no-event control, never a substitute for missing source. Do not interpolate
classes or interpret them as local heat flux or ignition odds.

Choose `failure_unit_id` (`BESS_INTEGRATED_ENCLOSURE` or `BESS_SEPARATE_PCS`),
`response_hypothesis_id` (`approved_replacement`, `noncell_repair_sensitivity`
or `limited_repair_sensitivity`), and `shape_scenario` (`electronics_ordinal` or
`heavy_electrical_ordinal`). Repairs require literal
`assume_retained_hardware_serviceable_for_sensitivity=True`; this is a
counterfactual, not evidence that compromised cells can be repaired.

A [known answer](../../cells/wildfire_bess/current/known_answers.json) is enclosure class 4 with replacement/electronics:
DR 0.18, giving $189,000 against the $1.05M same-unit hardware value. This is a
class-conditioned mean, not measured 18% ignition odds or the repair bill for a
known compromised battery. That known endpoint retains full $1.05M replacement.
PCS keeps its electronics response under either enclosure shape. Hypotheses are
unweighted and are not uncertainty percentiles.

[Contract](../../cells/wildfire_bess/current/metadata.md), [value binding](../../cells/wildfire_bess/current/value_binding.json) and
[derivation](../../cells/wildfire_bess/current/derivation.md) govern use. Hardware coverage is $94.4M of $109.8M
full TIV; $15.4M stays unbound. Missing/invalid class and unsupported units
withhold. No frequency, intrinsic Damage spread, generic protection credit or
cross-unit propagation model is supplied. Annual metrics require qualified
Hazard exposure, declared spatial law, original support, separate unit caps and
annual distributions. Repository status grants no national, complete-property,
portfolio, insured-loss or recipient admission.
