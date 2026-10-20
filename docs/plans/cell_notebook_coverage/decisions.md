<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: proposed
scope: Decision register for the cell notebook coverage plan (NB-D*). Recommendations awaiting owner gates are marked; an owner ruling is never inferred.
-->

# Cell notebook coverage — decisions

Format mirrors [`hazard_asset_coverage/DECISIONS.md`](../hazard_asset_coverage/DECISIONS.md). Each row is a
decision the plan executes against. Rows marked **recommended · gate Gn** become decisions only when the
owner answers the gate in the plan README; until then they are the agent's recommendation.

## NB-D01 — Repair before build

**Decision:** re-point, re-execute and reconcile the two existing pairs (`hail_solar`, `flood_solar`) to
their current index pins before any new cell notebook is started.

**Reason:** the existing pairs are the template the next eight will copy. Copying a broken loader eight times
is the fastest way to have ten broken notebooks. Repair is also the cheapest proof that the loader rule works.

## NB-D02 — One cell at a time, hurricane pair first

**Decision:** build in the order repair → scaffolding → `tropical_cyclone_wind_wind` →
`tropical_cyclone_wind_solar` → `wildfire_solar` → `strong_wind_solar` → `wind_tornado_wind` → `flood_wind` →
`wildfire_wind` → `hail_wind`; a package closes before the next opens.

**Reason:** the same rule the coverage plan used (D-002) — bounded reviewer attention and bounded blast
radius. The hurricane pair goes first because the 2026-08-18 review identified it as the most instructive
cell (a complete correction arc) with no walkthrough, and because Hazard consumes both of its artifacts today.

## NB-D03 — Resolve through the artifact index and verify the SHA

**Decision:** runtime notebooks for current cells resolve their artifact only through
`docs/contracts/machine_readable_artifact_index.json` and assert the SHA-256; proposal-only cells name their
`proposed/` file explicitly and print a NONCANONICAL or WITHHELD banner.

**Reason:** the two existing pairs broke because they welded a folder path copied from a deliverable tree.
The index is the repository's own statement of the current pin; the SHA makes a silent artifact swap visible
inside the notebook.

## NB-D04 — One shared helper beside the notebooks

**Decision (recommended · gate G2):** put root discovery, index lookup, SHA verification, the v2/v3 record
resolver and the KAT runner in `notebooks/_shared/repo_paths.py`, imported by path from every notebook.

**Reason:** ten copies of a loader cell drift; one helper changes once. The helper is not a `src/` API and
creates no consumer obligation. Alternative if the owner declines: an identical loader cell in every notebook,
with the structure test grepping for drift.

## NB-D05 — Import the repository evaluators

**Decision:** notebooks import `scripts/reference_helpers/damage_curve_eval.py` for supported curve forms;
an unsupported form is evaluated by a clearly titled local helper alongside the artifact's own formula
string, and the gap is logged as a follow-on to extend the evaluator.

**Reason:** a notebook that re-implements the logistic is a second, unreviewed evaluator.
`evaluate_curve_record` already dispatches `logistic`, `piecewise_linear`, `wind_tornado_logistic_ratio`
(with the `tornado_variant` D50 shift via `context`) and `thresholded_logistic_demand`; `strong_wind_solar_r_eff`
derives the demand ratio. The known gaps are the exact categorical-state lookup `wildfire_solar` requires (its
records are stored as `piecewise_linear` points but the artifact forbids interpolation — mirror
`validate_runtime_contracts.exact_state_value`) and any bundle-v3 pathway record whose `curve_form` is not in
that dispatch. Surfacing those as gaps is more useful than hiding them in notebook cells.

## NB-D06 — The runtime notebook evaluates exactly one artifact

**Decision:** `01` evaluates the cell's current pin — or, for cells without one, the named lead proposal —
and nothing else. Noncanonical v2 proposals for cells that already have a canonical v1 appear only as
"what's next" links in `00`.

**Reason:** a reader must never leave a runtime notebook unsure which curve Hazard actually consumes. The
coverage plan's counting rules already separate structural, proposal and runtime coverage; the notebooks
must not blur them again.

## NB-D07 — Withholding is a result to show, not a reason to skip

**Decision (recommended · gate G3):** zero-curve (`hail_wind`) and partial-screening cells get runtime
notebooks that load the artifact, list every withheld unit with its reason code and run the KATs that assert
the withholding.

**Reason:** the library's honesty is its main claim. A notebook that shows "this cell publishes no numeric
response, and here is the test that proves it" is the coverage record for that cell; skipping it would make
the notebook matrix overstate what a reader can learn.

## NB-D08 — Notebooks never author or publish

**Decision:** no notebook edits a curve artifact, workbook, KAT file, changelog, artifact index, schema or
GCS object; the only writes are figures under the notebook's own `outputs/`. A finding routes to the cell's
evidence memo or proposal path.

**Reason:** the same boundary the consumer repo enforces ("notebooks never publish"). In this repository the
governed objects are the cell packages and contracts; a notebook is a reader of them.

## NB-D09 — Companions, not required package files

**Decision:** this plan does not amend standard 02 (cell package standard) to require notebooks. Each cell
README links its pair under "Companion notebooks"; making notebooks a required package file is a separate
owner decision.

**Reason:** changing a definition redraws every instance in the same commit; the plan's job is coverage,
not a standards change. Once 10/10 exists, the owner can decide whether to make it a requirement.

## NB-D10 — Headless execution is a manual gate until CI exists

**Decision:** `scripts/reference_helpers/execute_notebooks.py` is the execution gate, run by hand before a
package closes; CI wiring is out of scope because `.github/` does not exist in this repository.

**Reason:** the 2026-08-18 review already lists the missing CI as the repo's cheapest gap; conflating the two
plans would block notebook coverage on infrastructure it does not need.
