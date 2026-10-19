---
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: done
scope: Research comparison; original local candidate and all runtime capabilities unchanged
---

# Remaining-property and domain audit r4

Read [the bounded review and BF-Q02](../../05_remaining_property_and_flood_domain.md).

| File | Purpose |
|---|---|
| [Source captures](source_captures.json) | Exact citations, access outcomes and local source hashes; no inaccessible document represented as read |
| [Property disposition](remaining_property.csv) | Four non-overlapping parent budgets; child failure units without fabricated allocations |
| [Policy examples](policy_examples.csv) | 40 controlled depth/condition/policy comparisons; complete-plant amounts withheld |
| [Riverine comparison](riverine_domain_impact.csv) | 438 diagnostic placement/RP cases; no event/annual inference |
| [Checks](known_answer_checks.csv) | 70 pin, replay, boundary, missing-input, value-cap and coverage checks |
| [Receipt](audit_receipt.json) | Exact inputs, script and outputs; unchanged candidate pins |

Reproduce from Damage, using Hazard's already installed parquet dependencies:

```bash
../Hazard_modeling/.venv/bin/python scripts/reference_helpers/bess_flood_domain_audit.py \
  --hazard-repo ../Hazard_modeling \
  --output-dir docs/extra/discussion/bess_damage/evidence/r4
```

Requires the saved Riverine r2 parquet, whose hash is checked against the committed
Hazard receipt. This helper is research arithmetic, not a production dependency.
It preserves the original v0.1 artifacts and never writes national/annual outputs.
