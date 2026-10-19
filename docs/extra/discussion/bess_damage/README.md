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

**Current checkpoint:** BF-Q01 is approved for local testing. The
[proposed Flood BESS cell](../../../cells/flood_bess/README.md) packages the
binary active-hardware policy and separate PCS proxy with exact pins and
ordinary runtime/annual capabilities withheld. Hazard's first local proof
passes 15 targeted tests and 10 controlled examples; the existing 12-cell
Pluvial controls remain below the assumed entry. The r1–r3 records below
preserve the prior evidence and decisions; their open-status snapshots predate
the owner's approval. No national or canonical BESS result is released.

| Date | Created by | Related to | Record | Purpose |
|---|---|---|---|---|
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Grouped repair and value](04_grouped_repair_and_value.md) | Original cost inputs, same-budget allocation, one open repair-policy choice and 31 checks |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Candidate pressure test](03_flood_candidate_pressure_test.md) | OEM anatomy, immersion endpoint audit, conditional PCS and battery hypothesis checks |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage / Hazard | [Flood evidence and reuse](01_flood_evidence_and_reuse.md) | First seven-step review, numerical pressure test and immediate research choices |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage | [Bounded search](02_bounded_search.md) | Exact search scope, endpoint tests, limits and follow-on leads |
| 2026-10-18 | owner-directed (Divy) · agent-researched | Damage | [Evidence registers](evidence/README.md) | Sources, claims, reuse, value and reproducible audit |

Classification: `EVIDENCE_ONLY_NO_OUTPUT_CHANGE` plus planning documentation.
The r1–r3 records are pre-cell research; the separately linked local candidate
is not a `flood_bess` release. The current artifact index and all existing cell outputs remain
unchanged. A subsequent candidate/new-cell package follows the existing skill's
new-cell and capability gates.
