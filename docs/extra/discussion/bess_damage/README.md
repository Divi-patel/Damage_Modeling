<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS Damage reasoning and evidence; no released BESS response
-->

# BESS Damage research

Start with [the grouped-value review and BF-Q01](04_grouped_repair_and_value.md), then
[the candidate pressure test](03_flood_candidate_pressure_test.md) and
[the first evidence review](01_flood_evidence_and_reuse.md) for the original audit.
The target is Hazard's selected **100 MW / 400 MWh usable-AC, outdoor LFP battery
plant**, excluding the collector station and export line. The profile is pinned
at Hazard commit `23e1aac4d`; exact input hashes are in
[the audit receipt](evidence/audit_receipt.json).

**Current checkpoint:** the original PVSCM inputs now support a four-group
allocation of the unchanged $84M enclosure budget. **31 r3 checks pass**, in
addition to the retained 52 r2 checks. BF-Q01 presents one concrete choice: a
conservative common-entry active-hardware replacement policy, or holding the
battery response for matched service evidence. The recommendation is the first
as a labeled screening candidate; the owner ruling remains open. No BESS runtime
curve or predicted monetary result exists. These examples are policy arithmetic,
not site predictions. Next: record the ruling and continue qualification under
[the execution plan](../../../plans/bess_damage/README.md).

| Date | Created by | Related to | Record | Purpose |
|---|---|---|---|---|
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Grouped repair and value](04_grouped_repair_and_value.md) | Original cost inputs, same-budget allocation, one open repair-policy choice and 31 checks |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Candidate pressure test](03_flood_candidate_pressure_test.md) | OEM anatomy, immersion endpoint audit, conditional PCS and battery hypothesis checks |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Flood evidence and reuse](01_flood_evidence_and_reuse.md) | First seven-step review, numerical pressure test and immediate research choices |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage | [Bounded search](02_bounded_search.md) | Exact search scope, endpoint tests, limits and follow-on leads |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage | [Evidence registers](evidence/README.md) | Sources, claims, reuse, value and reproducible audit |

Classification: `EVIDENCE_ONLY_NO_OUTPUT_CHANGE` plus planning documentation.
These are pre-cell research records, not a `flood_bess` release or a runtime-shaped
placeholder. The current artifact index and all existing cell outputs remain
unchanged. A subsequent candidate/new-cell package follows the existing skill's
new-cell and capability gates.
