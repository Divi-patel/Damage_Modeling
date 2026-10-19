---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Local candidate input and output contract
---

# Inputs, outputs and non-admission

Pin `flood_bess`, model v0.1, docs r1, bundle-v2 and all hashes in
`consumption_pin.json`. Use `allow_local_candidate=True` only in the authorized
local test. No default loader, runtime index or national producer selects this
proposal. Global schemas and existing cells are unchanged.

| Input | Required interpretation |
|---|---|
| `unit_kind` | `battery_enclosures` or `pcs`; the supplied depth refers to one physical unit |
| `depth_m` | Finite numeric depth above local grade; 0–2.3m test envelope; no Boolean/string/negative input |
| `water_condition` | Explicit `freshwater_screening`, not inferred from a location |
| `policy_id` | Exact `BF_Q01_ACTIVE_REPLACEMENT_LOCAL_V1` |
| `hazard_status` | Available, or a preserved missing/domain/siting reason |

Unsupported water conditions, missing/invalid depth, unknown property and domain
failures return null DR/cost with a reason. No table endpoint extrapolation.
The adapter constructs the battery's binary state from depth; callers cannot
pass a fractional state. Output `candidate_hardware_loss_usd` is explicitly
local policy arithmetic. `complete_plant_loss_usd` is always null. No EAL/PML,
VaR/TVaR, insurance terms or sizing projection is supplied.

For multiple units, retain instance identity and local exposure. A single wet
enclosure incurs one active-enclosure amount, not 80 copies. Sum only disjoint
physical units; a known subtotal must preserve missing units and the unresolved
property ledger. Do not label it a mathematical lower bound on true loss: the
candidate itself is an uncalibrated conservative policy.
