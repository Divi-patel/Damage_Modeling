---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Exact current request guide; validation/documentation repair without curve changes
---

# Request Hurricane × utility-scale BESS

```yaml
cell_id: tropical_cyclone_wind_bess
consumer_pin: tropical_cyclone_wind_bess@model_v1_0__docs_r1
damage_code_id: BESS_TC_WIND_SCREENING_V1
artifact_schema: damage_curve_record_bundle.v3
artifact_sha256: 0a99b2f0efbe1628d1f0500e0801a24251cab9d3bc7c22f32de0a5c758945fed
```

[Canonical curve_artifact.json](../../cells/tropical_cyclone_wind_bess/current/curve_artifact.json) · [Runtime index](../../contracts/machine_readable_artifact_index.json).

Use pathway `tropical_cyclone_wind` and failure unit
`BESS_INTEGRATED_ENCLOSURE` or `BESS_SEPARATE_PCS`. Comparable 3-second event and
reference gusts give pressure ratio `(event_gust/reference_gust)**2`, admitted
only over 0–2. Raw 10-minute STORM wind and a 3-second design reference need the
declared bridge. The reference is a screening engineering choice, not observed
OEM capacity.

Specify `response_hypothesis_id` (`approved_replacement` or `repair_sensitivity`)
and `resistance_scenario` (`lower_resistance`, `central_screening` or
`upper_resistance`). These are unweighted alternatives, not confidence bounds.
Repair assumes the documented retained hardware remains serviceable. At pressure
ratio zero, modeled-unit conditional DR is zero; missing or out-of-domain demand
withholds. Check nonzero requests against the [known answers](../../cells/tropical_cyclone_wind_bess/current/known_answers.json).

Use matching same-unit values from [value binding](../../cells/tropical_cyclone_wind_bess/current/value_binding.json). Enclosure and
PCS hardware total $94.4M of $109.8M full TIV; the $15.4M remainder stays unbound.
Major-compromise replacement is an engineering hypothesis, not a rule that every
gust destroys a unit. No intrinsic Damage spread, autonomous frequency, extra
debris/rain ingress or propagation model is supplied.

[Contract](../../cells/tropical_cyclone_wind_bess/current/metadata.md) and [derivation](../../cells/tropical_cyclone_wind_bess/current/derivation.md) govern the request.
Conditional annual use requires Hazard's qualified source/reference, declared
common storm, original unknown support, separate unit caps and annual AEP/OEP/
tails. The Damage artifact alone is not an annual, complete-property, portfolio
or recipient risk product.
