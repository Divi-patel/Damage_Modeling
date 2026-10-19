---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS v1.0 model-specific input, value and annual-consumer contract
---

# Runtime and consumer contract

Pin `flood_bess@model_v1_0__docs_r1`, bundle/capability v2 and all hashes in
`consumption_pin.json`. The value-binding schema is model-specific
`bess-annual-screening-value.v1`; no global contract field changed.

| Input | Required interpretation |
|---|---|
| Physical ID and kind | Unique reference instance; `battery_enclosures` or `pcs`; declared counts match |
| External depth | Finite nonnegative metres above local grade; missing is NaN/withheld, never zero |
| Water condition | Explicit `freshwater_screening` or `saline_screening`; no implicit fallback |
| Entry | Reference 0.30 m; comparison is strictly greater-than for binary records |
| Value | Same-unit hardware value; no MW/MWh multiplier and no unmodeled-value redistribution |
| Policy | `BESS_FLOOD_SCREENING_V1` |

The response is a conditional DR/cost. The Hazard annual consumer enforces
frequency, shared event/rank, local capacity and same-unit caps. It reports
modeled annual contribution and missing-event probability separately. Complete
plant EAL and complete physical-risk status remain withheld/false.

`annual_response_complete` refers only to annual evaluation of the modeled
hardware: it does not mean all property is modeled. A measured-zero event rate
can complete that annual evaluation despite absent conditional surge pixels;
`unit_source_coverage` and `value_source_coverage` still reveal those missing
pixels. No supported catalog/rate means no such measured-zero inference.

Missing-risk projection preserves original probability mass. A numeric zero
contribution is not a vulnerability answer for missing depth. This cell does
not independently output event rates, AEP/OEP, PML, VaR, TVaR or insured losses.
