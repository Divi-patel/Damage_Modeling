<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: proposed
scope: The per-notebook contract for damage_modeling companion notebooks — loader rule, required sections per role, figure rule, execution rule, and the variants per cell type (single-primary logistic · multi-unit depth ladder · categorical state tables · wind ratio/demand axes · v3 partial-screening pathways · zero-curve).
-->

# Companion-notebook contract

This is the contract every notebook under `notebooks/<hazard>/<asset>/` follows. It is written so a builder
can start a new cell's pair without reading the two existing pairs first, and so a reviewer can reject a
notebook that executes but explains nothing.

## Why the existing pairs fail

Executed headlessly on 2026-08-26 (`.venv/bin/jupyter nbconvert --to notebook --execute …`), both
`notebooks/hail/solar/01_runtime_curve_walkthrough.ipynb` and
`notebooks/flood/solar/00_curve_curation_walkthrough.ipynb` stop in cell 1:

```text
RuntimeError: Could not find damage_modeling repo root from current working directory.
```

The loader cell defines the root as "a folder containing `AGENTS.md` **and** `docs/damage_curves`", then
builds `CELL_DIR = docs/damage_curves/damage_curve_implementation/DAMAGE_CURVE_LIBRARY_V2_5_IMPLEMENTATION_HARDENED_DELIVERABLE/01_cells/<cell>/current`
and pins `hail_solar__model_v1_0__docs_r5` / `flood_solar__model_v1_0__docs_r3`. That tree was removed when
the repo moved to `docs/cells/`; the r5 / r3 files now exist only under the gitignored
`docs/source_drops/extracted/v2_5_implementation_hardened/`, so a fresh clone could never have run them.
The current pins are `docs_r7` and `docs_r4`. The lesson is the first rule below.

## Rule 1 · Loader

```text
find_repo_root()      walk up from cwd until AGENTS.md AND docs/cells exist
load_artifact_index() docs/contracts/machine_readable_artifact_index.json
resolve_cell(cell_id) → path · consumer_pin · sha256   (current cells)
verify_sha256(path)   must equal the index value; print both
records_of(artifact)  v2: artifact["curve_records"]; v3: [r for p in artifact["pathways"] for r in p["curve_records"]]
```

- Current cells resolve **only** through the index. Never through a folder path copied from a deliverable
  tree, never from `docs/source_drops/extracted/`, never from GCS, never from the Hazard repo.
- Cells with no current pin (`tropical_cyclone_wind_solar`, `hail_wind`) name their lead file explicitly
  (`docs/cells/<cell>/proposed/<file>`) and print a banner in the first Markdown cell **and** the first code
  cell output: `NONCANONICAL — proposal only; no artifact-index entry; not the cell's runtime pin` or
  `WITHHELD — model v0.1 fail-closed scaffold; no runtime curve`.
- The loader lives in one shared helper (`notebooks/_shared/repo_paths.py`, plan decision NB-D04, owner gate
  G2) imported by path from every notebook. If the owner prefers a per-notebook cell, the cell text is
  identical in every notebook and the structure test greps for drift.

## Rule 2 · Identity block (first output of every notebook)

Print, from the artifact itself: `cell_id` · `damage_code_id` · `semantic_damage_model_version` ·
`documentation_revision` · `schema_version` · `canonical_runtime_artifact` · artifact path (repo-relative) ·
SHA-256 · number of failure units · number of curve records · the consumer pin string from the index. The
identity block is what a reviewer compares against [`VERSION_REGISTRY.md`](../../cells/VERSION_REGISTRY.md).

## Rule 3 · Evaluators

Import `scripts/reference_helpers/damage_curve_eval.py`. `evaluate_curve_record` dispatches four forms —
`logistic`, `piecewise_linear`, `wind_tornado_logistic_ratio` (tornado D50 shift via
`context={"tornado_variant": True}`) and `thresholded_logistic_demand` — and `strong_wind_solar_r_eff` derives
the strong-wind demand ratio. For a `curve_form` the evaluator does not support, or a form it would evaluate
wrongly (the `wildfire_solar` records are stored as `piecewise_linear` points but must be read as **exact
categorical states, never interpolated** — mirror `validate_runtime_contracts.exact_state_value`), the notebook
(a) prints the artifact's own formula / lookup rule, (b) evaluates with a local helper whose cell is titled
`Local helper — not the repository evaluator`, and (c) records the gap in the plan's `notes` as an evaluator
follow-on. Bundle-v3 pathway records must have their `curve_form` checked against that dispatch before use. A
notebook never silently re-implements a supported form.

## Rule 4 · Known-answer tests

If `docs/cells/<cell>/{current|proposed}/known_answer_tests_*.json` exists for the evaluated artifact, the
runtime notebook loads it, evaluates every case, prints a pass/fail table and **asserts** all pass. If no KAT
file is published for the evaluated artifact, the notebook prints exactly that sentence; it does not invent
expected values. (As of 2026-08-26, `current/` has KATs for `hail_solar`, `wildfire_solar`, `flood_wind`,
`wildfire_wind`, `tropical_cyclone_wind_wind`; none for `flood_solar`, `wind_tornado_wind`,
`strong_wind_solar` — owner gate G4.)

## Rule 5 · Figures and outputs

- Figures save to `notebooks/<hazard>/<asset>/outputs/` with the notebook prefix (`00_`, `01_`) and a
  descriptive slug; nothing else is written anywhere.
- Every figure title/caption states: axis variable and unit, what each line/colour is, whether values are
  **current**, **proposed** or **withheld**, and the artifact identity (damage code + model + docs revision).
- Native axis only: hail in mm, flood in m of local depth above component datum, tornado as IEC speed ratio,
  strong wind as 3-s gust (mph) with the derived demand ratio shown alongside, wildfire as ordered FSim class
  states (bars/steps, not a smoothed line), TC wind on its pathway axis.

## Rule 6 · Execution

`.venv/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=300 <notebook>` must
succeed from any working directory inside the repo, on a fresh clone, with only `requirements.txt` installed.
Kernel name `python3`. No network. No environment variables. Runtime under two minutes per notebook.

## Rule 7 · Boundary

No EAL, PML, VaR, TVaR, annual frequency, portfolio accumulation or scenario benefit. A conditional-loss
example uses an **explicitly labelled example value basis** and says so in the cell title. Hazard consumer
code is referenced by path and pinned identifier for context; it is never imported.

## Required sections

### `00_curve_curation_walkthrough.ipynb`

| # | Section | Must contain |
|---|---|---|
| 0 | Title + how to read | cell, model version, docs revision; banner if proposal/withheld; link to the cell README, dossier and metadata spec |
| 1 | Cell identity and scope | hazard pathway, asset, exclusions (standard 02 §1 items 1–3) |
| 2 | Failure-unit coverage tree | primary / conditioner-only / secondary / DR≈0 / out-of-scope, from the artifact's `failure_units` and coverage roles — printed from the JSON, not retyped |
| 3 | Evidence classes | each source class and what it is allowed to support (from the dossier / source register); tier vocabulary |
| 4 | X-axis decision | the accepted axis, rejected alternatives, valid range, extrapolation policy — from `hazard_axis` |
| 5 | Curve-form decision | why this form (logistic · piecewise · state table · ratio · demand) and what it cannot express |
| 6 | Anchors → parameters | the interpreted anchors and the fit / interpolation that produced the shipped parameters; a plot of curve over anchors; for exact tables, the table itself with source rows |
| 7 | Parameter tiers | the `parameter_tier_table` rendered; what is evidence-backed vs engineered vs placeholder |
| 8 | Selectors · conditioners · exposure | which are fixed attributes, which are event-time state, which touch value; the artifact's `selector_logic`, `conditioner_logic`, `exposure_logic` / `exposure_contract` |
| 9 | Value link and cap | the value bucket, basis, `f_kind`, and the asymptotic cap arithmetic; what is withheld |
| 10 | Capability and open seams | `capability_declaration` rendered; open seams and their update triggers |
| 11 | Reviewer checklist | the questions a reviewer should be able to answer after this notebook |

### `01_runtime_curve_walkthrough.ipynb`

| # | Section | Must contain |
|---|---|---|
| 0 | Title + mental model | one paragraph: what enters (axis), what leaves (failure-unit DR), what the consumer adds |
| 1 | Resolve and load | Rule 1 + Rule 2 identity block |
| 2 | Failure units and coverage | table from the artifact; withheld units with reason codes (v3) |
| 3 | Evaluate every record | evaluator import (Rule 3); a DR table at named axis points per record |
| 4 | Plot | native-axis plot per record / per unit (Rule 5) |
| 5 | Axis transform (if any) | local depth ladder, IEC ratio, demand ratio, class mapping — shown as before/after numbers |
| 6 | Selectors · conditioners · exposure at runtime | which inputs change which curve; one worked example per kind |
| 7 | Known-answer tests | Rule 4 |
| 8 | Consumer-style assembly | `loss = Σ DR_u × value_u × exposure_u` on a labelled example value basis; the cap; what stays withheld |
| 9 | Capability flags | what the consumer may and may not compute from this artifact |
| 10 | What this teaches / cannot teach | limits, open seams, where the next evidence lands |

## Variants by cell type

| Cell type | Cells | What changes in `00` | What changes in `01` |
|---|---|---|---|
| Single primary failure unit, logistic, archetype selectors | `hail_solar` | fit view in logit space; archetype families | three archetype curves; stow conditioner as adjustment; module value bucket vs subsystem share |
| Multi-unit depth ladder, piecewise-linear | `flood_solar` | local-depth axis rejection of plant-level depth; per-unit ordinates derived vs assumed | datum ladder → local depth → per-unit DR → installed-share sum; excluded `FS_FOUND` velocity axis shown as excluded |
| Categorical source-native states, exact tables | `wildfire_solar` | why classes, not a continuous axis; screening-proxy grade | step/bar plots per unit; no interpolation; screening flags mandatory |
| Wind ratio / demand axes | `wind_tornado_wind` · `strong_wind_solar` | IEC class table / design-gust demand ratio derivation | hub-height or array-height input → ratio → per-unit curve; `include_in_default_structural_aggregate`; tracker/fixed selectors |
| v3 partial-screening pathway | `flood_wind` · `wildfire_wind` · `tropical_cyclone_wind_wind` | the pathway scope, the source-native atom, why other units are withheld | `pathways[0]` resolver; withheld table with reason codes; same-unit value / exposure rule; KATs |
| v3 noncanonical candidate | `tropical_cyclone_wind_solar` | strict gate NO-GO history; what the synthetic-T4 candidate adds and does not prove | NONCANONICAL banner; ten records; named 100 %-physical-value assembly; loss per kWdc; Hazard's below-crown use named |
| Zero-curve scaffold | `hail_wind` | the evidence gate and the seven-source / nine-claim addendum | WITHHELD banner; `curve_records == []`; KATs asserting withholding; no plot |

## Per-cell folder README

Each `notebooks/<hazard>/<asset>/README.md` has: notebook order table · **Source artifacts** (repo-relative
links to the pinned artifact, KAT file if any, dossier, metadata spec) · execution state line (`executing
YYYY-MM-DD` or `broken — see plan`) · what each notebook covers · what it does not cover. Each
`notebooks/<hazard>/README.md` lists its asset folders. The repository matrix lives in
[`notebooks/README.md`](../../../notebooks/README.md).

## Structure test (`tests/test_notebook_coverage.py`)

Mirrors [`tests/test_curve_request_guides.py`](../../../tests/test_curve_request_guides.py):

1. every `notebooks/<h>/<a>/` folder with `.ipynb` files appears in the `notebooks/README.md` matrix and in
   `docs/cells/<cell>/README.md` under "Companion notebooks";
2. every runtime notebook declares one `cell_id`; for current cells the index resolves it and the declared
   artifact filename equals the index path's basename; for proposal cells the declared `proposed/` file exists;
3. no notebook source contains `docs/damage_curves/` or `source_drops/extracted`;
4. every figure referenced by a notebook README exists under `outputs/`.

Headless execution is a separate manual runner (`scripts/reference_helpers/execute_notebooks.py`) until a CI
plan exists — `.github/` is absent in this repository.
