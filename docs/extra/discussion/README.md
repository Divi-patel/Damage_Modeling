<!--
author: Divi-patel (2026-06-21) · revision 2026-08-26 owner-directed (Divy) · agent-drafted
created: 2026-06-21
updated: 2026-10-16
status: active
scope: reasoning-log index — the ledger over every discussion node/package, the discussion → plan progression, the stamp, the closed status vocabulary and the node template.
-->

# Discussion index

Discussion notes are the P2 surface for unresolved reasoning before a plan or governed cell decision is
committed. They are inputs to plans and cell packages, not runtime authority. A node opens for **one bounded
decision question**, records the options weighed and the pressure tests run, and ends in a **verdict** — even
"we chose to defer, and here is the trigger". Start a new node from [`_templates/`](_templates/README.md).

## The discussion ledger — newest first

*`Date` and `Created by` are copied from each node's own stamp (the authority); this table is an index over
it. `Related to` is the teammate a node is routed to — blank until assigned. `Status` uses the closed
vocabulary for stamped nodes; rows that predate the stamp keep the status phrase they were recorded with (in
italics) until backfilled, and their `Date` / `Created by` come from the file's first git commit (or the
date the document names).*

| Date | Topic | Created by | Related to | Status | Purpose |
|---|---|---|---|---|---|
| **2026-10-18** | [`bess_damage/`](bess_damage/README.md) | owner-directed (Divy) · agent-researched | Divy / Hazard | active | Bounded Flood source/claim and value review, five source curves / 95 checks, explicit BESS transfer limits and next candidate. |
| **2026-10-16** | [`substation_damage/`](substation_damage/README.md) | owner-directed (Divy) · agent-researched | Divy / Hazard | active | Pinned Flood assembly reuse review, 93 numerical cases, 31-row value accounting, open source/profile/denominator qualification and skill 0.8. |
| **2026-10-15** | [`real_estate_conus/`](real_estate_conus/README.md) | owner-directed (Divy) · agent-drafted | — | active | Warehouse/office/house scope, skill revision 0.7, pinned Junga Flood proposal intake, office source check and consumer gaps; linked warehouse-first Hazard plan; no current release changes. |
| **2026-08-29** | [`tornado_solar/`](tornado_solar/README.md) | owner-directed (Divy) · agent-drafted | Divy | active | What Damage research, pathway contract and promotion evidence are required before Tornado × Solar can replace the current aerodynamic lower-bound sensitivity; current versions remain unchanged. |
| **2026-08-26** | [`cell_notebook_coverage/`](cell_notebook_coverage/README.md) | owner-directed (Divy) · agent-drafted | — | active | Should every hazard × asset cell carry companion notebooks, in what shape and order — and why the two existing pairs no longer run. Verdict recorded; owner gates G1–G4 open; executes through [`plans/cell_notebook_coverage/`](../../plans/cell_notebook_coverage/README.md). |
| 2026-08-18 | [`2026-08-18_damage_modeling_architecture_and_flow.md`](2026-08-18_damage_modeling_architecture_and_flow.md) | Divi-patel | — | *reference (unstamped review)* | Walkthrough of the repository at commit `9009770`: navigation, file lifecycle, consumer flows A–D, the version convention, and the Part IV gap list (missing CI, 2-of-10 notebook coverage, bespoke validators, no spread standard). |
| 2026-07-28 | [`hazard_asset_coverage/`](hazard_asset_coverage/README.md) | Divi-patel | — | *accepted planning input* | Separate structural coverage from runtime-curve maturity and define the coverage-first sequence. |
| 2026-07-28 | [`flood_wind_shared_electrical/`](flood_wind_shared_electrical/README.md) | Divi-patel | — | *active decision record* | Frame flood × wind, GSU/substation reuse, ownership, value, and the non-runtime shared electrical substrate. |
| 2026-07-06 | [`repo_information_architecture.md`](repo_information_architecture.md) | Divi-patel | — | *executed decision* | Explain the repository information architecture adopted by the corresponding plan. |
| 2026-06-25 | [`drive_docs_review/`](drive_docs_review/README.md) | Divi-patel | — | *active/reference* | Review imported Drive methodology material. |
| 2026-06-25 | [`implementation_improvements.md`](implementation_improvements.md) | Divi-patel | — | *reference* | Track general implementation improvements. |
| 2026-06-21 | [`evidence_harvest/`](evidence_harvest/README.md) | Divi-patel | — | *active/reference* | Review and classify legacy curve evidence. |
| 2026-06-21 | [`archive/`](archive/README.md) | Divi-patel | — | *archive* | Preserve superseded discussion without making it current authority. |

## Progression

```text
discussion -> plan -> governed implementation -> validation -> task history
```

A discussion can recommend a change. Only the applicable method standard, cell package, contract, or released
artifact can authorize it. When the question is answered, the verdict lands as a `<PREFIX>-D*` row in the
plan's `decisions.md` (or in the cell package / contract that authorizes it) and the node flips to `settled`.

## The stamp and the status vocabulary

Every node carries a five-field stamp in an HTML comment at the top — `author · created · updated · status ·
scope`. Agent-drafted work is stamped `owner-directed (<name>) · agent-drafted`. The vocabulary is **closed**:
`draft · proposed · active · settled · superseded · done` — `active` while gates are open, `settled` when the
answer is written in the node, `superseded` only with a forward link.

## Ledger duty

Add a node's row to this table **in the same commit** as the node, newest first; update the row in the same
edit that changes the stamp. If the row and the stamp disagree, the stamp wins.
