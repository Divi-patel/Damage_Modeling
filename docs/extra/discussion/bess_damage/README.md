<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS Damage reasoning and evidence; no released BESS response
-->

# BESS Damage research

Start with [the first Flood evidence review](01_flood_evidence_and_reuse.md).
The target is Hazard's selected **100 MW / 400 MWh usable-AC, outdoor LFP battery
plant**, excluding the collector station and export line. The profile is pinned
at Hazard commit `23e1aac4d`; exact input hashes are in
[the audit receipt](evidence/audit_receipt.json).

**Current checkpoint:** existing electrical curves reproduced, primary-source
claims separated from numerical assumptions, and every reference-budget row
assigned a research treatment. There is no BESS runtime curve or monetary result.
The next work is a bounded battery-ingress/consequence candidate and PCS transfer
test under [the execution plan](../../../plans/bess_damage/README.md).

| Date | Created by | Related to | Record | Purpose |
|---|---|---|---|---|
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Flood evidence and reuse](01_flood_evidence_and_reuse.md) | First seven-step review, numerical pressure test and immediate research choices |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage | [Bounded search](02_bounded_search.md) | Exact search scope, endpoint tests, limits and follow-on leads |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage | [Evidence registers](evidence/README.md) | Sources, claims, reuse, value and reproducible audit |

Classification: `EVIDENCE_ONLY_NO_OUTPUT_CHANGE` plus planning documentation.
These are pre-cell research records, not a `flood_bess` release or a runtime-shaped
placeholder. The current artifact index and all existing cell outputs remain
unchanged. A subsequent candidate/new-cell package follows the existing skill's
new-cell and capability gates.
