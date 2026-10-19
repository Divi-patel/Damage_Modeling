---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: BWF-Q01 selected consequence, proposed ordinal BESS Wildfire response and finite local consumer proof
---

# BESS Wildfire: owner-selected consequence and local candidate

**BWF-Q01 is settled for local testing.** Owner, 2026-10-19: “Test full replacement;
retain repair sensitivities (Recommended)”. Test $1.05M integrated replacement
after battery thermal compromise. The $204k/$334k alternatives require serviceable
retained hardware. This ruling does not approve the class-to-damage likelihood,
empirical calibration, annual metrics, national run or canonical release.

## What changed after the ruling

| Part | State |
|---|---|
| Owner cost policy | Settled for local testing; known compromised battery endpoint is 100% of the same enclosure hardware value. |
| Ordinal response | Analyst T4 hypothesis, proposed model v0.1/docs r1; no observed BESS fragility or ignition odds inferred. |
| Repair hypotheses | Retained separately; explicit serviceability counterfactual required. |
| Value | 80 enclosure ×$1.05M +20 PCS ×$520k =$94.4M candidate hardware; $15.4M of full $109.8M unbound. |
| Current runtime/index | Unchanged; new cell has no canonical/indexed entry. |
| Annual/source deployment | Still requires separate consumer qualification. |

The [local proposal](../../../cells/wildfire_bess/proposed/local_candidate_v0_1/README.md)
contains exact-state JSON, standalone/embedded capability, value reconciliation,
sources/claims/parameters, independent known answers, SHA pins and an explicit
opt-in audit reader. Existing bundle/capability v3 schemas are unchanged.

## Proposed response and its limits

Use the existing electrical ordinal table as the simple class-response template,
with the heavy-electrical table as a distinct enclosure shape sensitivity. PCS
retains its separate electronics response. The original electrical ordinates
were economic DRs with T4 absolute anchors. Their BESS transfer is a **new T4
mean-response hypothesis**, not a source-supported conversion to battery-compromise
probability. No stochastic Damage-state sampling or intrinsic spread is created.

Why this baseline: it retains the actual six-class source, avoids invented
component heat flux/duration thresholds, costs a coherent integrated failure unit,
and makes the remaining weak transfer visible and replaceable. OEM/field evidence
constrains the mechanism and endpoint; it does not calibrate these numbers.
Neither shape is a confidence bound or guaranteed risk bound.

```text
Known battery compromise: replacement cost = $1.05M per enclosure.
Unobserved outcome at a source class:
  conditional mean = ordinal response weight × selected end-state cost.
```

For example, class 4 uses an electronics weight .18, producing $189,000 conditional
mean per enclosure under replacement. That is **not** the price of replacing an
already-compromised battery and is **not** an 18% measured ignition probability.
Serviceable-hardware repair hypotheses hold the same weight only to isolate the
economic interpretation; equal actual damage-state probabilities are not claimed.
Full reasoning and rejected alternatives are in the [derivation](../../../cells/wildfire_bess/proposed/local_candidate_v0_1/derivation.md).

## Verification and current capabilities

[The build/validation receipt](evidence/wildfire/r2/validation.json) records 84
independent Decimal/source comparisons, 19 negative response controls, one opt-in
control, three tampered payloads and ten reconciled value rows. Source/claim
references resolve; the existing source artifact and current index are unchanged.
This is numerical/contract verification, not empirical scientific validation.

The [uniform-class pressure table](../../../cells/wildfire_bess/proposed/local_candidate_v0_1/uniform_class_pressure_test.csv)
has 42 controlled cases across cost/shape hypotheses and exact states. Those
arithmetic probes are not annual losses, return-period metrics, observed events
or a map. The proposed response must retain its source/partial-property flags.

The local reader requires an exact FSim state, pathway, BESS reference selector,
response hypothesis and shape. Unknown states/units, booleans/fractions, unsupported
frequency inputs and repair without the counterfactual return no numeric result.
State0 is a no-event control, never a replacement for unavailable source data.

## Hazard handoff and finite next step

Hazard owns its content-pinned conditional reader in `perils/wildfire`, public
API exports, deployment sampling in `drivers`, and a small CLI proof. It must
not import the Damage proposal-authoring helper into production. The next proof
replays exact candidate arithmetic and real native input vectors, retaining 121
equipment units, original source meaning and unbound residuals.

Local conditional response does not imply joint fire occurrence across different
unit pixels. A separate annual proof must qualify that dependence, original unknown
mass, unique-unit caps, no restoration and EAL/AEP/OEP/fixed-mass tails before
canonical admission. Detailed propagation, calibrated thermal transfer and residual
value improvements remain BR-24–BR-26; missing proof for a complete/calibrated
claim cannot be deferred into permission for that claim.

This implements the existing curation skill. No new mandatory skill stage,
library schema or broad changes to unrelated local skill edits are needed.


### Subsequent local consumer proof

[Hazard's local proof](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/19_wildfire_local_candidate.md)
now replays 10,248 real raster fields and verifies 7,200 conditional unit means,
retaining 1,512 unbound equipment rows. Its public peril API, local CLI, 36 new
tests, installed-resource check and executed reader are complete. This qualifies
only the bounded local conditional consumer. No annual, site-hydraulic/thermal,
canonical or national capability is added to this proposal.
