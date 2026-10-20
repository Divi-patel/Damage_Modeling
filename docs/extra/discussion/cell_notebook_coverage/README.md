<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: active
scope: Reasoning node — should every hazard × asset cell carry companion notebooks, in what shape, and why the two existing pairs no longer run. Verdict recorded; owner gates open. Promotion target: docs/plans/cell_notebook_coverage/.
-->

# Cell notebook coverage — the reasoning

> **Status: active.** The verdict below is recorded and the executable sequence lives in the
> [cell notebook coverage plan](../../../plans/cell_notebook_coverage/README.md). This node becomes `settled`
> when the owner answers gates G1–G4 in that plan.

## The question

Only two of the ten governed cells have companion notebooks (`hail_solar`, `flood_solar`), and on 2026-08-26
both of those pairs fail in their first code cell. The
[2026-08-18 architecture review](../2026-08-18_damage_modeling_architecture_and_flow.md) already named the
gap ("Notebooks cover 2 of 10 cells … the most instructive cell — the hurricane one — has none") and
recommended notebooks for the eight uncovered cells. Nothing was planned or executed after it.

So the bounded question is:

```text
Should every cell have companion notebooks?  →  in which shape?  →  built in which order?
and: what broke the two we have, so the next eight do not break the same way?
```

## What was verified before reasoning (2026-08-26)

| Check | Result |
|---|---|
| Notebooks on disk / in git, all refs (`main`, `origin/main`, `divi/main`) | exactly four: `hail/solar/{00,01}`, `flood/solar/{00,01}`; added once in `abd3f3e` (2026-06-25); never deleted, renamed, stashed or left on another branch |
| Remote (`aamani-ai/Damage_Modeling` `main`, GitHub API) | same four — local and remote agree; nothing is unpushed |
| Headless execution (`jupyter nbconvert --execute`, `.venv` python 3.12, nbconvert 7.17) | `hail/solar/01` and `flood/solar/00` raise `RuntimeError` in cell 1: the repo-root finder requires `docs/damage_curves/` to exist |
| Root cause | the loader cell welds a deliverable-shaped path (`docs/damage_curves/damage_curve_implementation/DAMAGE_CURVE_LIBRARY_V2_5_…/01_cells/<cell>/current/…docs_r5|r3…`) that was removed in the information-architecture migration; those exact artifacts now exist only in the gitignored `docs/source_drops/extracted/` mirror, so a fresh clone could never run them |
| Current pins the notebooks *should* read | `hail_solar@model_v1_0__docs_r7`, `flood_solar@model_v1_0__docs_r4` via [`docs/contracts/MACHINE_READABLE_ARTIFACTS.md`](../../../contracts/MACHINE_READABLE_ARTIFACTS.md) |

The memory of "notebooks for almost all hazards" is therefore not lost work in this repo. The per-hazard
damage notebooks that do exist live in the consumer repo (`Hazard_modeling/Notebooks/<peril>/…/m3/`), which
narrates *how Hazard consumes* each curve — a different question from *how Damage curated it*.

## Why notebooks matter here specifically

- **Damage's product is a governed JSON artifact plus a paper trail.** A reader cannot see a curve in a JSON
  file; the runtime notebook is the only place the artifact is evaluated, plotted and reconciled to its
  known-answer tests inside this repo.
- **Curation is the discipline this repo was spun out to protect.** The `00` notebook is the teaching view
  of the dossier: evidence classes → anchors → fitted/interpolated parameters → selectors/conditioners/exposure →
  value link → capability. Without it, the dossier is read only by the person who wrote it.
- **The hurricane cell has a correction arc** (model v1.0 → v1.1 "63% covered value" → v1.2 "tower-only,
  16% covered, 84% withheld"). That arc is the best worked example of honest versioning in the library and
  currently has no walkthrough.
- **Consumers already depend on these artifacts.** Hazard pins seven of them at grid support; a consumer-facing
  example per cell removes the "how do I call this?" question that the request guides answer only in prose.

## Options weighed

| Option | What it is | Verdict |
|---|---|---|
| **A · per-cell `00` + `01` pair** (the shape [`notebooks/README.md`](../../../../notebooks/README.md) already prescribes) | one curation walkthrough + one runtime walkthrough per `notebooks/<hazard>/<asset>/` | **chosen** — cell physics differ too much (logistic · piecewise depth ladder · categorical FSim states · IEC speed ratio · v3 partial-screening pathways · zero-curve) for one generic notebook to explain them |
| B · one cross-hazard notebook looping over the artifact index | a single library overview plotting every current response | not as the primary vehicle; kept as an optional close-out add-on (`notebooks/00_library_overview.ipynb`) once the per-cell pairs exist |
| C · generate notebooks from a template by script | parameterize one template per role and render ten copies | partially adopted — **templates yes, generation no**; the curation story is bespoke per cell and a rendered copy would be a receipt, not an explanation |
| D · leave notebooks to the consumer repo | rely on `Hazard_modeling/Notebooks/*/m3/` | rejected — those notebooks answer the consumer question and import Hazard production code; they cannot show curation evidence, withheld units or KAT reproduction from Damage's side |

## Pressure tests the plan must survive

1. **Bundle shape differs.** Five current cells are `damage_curve_record_bundle.v2` (records at top level);
   three current cells and the TC-solar candidate are `v3` (everything nested under `pathways[0]`:
   `hazard_axis`, `curve_records`, `failure_unit_coverage`, `selector_logic`, `exposure_contract`). The runtime
   template needs one loader that resolves both shapes, or the eight new notebooks will fork immediately.
2. **Not every cell has a runtime curve.** `hail_wind` is a fail-closed model-v0.1 scaffold (`curve_records: []`,
   `NO_RUNTIME_CURVE`). Its runtime notebook must demonstrate the *withholding* — load, assert zero records,
   run its KATs — not invent a plot.
3. **Not every lead artifact is canonical.** `tropical_cyclone_wind_solar` has no `current/`; its lead is the
   noncanonical model-v2.1/docs-r1 candidate that Hazard serves below crown. A notebook over a proposal must
   carry a NONCANONICAL banner and must never be linked as the cell's current pin.
4. **Known-answer files are uneven.** KAT JSONs exist in `current/` for `hail_solar`, `wildfire_solar`,
   `flood_wind`, `wildfire_wind`, `tropical_cyclone_wind_wind`; none is published in `current/` for
   `flood_solar`, `wind_tornado_wind`, `strong_wind_solar`. A runtime notebook reproduces KATs where they exist
   and says plainly when none is published — it does not manufacture one. Publishing a KAT is a curation act
   for the owner (gate G4).
5. **Path welding is what broke the last set.** Resolve the artifact through the machine-readable index (cell
   id → path → SHA-256) and verify the SHA in the notebook; never through a folder path copied from a
   deliverable tree, and never from `docs/source_drops/extracted/`.
6. **Evaluators must not be re-implemented per notebook.** `scripts/reference_helpers/damage_curve_eval.py`
   already dispatches `logistic`, `piecewise_linear`, `wind_tornado_logistic_ratio` and
   `thresholded_logistic_demand`, and derives the strong-wind demand ratio; notebooks import it. Where a form is
   unsupported — or would be evaluated wrongly, as with `wildfire_solar`'s exact categorical states that must
   not be interpolated — the notebook shows the artifact's own formula / lookup rule, evaluates with a clearly
   labelled local helper, and records the evaluator gap as a plan follow-on.
7. **Cross-repo boundary.** Hazard consumer code is *referenced* (path + pinned id) for context, never imported;
   the consumer repo is a gitignored local symlink and a fresh clone must still execute every notebook.
8. **Notebooks never author or publish.** No notebook edits a curve artifact, a workbook, a KAT file, the
   artifact index or GCS. A finding routes to the cell's evidence memo / proposal path.

## Verdict

- Every governed cell gets a `00_curve_curation_walkthrough` + `01_runtime_curve_walkthrough` pair under
  `notebooks/<hazard>/<asset>/`, built **one cell at a time**, hurricane pair first (as the audit recommended),
  after the two broken pairs are repaired against their current pins.
- Shared mechanics (repo-root discovery, index lookup, SHA check, v2/v3 shape resolver, KAT runner) live in one
  small helper beside the notebooks so the next path migration cannot break ten notebooks at once
  (recommendation; owner gate G2).
- Proposal-only and zero-curve cells get notebooks that show exactly what the artifact *withholds*, labelled
  as such (owner gate G3).
- The plan does not amend the cell-package standard: notebooks remain companions linked from each cell README,
  not a required package file. Making them required is a separate owner decision.

## Owner gates carried into the plan

`G1` approve the plan (`proposed → active`) · `G2` shared helper module vs per-notebook loader cell ·
`G3` runtime notebooks for the proposal-only / zero-curve cells · `G4` publish KAT files for the three current
cells that lack one. CI does not exist in this repo (`.github/` is absent); headless execution stays a manual
gate until a separate CI plan lands.

## Exit condition

This node is `settled` when G1–G4 are answered and recorded as `NB-D*` rows in the plan's
[`decisions.md`](../../../plans/cell_notebook_coverage/decisions.md). The plan, not this node, tracks
execution.

## Related

- Plan of record: [`docs/plans/cell_notebook_coverage/`](../../../plans/cell_notebook_coverage/README.md)
- Trigger: [2026-08-18 architecture & flow review](../2026-08-18_damage_modeling_architecture_and_flow.md) (Part IV gaps)
- Notebook home and roles: [`notebooks/README.md`](../../../../notebooks/README.md)
- Current pins: [`MACHINE_READABLE_ARTIFACTS.md`](../../../contracts/MACHINE_READABLE_ARTIFACTS.md)
- Cell inventory: [`docs/cells/README.md`](../../../cells/README.md) · [`VERSION_REGISTRY.md`](../../../cells/VERSION_REGISTRY.md)
- Coverage sequencing precedent (one cell at a time): [`hazard_asset_coverage` plan](../../../plans/hazard_asset_coverage/README.md)
