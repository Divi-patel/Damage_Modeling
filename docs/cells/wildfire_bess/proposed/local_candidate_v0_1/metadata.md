---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Input and capability contract for local Wildfire BESS candidate v0.1
---

# Local input/output contract

| Field | Required value / behavior |
|---|---|
| `allow_local_test` | Literal `True` on load; ordinary production loading refused. |
| `pathway_id` | `wildfire_thermal_attack`; no autonomous-fire/flood/wind fallback. |
| `selector_id` | `BESS_LFP_R1_WILDFIRE_ORDINAL_LOCAL_V0_1`; selected reference only. |
| `failure_unit_id` | `BESS_INTEGRATED_ENCLOSURE` or `BESS_SEPARATE_PCS`; residual units withheld. |
| `class_state` | Finite exact integer 0..6; booleans/strings/fractions/missing/out-of-range rejected. State0 is no-event, not missing source. |
| `response_hypothesis_id` | `approved_replacement`, `noncell_repair_sensitivity` or `limited_repair_sensitivity`; no default. |
| `shape_scenario` | `electronics_ordinal` or `heavy_electrical_ordinal`; no percentile interpretation or default. PCS keeps its electronics response under either enclosure shape. |
| `assume_retained_hardware_serviceable_for_sensitivity` | Literal `True` for repair cases. This is an explicit local counterfactual, not evidence of actual serviceability. |
| Frequency, heat-flux, duration, generic discount inputs | Unsupported; not hidden converters or optional credits. |

Output is a conditional scalar mean DR and same-unit expected hardware dollars,
with `local_candidate_only`, curve identity and limitation flags. It is not an
observed damage assessment. Known compromised battery replacement cost is $1.05M;
a severity-class mean can be smaller and must never be labeled the known-state
repair cost. Every annual metric and complete-plant loss remains unavailable.

JSON owns the response/value/capability; CSVs are audit views. Exact-state lookup
is mandatory even though the existing schema's table carrier is named
`piecewise_linear`. No interpolation/extrapolation occurs. The standalone and
embedded capability are identical. The consumption pin covers the local reader
and numerical payloads; no canonical index entry is created.
