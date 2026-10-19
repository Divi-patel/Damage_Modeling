---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Qualified BESS TC wind v1.0 consumer inputs and annual-use prerequisites
---

# Consumer contract

Pin model v1.0/docs r1/bundle v3 and the exact current artifact, capability and
value hashes. The JSON artifact is the Damage handoff; the old proposal's
`evaluate_local.py` remains historical authoring evidence, not a current runtime.

| Input | Meaning |
|---|---|
| `failure_unit_id` | Integrated enclosure or separate PCS; residual units withheld |
| `pathway_id` | Explicit `tropical_cyclone_wind` |
| comparable pressure ratio | Squared comparable event/reference 3-second gust ratio, valid 0–2; no unbridged rating or extrapolation |
| `response_hypothesis_id` | Explicit `approved_replacement` or `repair_sensitivity` |
| resistance scenario | Explicit lower/central/upper; unweighted sensitivity |
| physical identity/value | Unique physical unit and its exact same-unit value |

M3 emits conditional mean unit DR/scenario cost. No intrinsic random Damage
spread, autonomous event frequency or plant distribution is supplied. Missing
response is null, not zero. Complete-plant metrics remain withheld.

The qualified Hazard consumer imports its installed `hurricane.api` loader and
response/annual functions. Its annual calculation is separate: common storm
identity, declared rank coupling, original source mass/unknown states, per-unit
annual cap before plant sum, no within-year restoration, saved annual AEP/OEP and
independent mean/fixed-mass-tail checks. The capability declaration is conditional
on those gates. Only then may it report partial-scope annual screening metrics.

The current validated reference is a regional MRI1700 engineering proxy with
MRI700/3000 alternatives; this is a consumer policy, not observed OEM capacity or
a legal design classification. Current source floor and rare-tail limits stay
visible. An unavailable clock is unknown annual support, not an event probability.
National support, portfolio composition, portable packaging and recipient release
need their own checks. See [capability](capability.json) and [derivation](derivation.md).
