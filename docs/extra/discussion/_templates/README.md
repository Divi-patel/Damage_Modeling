<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: active
scope: Blank discussion-node template carrying the Hazard_modeling reasoning-log conventions — one bounded question, options weighed, pressure tests, a verdict, owner gates, an exit condition and a promotion target.
-->

# docs/extra/discussion/_templates/

Start a new reasoning node by copying [`TEMPLATE_discussion_node.md`](TEMPLATE_discussion_node.md) to
`docs/extra/discussion/<topic_slug>/README.md` (a folder, so evidence files can sit beside it) or to
`docs/extra/discussion/YYYY-MM-DD_<topic_slug>.md` for a single dated note. The conventions come from the
sibling `Hazard_modeling` repository (`docs/discussion/README.md` and
`docs/guides/the_documentation_workflow.md` there); the local index is [`../README.md`](../README.md).

## What a node is for

A node opens for **one bounded decision question**. It records the options weighed, the pressure tests run
and the dead ends named — not just the verdict. The verdict itself lands elsewhere: a `<PREFIX>-D*` row in a
plan's `decisions.md`, a cell package change, a contract or a released artifact. A discussion can recommend;
only the applicable standard, cell package, contract or artifact can authorize.

## Done when

A **verdict exists** — even "we chose to defer, and here is the trigger". Then the node names its exit
condition and promotion target and its status flips: `active` while gates are open → `settled` when the
question has an answer written in the node → `superseded` when a later node replaces it (link forward).

## Ledger duty

Add the node's row to [`../README.md`](../README.md) in the same commit, newest first, copying `Date` and
`Created by` from the node's stamp.
