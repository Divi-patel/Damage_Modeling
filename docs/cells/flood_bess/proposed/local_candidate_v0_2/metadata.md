---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Local v0.2 input contract and capability limits
---

# Local input and output rules

Pin model v0.2 / docs r1 / bundle v2 and every digest in `consumption_pin.json`.
The call requires explicit local-test opt-in and policy
`BF_Q02_FLOOD_REPLACEMENT_LOCAL_V2`. An incorrect version/policy is not an alias.

| Input | Interpretation |
|---|---|
| `unit_kind` | One `battery_enclosures` or `pcs` physical instance |
| `depth_m` | Finite nonnegative depth above its local grade, never Boolean/string |
| `water_condition` | Explicit `freshwater_screening` or `saline_screening`; no default conversion of unknown |
| `hazard_status` | Available or the original unavailable/source/siting reason |
| `policy_id` | Exact acknowledged v0.2 policy |

The artifact's `curve_selection_by_water_condition` maps condition and unit to
the exact record. Binary-state records must not be interpolated using depth.
The continuous freshwater PCS record subtracts entry once and has an explicit
constant terminal plateau. The same-unit cap is checked after evaluation.

Output remains `status`, `reason`, `dr`, `candidate_hardware_loss_usd`,
`complete_plant_loss_usd` and interpretation. Complete-plant cost is always null.
Missing input is null DR/cost, never zero. Unsupported property stays unmodeled.
No EAL/PML/VaR/TVaR or insurance/routine-performance quantity is supplied.

The source-coupling consumer additionally retains native source class, bounds,
censoring and entry-bin ambiguity. Category MOM envelopes are not simultaneous
events or return-period losses. Source flags do not silently modify the policy.
