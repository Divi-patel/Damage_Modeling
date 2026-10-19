---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Exact local input/output and withholding contract for BESS wind v0.1
---

# Local input contract

Pin model v0.1 / docs r1 / bundle v3 and every member of
`consumption_pin.json`. `load_candidate(allow_local_test=True)` is mandatory;
the default refuses numerical use. This is an artifact-local test reader,
not a production `damage_code()` endpoint.

| Field | Exact meaning |
|---|---|
| `failure_unit_id` | `BESS_INTEGRATED_ENCLOSURE` or `BESS_SEPARATE_PCS`; other units withheld |
| `pressure_ratio` | Finite real 0–2; Boolean/string/None/NaN/infinity rejected; no clamp |
| `pathway_id` | `tropical_cyclone_wind`; never inferred from intensity |
| `demand_basis_id` | `BESS_TC_LOCAL_PRESSURE_RATIO_RESEARCH_V1`; not an unbridged wind speed |
| `response_hypothesis_id` | Explicit `approved_replacement` or `repair_sensitivity`; no default |
| `resistance_scenario` | Explicit `lower_resistance`, `central_screening` or `upper_resistance`; no probability interpretation |

Output is conditional same-unit DR/candidate cost, exact curve ID and limitation
flags. An unavailable response has null DR and cost. Complete-plant cost is null
for every call. No EAL/PML/VaR/TVaR, insurer settlement or revenue loss is emitted.

```python
candidate = load_candidate(allow_local_test=True)
result = evaluate(
    candidate,
    failure_unit_id="BESS_INTEGRATED_ENCLOSURE",
    pressure_ratio=1.0,
    pathway_id="tropical_cyclone_wind",
    demand_basis_id="BESS_TC_LOCAL_PRESSURE_RATIO_RESEARCH_V1",
    response_hypothesis_id="approved_replacement",
    resistance_scenario="central_screening",
)
```

This demand-1 local fixture returns about 0.3123313 DR / $327,947.87 mean cost
under synthetic state probabilities. It is not the cost of a known major state,
the annual probability of a loss, or a design-code claim. The known major state's
selected cost remains the integrated $1.05M replacement.
