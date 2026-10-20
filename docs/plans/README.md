<!--
author: Divi-patel (2026-07-06) · revision 2026-08-26 owner-directed (Divy) · agent-drafted
created: 2026-07-06
updated: 2026-10-16
status: active
scope: planning index (the intent + decision layer) — the ledger over every plan folder, the discussion → plan → execution workflow, the stamp, the closed status vocabulary and the templates.
-->

# docs/plans/ — the plan-of-record

Planning home for `damage_modeling` workstreams that have graduated from discussion into a build shape.

The convention mirrors `Hazard_modeling`: exploratory reasoning stays under
[`docs/extra/discussion/`](../extra/discussion/README.md); when a direction is stable enough to execute
carefully, it gets a folder here with a plan-of-record (`README.md`), a decisions log (`decisions.md`) and an
assumptions register (`assumptions.md`). Start a new folder from [`_templates/`](_templates/README.md).

## The plan ledger — newest first

*`Date` and `Created by` are copied from each plan's own stamp (the authority); this table is an index over
it. `Related to` is the teammate a plan is routed to — blank until assigned. `Status` uses the closed
vocabulary for stamped plans; rows that predate the stamp keep the status phrase they were recorded with
(in italics) until their plan is backfilled, and their `Date` / `Created by` come from the folder's first
git commit.*

| Date | Plan | Created by | Related to | Status | What it decides |
|---|---|---|---|---|---|
| **2026-10-18** | [`bess_damage/`](bess_damage/README.md) | owner-directed (Divy) · agent-drafted | Divy / Hazard | active | Flood-first BESS curation: first evidence/reuse audit complete; enclosure/PCS candidate next; size-scaling handoff tracked for later. |
| **2026-10-16** | [`substation_damage/`](substation_damage/README.md) | owner-directed (Divy) · agent-researched | Divy / Hazard | active | Qualify existing Flood substation response, repair-value scope, governed standalone candidate and conditional/annual consumer proofs; numerical review complete, proxy and denominator unresolved. |
| **2026-08-26** | [`cell_notebook_coverage/`](cell_notebook_coverage/README.md) | owner-directed (Divy) · agent-drafted | — | proposed | Repair the two broken companion-notebook pairs against their current pins, then give every governed cell an executing curation + runtime notebook pair, one cell at a time, hurricane pair first — with a per-notebook contract, per-cell work packages, a structure test and owner gates G1–G4. |
| 2026-08-14 | [`tropical_cyclone_wind_wind_v1_1_proxy/`](tropical_cyclone_wind_wind_v1_1_proxy/README.md) | Divi-patel | — | *owner-approved model-behavior change planned; v1.0 remains current* | Build and validate the explicit canonical-5-MW screening proxy, 0.63 covered-value crosswalk and Hazard migration gates. |
| 2026-07-29 | [`strong_wind_solar_completion/`](strong_wind_solar_completion/README.md) | Divi-patel | — | *step 1 audit complete; promotion blocked* | Harden the existing convective-wind × solar v2 proposal without rebuilding it, close scientific and consumer gates in order, and preserve v1 as canonical until an explicit release decision. |
| 2026-07-29 | [`tropical_cyclone_wind_solar_completion/`](tropical_cyclone_wind_solar_completion/README.md) | Divi-patel | — | *owner-authorized noncanonical model-v2/docs-r1 candidate built; promotion blocked* | Govern five records—one Perry compatibility record plus four cell-local synthetic-T4 records—while preserving v0.1/v1 and acquiring the evidence required for any promotion. |
| 2026-07-29 | [`solar_wind_normalized_response/`](solar_wind_normalized_response/README.md) | Divi-patel | — | *comparison-only candidate v0.1; no runtime authority* | Govern the hazard-label-neutral, solar-specific audit fingerprint without treating strong-wind numerical identity as tropical-cyclone evidence or a shared runtime dependency. |
| 2026-07-28 | [`hazard_asset_coverage/`](hazard_asset_coverage/README.md) | Divi-patel | — | *breadth complete: 10/10 structural, 8/10 repository-current canonical runtime after partial-screening flood_wind, wildfire_wind, and tropical_cyclone_wind_wind v1 releases; TC-wind-solar also has a noncanonical model-v2.1 candidate* | Continue depth work one cell at a time; partial canonical status is not complete calibration, and the out-of-queue TC-solar work does not change current pins. |
| 2026-07-28 | [`flood_wind_shared_electrical/`](flood_wind_shared_electrical/README.md) | Divi-patel | — | *phase 2 complete; local v1 proposal noncanonical; shared runtime deferred* | Govern the flood-wind cell and asset-neutral flood-electrical substrate while preserving an explicit future migration path. |
| 2026-07-06 | [`repo_information_architecture/`](repo_information_architecture/README.md) | Divi-patel | — | *initial plan-of-record* | Normalize the repo from deliverable-shaped navigation into a shallow, durable documentation architecture without losing provenance. |

## Workflow

```text
discussion note (docs/extra/discussion/)
  -> plan folder (here: README + decisions + assumptions)
  -> staged execution, one bounded package at a time
  -> verification against the plan's own gates and done-when
  -> task history / handoff (docs/extra/tasks_history/)
```

Planning docs are not raw research and are not runtime artifacts. They are the build-facing record of what we
intend to change, why, and how we will verify it. A plan can schedule a change; only the applicable method
standard, cell package, contract or released artifact can authorize it.

## The stamp and the status vocabulary

Every plan file carries a five-field stamp in an HTML comment at the top —
`author · created · updated · status · scope`. Agent-drafted work is stamped honestly as
`owner-directed (<name>) · agent-drafted`.

The status vocabulary is **closed**: `draft · proposed · active · settled · superseded · done`.

| Flip | Trigger — the thing that must actually be true |
|---|---|
| `draft → proposed` | coherent enough that a teammate reading it would not be misled |
| `proposed → active` | the owner said go |
| `active → done` | the done-when passed **and** the result was verified |
| `anything → superseded` | a replacement exists and this plan links forward to it |

An owner ruling is never inferred: a plan that needs one lists the gate, the options and a recommendation, and
stays `proposed` until the owner answers.

## Ledger duty

Add a plan's row to this table **in the same commit** as the plan, newest first. When a plan flips status,
update the row in the same edit as the stamp. If the row and the stamp disagree, the stamp wins and the row is
wrong.
