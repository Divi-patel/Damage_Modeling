<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: active
scope: Blank plan-folder templates (README · decisions · assumptions) carrying the Hazard_modeling plan conventions — 5-field stamp, closed status vocabulary, outcome-first shape, checkable done-when, owner gates.
-->

# docs/plans/_templates/

Start a new plan folder by copying these three files into `docs/plans/<topic_slug>/` and filling every
section. The conventions come from the sibling `Hazard_modeling` repository
(`docs/guides/the_documentation_workflow.md` there); the local index is [`../README.md`](../README.md).

| Template | Becomes | Purpose |
|---|---|---|
| [`TEMPLATE_plan_README.md`](TEMPLATE_plan_README.md) | `README.md` | the plan of record — outcome first, scope, current state, decisions fixed, sequence with gates, validation, done-when, owner gates |
| [`TEMPLATE_plan_decisions.md`](TEMPLATE_plan_decisions.md) | `decisions.md` | `<PREFIX>-D01 …` decision register — Decision + Reason; recommendations awaiting an owner gate are marked |
| [`TEMPLATE_plan_assumptions.md`](TEMPLATE_plan_assumptions.md) | `assumptions.md` | `<PREFIX>-A01 …` assumption / watchlist table with change triggers |

## The stamp (required on every file)

```text
<!--
author: <name>  |  owner-directed (<name>) · agent-drafted
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: proposed | active | settled | superseded | done      (draft is allowed before a teammate can read it)
scope: one line — what this plan changes and how it will be verified
-->
```

The status vocabulary is **closed**: `draft · proposed · active · settled · superseded · done`. A plan starts
`proposed` and becomes `active` only when the owner says go; `done` when its done-when passed and the result
was verified; `superseded` only with a forward link to the replacement.

## Ledger duty

Add the plan's row to [`../README.md`](../README.md) **in the same commit**, newest first, copying `Date`
and `Created by` from the plan's own stamp. The stamp is the authority; the table is an index over it.

## Choose a decision/assumption prefix

Pick a short unique prefix per plan (`COV-`, `NB-`, …) so IDs can be cited across plans without collision.
