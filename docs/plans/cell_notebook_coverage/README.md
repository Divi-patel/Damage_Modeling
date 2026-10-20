<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: proposed
scope: Plan of record — repair the two existing companion-notebook pairs against their current pins, then give every governed hazard × asset cell a curation + runtime notebook pair, one cell at a time, hurricane first, with a shared loader, a coverage gate and a checkable done-when.
-->

# Cell notebook coverage plan

> **Plan of record — repair first, then one cell at a time, hurricane pair first.** Ten cells are
> structurally governed; two have companion notebooks and both of those fail in their first code cell
> (verified 2026-08-26). This plan takes the library to **10/10 cells with an executing `00` + `01` pair**
> without touching any curve, pin, workbook or contract. Reasoning:
> [`discussion/cell_notebook_coverage/`](../../extra/discussion/cell_notebook_coverage/README.md).
> Status `proposed` until the owner answers gate G1.

## Outcome first

When this plan is done:

```text
notebooks/
  <hazard>/<asset>/
    README.md
    00_curve_curation_walkthrough.ipynb     evidence → anchors → parameters → selectors/conditioners/exposure → value → capability
    01_runtime_curve_walkthrough.ipynb      index pin → SHA → load → evaluate → plot → KATs → consumer-style assembly
    outputs/                                saved review figures
```

exists for all ten cells; every notebook executes headlessly top-to-bottom from a fresh clone against the
repository-current pin (or an explicitly labelled noncanonical / withheld artifact); every cell README links
its pair; and a repository test keeps the coverage matrix, links and pins honest.

Nothing about the science changes. A notebook that finds a curve defect routes the finding to the cell's
evidence memo or proposal path; it never edits the artifact.

## Scope and non-scope

| In scope | Out of scope |
|---|---|
| repairing `hail/solar` and `flood/solar` loaders, prose and outputs against `docs_r7` / `docs_r4` | changing any curve record, parameter, selector, value profile or capability |
| a shared notebook helper (root discovery · index lookup · SHA check · v2/v3 shape resolver · KAT runner) and two template notebooks | a `src/` runtime API for consumers (separate system work) |
| eight new `00`+`01` pairs, one cell at a time | notebooks for archived model versions (read for narrative only) |
| per-cell `README.md`, per-hazard `README.md`, the `notebooks/README.md` coverage matrix, cell-README "Companion notebooks" sections | amending the cell-package standard to *require* notebooks (owner decision) |
| `tests/test_notebook_coverage.py` structure gate + a manual headless-execution runner | CI wiring — `.github/` does not exist; a CI plan is separate |
| optional close-out `notebooks/00_library_overview.ipynb` | EAL / PML / VaR / TVaR anywhere in this repo |

## Current state (measured 2026-08-26)

| Cell | Repo-current runtime | Lead artifact the notebooks read | Bundle | Records / failure units | KAT in `current/` | Hazard consumer | Notebooks |
|---|---|---|---|---|---|---|---|
| `hail_solar` | canonical model v1.0 · runtime docs r7 | `current/hail_solar__model_v1_0__docs_r7__curve_artifact.json` | v2 | 3 / 1 | yes | hail × solar CONUS (`HAIL_SOLAR_DEFAULT_3P2_GBS` selected) | `00`+`01` — **broken loader** |
| `flood_solar` | canonical v1.0 · r4 | `current/flood_solar__model_v1_0__docs_r4__curve_artifact.json` | v2 | 8 / 8 | **none** | flood × solar CONUS (7 units, `FS_FOUND` excluded) | `00`+`01` — **broken loader** |
| `wind_tornado_wind` | canonical v1.0 · r4 (+ noncanonical v2.0) | `current/wind_tornado_wind__model_v1_0__docs_r4__curve_artifact.json` | v2 | 5 / 5 | **none** (v2 proposal has one) | convective wind × wind farm (`WIND_TORNADO_WIND_V1`) | none |
| `strong_wind_solar` | canonical v1.0 · r3 (+ noncanonical v2.0) | `current/strong_wind_solar__model_v1_0__docs_r3__curve_artifact.json` | v2 | 5 / 5 | **none** (v2 proposal has one) | convective wind × solar (`STRONG_WIND_SOLAR_V1`) | none |
| `wildfire_solar` | canonical screening v1.0 · r3 | `current/wildfire_solar__model_v1_0__docs_r3__curve_artifact.json` | v2 | 10 / 10 (categorical FSim states) | yes | wildfire × solar CONUS (`WILDFIRE_SOLAR_FSIM_SCREENING_V1`) | none |
| `flood_wind` | canonical partial screening v1.0 · r1 | `current/flood_wind__model_v1_0__docs_r1__curve_artifact.json` | v3 (1 pathway) | 1 source-native substation atom / 15 units, rest withheld | yes | none at grid support (flood is solar-only there) | none |
| `wildfire_wind` | canonical Tier-4 partial screening v1.0 · r1 | `current/wildfire_wind__model_v1_0__docs_r1__curve_artifact.json` | v3 (1 pathway) | 2 exact electrical units / 12, rest withheld | yes | none at grid support | none |
| `tropical_cyclone_wind_wind` | canonical v1.2 · r2 tower-only | `current/tropical_cyclone_wind_wind__model_v1_2__docs_r2__curve_artifact.json` | v3 (1 pathway) | Jaimes selectors + canonical-5-MW tower proxy; 16 % TIV covered, 84 % withheld / 10 units | yes | hurricane × wind farm (`…JAIMES_TOWER_SCREENING_V1_2`) | none |
| `tropical_cyclone_wind_solar` | **no canonical runtime**; lead = noncanonical v2.1 · r1 (v0.1 / v1.0 / v2.0 preserved) | `proposed/tropical_cyclone_wind_solar__model_v2_1__docs_r1__curve_artifact.json` | v3 (1 pathway + site-facility axis) | 10 records / 11 units | yes (v2.1) | hurricane × solar CONUS served **below crown** on the proposal | none |
| `hail_wind` | **no runtime**; model v0.1 · docs r2 fail-closed scaffold | `proposed/hail_wind__model_v0_1__docs_r1__curve_artifact.json` | v1 | 0 / 11 · `NO_RUNTIME_CURVE` | yes (v0.1, tests withholding) | none | none |

Sources: [`MACHINE_READABLE_ARTIFACTS.md`](../../contracts/MACHINE_READABLE_ARTIFACTS.md) (pins), each cell's
`current/` and `proposed/` folders (records, KATs), the Hazard consumer code paths listed per cell in
[`cell_work_packages.md`](cell_work_packages.md). The "broken loader" finding is reproduced in
[`notebook_contract.md`](notebook_contract.md#why-the-existing-pairs-fail).

## Decisions fixed for this plan

| Decision | Contract | Register |
|---|---|---|
| Repair before build | the two existing pairs are re-pointed, re-executed and reconciled to `docs_r7` / `docs_r4` before any new cell starts | [`NB-D01`](decisions.md#nb-d01--repair-before-build) |
| One cell at a time, hurricane pair first | order: repair → scaffolding → `tropical_cyclone_wind_wind` → `tropical_cyclone_wind_solar` → `wildfire_solar` → `strong_wind_solar` → `wind_tornado_wind` → `flood_wind` → `wildfire_wind` → `hail_wind` | [`NB-D02`](decisions.md#nb-d02--one-cell-at-a-time-hurricane-pair-first) |
| Resolve artifacts through the index, never a copied path | the runtime notebook reads `docs/contracts/machine_readable_artifact_index.json`, prints and verifies SHA-256; proposal cells name their `proposed/` file explicitly with a NONCANONICAL banner | [`NB-D03`](decisions.md#nb-d03--resolve-through-the-artifact-index-and-verify-the-sha) |
| One shared helper beside the notebooks | `notebooks/_shared/` holds root discovery, index lookup, SHA check, v2/v3 resolver and KAT runner; notebooks import it by path — *recommended, owner gate G2* | [`NB-D04`](decisions.md#nb-d04--one-shared-helper-beside-the-notebooks) |
| Import the repo's evaluators | `scripts/reference_helpers/damage_curve_eval.py` evaluates supported forms; unsupported forms are shown from the artifact's own formula with a labelled local helper and logged as an evaluator gap | [`NB-D05`](decisions.md#nb-d05--import-the-repository-evaluators) |
| Current pin only in `01`; proposals only as links in `00` | a runtime notebook evaluates exactly one artifact — the pin (or, for cells without one, the named lead proposal); v2 proposals for cells that already have v1 appear only as "what's next" links | [`NB-D06`](decisions.md#nb-d06--the-runtime-notebook-evaluates-exactly-one-artifact) |
| Withholding is a result | zero-curve and partial-screening notebooks show what is withheld and why, and run the KATs that assert it | [`NB-D07`](decisions.md#nb-d07--withholding-is-a-result-to-show-not-a-reason-to-skip) |
| Notebooks never author or publish | no notebook writes outside its `outputs/`; findings route to evidence memos / proposals | [`NB-D08`](decisions.md#nb-d08--notebooks-never-author-or-publish) |

## The notebook contract (summary)

The full per-section contract, loader rule, figure rule and the per-cell-type variants are in
[`notebook_contract.md`](notebook_contract.md). In one screen:

| Role | Must show | Must not |
|---|---|---|
| `00_curve_curation_walkthrough` | cell identity and scope · failure-unit coverage tree · evidence classes and what each may support · x-axis decision · curve-form decision · anchors → parameters (fit or interpolation) with the parameter-tier table · selectors / conditioners / exposure · value link and cap · capability and open seams · reviewer checklist | re-derive a parameter that differs from the artifact without saying so; present a proposal as current |
| `01_runtime_curve_walkthrough` | index pin → path → SHA-256 (verified) · identity block (damage code · model · docs revision · schema) · failure units and coverage roles · every curve record evaluated and plotted on its native axis · selector / conditioner / exposure behaviour · KAT reproduction (or "none published") · consumer-style conditional-loss assembly with an explicit example value basis · capability flags | EAL / PML / VaR / TVaR; reading `docs/source_drops/extracted/`, GCS or the Hazard repo; writing anything outside `outputs/` |
| `02_derivation_or_fit_check` *(optional)* | reproduce fitted parameters from the workbook / dossier anchors | — |
| `03_consumer_integration_example` *(optional, only where a Hazard consumer exists)* | how the consumer calls the artifact for a concrete asset / value basis | annual metrics |

## Execution sequence

### Phase 0 · Repair the two existing pairs (`hail_solar`, `flood_solar`)

- [ ] Re-point both loaders from the removed `docs/damage_curves/…docs_r5|r3…` path to the index pins
  (`hail_solar@model_v1_0__docs_r7`, `flood_solar@model_v1_0__docs_r4`); root discovery keys on `AGENTS.md` +
  `docs/cells`.
- [ ] Re-execute all four notebooks headlessly; diff every printed identity, count and parameter against the
  r7 / r4 artifacts; rewrite prose that still describes r5 / r3 fields.
- [ ] Regenerate `outputs/` figures; delete figures no longer produced.
- [ ] Update `notebooks/hail/solar/README.md`, `notebooks/flood/solar/README.md`, the cell READMEs' "Companion
  notebooks" sections; record the repair in the plan's `notes` and in task history.
- [ ] Gate: both pairs execute from a fresh clone; the `notebooks/README.md` matrix shows them `executing`.

### Phase 1 · Shared scaffolding

- [ ] `notebooks/_shared/repo_paths.py` (or the owner's alternative under G2): `find_repo_root()`,
  `load_artifact_index()`, `resolve_cell(cell_id) -> (path, consumer_pin, sha256)`, `verify_sha256()`,
  `records_of(artifact)` (v2 top-level / v3 `pathways[*]`), `run_known_answers(artifact, kat)`.
- [ ] `notebooks/_templates/00_curve_curation_walkthrough.ipynb` and `01_runtime_curve_walkthrough.ipynb`
  carrying the contract's section headings and the loader cell; `notebooks/_templates/README.md`.
- [ ] `tests/test_notebook_coverage.py`: every `notebooks/<h>/<a>/` folder is listed in the matrix and in its
  cell README; every runtime notebook's declared pin resolves in the index; every referenced artifact path
  exists; no notebook source contains `docs/damage_curves/` or `source_drops/extracted`.
- [ ] `scripts/reference_helpers/execute_notebooks.py`: headless `nbconvert --execute` over every notebook,
  outputs to a temp dir, non-zero exit on any failure (manual gate until CI exists).
- [ ] Gate: tests pass with the two repaired pairs; runner passes.

### Phase 2 · Hurricane pair (the audit's first recommendation)

- [ ] `tropical_cyclone_wind_wind` (current v1.2 / r2): `00` walks the correction arc v1.0 → v1.1 → v1.2
  from `CHANGELOG.json` and the archived artifacts (read-only), the Jaimes source selectors, the
  3.3 MW → canonical-5 MW tower route and why 84 % of TIV is withheld; `01` loads the pin, evaluates the
  tower record, reproduces the r2 KATs, shows the same-unit value rule.
- [ ] `tropical_cyclone_wind_solar` (noncanonical v2.1 / r1, gate G3): NONCANONICAL banner; `00` explains
  why the strict gate stayed NO-GO and what the owner-authorized synthetic-T4 candidate adds; `01` evaluates
  the ten records, the named 100 %-physical-value plant assembly and loss per kWdc, reproduces the v2.1 KATs,
  and names Hazard's below-crown consumption.
- [ ] Gate: both execute; cell READMEs link the pairs; matrix updated.

### Phase 3 · Remaining canonical v2-bundle cells

- [ ] `wildfire_solar` — categorical FSim class states, exact tables, no interpolation, screening flags.
- [ ] `strong_wind_solar` — 3-s gust → effective demand ratio `R_eff`, thresholded logistic, fixed-tilt /
  tracker selectors; the v2.0 proposal appears only as a "what's next" link.
- [ ] `wind_tornado_wind` — hub-height gust → IEC speed ratio, per-unit logistic ratio curves, the default
  structural aggregate flag; v2.0 proposal as link only.
- [ ] Gate per cell before the next starts.

### Phase 4 · Partial-screening v3 cells

- [ ] `flood_wind` — one FEMA Hazus-MH 2.1 whole-substation atom; every component / wind unit shown as
  withheld with its reason code; same-substation value / exposure rule.
- [ ] `wildfire_wind` — two exact FSim-state electrical units; all other units withheld; mandatory
  source / assumption acknowledgement.
- [ ] Gate per cell.

### Phase 5 · Zero-curve cell

- [ ] `hail_wind` — `00` explains the evidence gate (seven sources, nine claims, no same-blade economic
  atom); `01` loads the v0.1 artifact, asserts `curve_records == []` and `NO_RUNTIME_CURVE`, runs the KATs
  that test the withholding.

### Phase 6 · Close-out

- [ ] `notebooks/README.md` matrix reads 10/10 `executing`; per-hazard READMEs complete.
- [ ] Optional `notebooks/00_library_overview.ipynb` over the artifact index.
- [ ] `AGENTS.md` and `docs/README.md` rows updated; task-history handoff written.
- [ ] Plan → `done`; discussion node → `settled`; follow-ons (KAT publication, evaluator gaps, CI) filed as
  their own bounded items.

## Validation gates

- every notebook executes headlessly top-to-bottom in `.venv` (`python3.12`, `nbconvert`) from a fresh
  clone with no dependence on `docs/source_drops/extracted/`, GCS or the Hazard repo;
- every runtime notebook prints `damage_code_id`, semantic model version, docs revision, schema, artifact
  path and a SHA-256 that matches the artifact index (current cells) or carries a NONCANONICAL / WITHHELD
  banner naming the exact proposed file (proposal cells);
- KATs are reproduced wherever a KAT file is published; otherwise the notebook states that none is;
- no notebook computes EAL / PML / VaR / TVaR or writes outside its `outputs/`;
- every cell README has a "Companion notebooks" section; `notebooks/README.md` lists every notebook;
- `tests/test_notebook_coverage.py` passes; the Markdown link-check count over `docs/`, `notebooks/`,
  `AGENTS.md`, `README.md` does not rise above the 2026-08-26 baseline (1,411 links, 90 pre-existing broken);
- every saved figure has a caption defining axes, units, colours and whether a value is current, proposed or
  withheld.

## Done when

All ten cells have an executing `00` + `01` pair that a first-time reader can run from a fresh clone; each
pair is linked from its cell README and the coverage matrix; each runtime notebook verifies its pin and
reproduces its published KATs; the structure test and the manual runner pass; and nothing in `docs/cells/`,
`docs/contracts/` or any workbook changed because of this plan.

## Owner gates (open)

| Gate | Question | Recommendation |
|---|---|---|
| G1 | Approve this plan (`proposed → active`)? | approve; Phase 0 is repair-only and carries no science risk |
| G2 | Shared helper `notebooks/_shared/` vs a loader cell copied into every notebook? | shared helper — the copied cell is exactly what broke the current pairs |
| G3 | Build runtime notebooks for the proposal-only (`tropical_cyclone_wind_solar`) and zero-curve (`hail_wind`) cells? | yes, labelled — TC solar is consumed below crown today; the zero-curve walkthrough is the honest coverage record |
| G4 | Publish KAT files in `current/` for `flood_solar`, `wind_tornado_wind`, `strong_wind_solar`? | owner's curation call; until then the notebooks state "none published" |

## Connected work

- Reasoning: [`discussion/cell_notebook_coverage/`](../../extra/discussion/cell_notebook_coverage/README.md)
- Per-cell packages: [`cell_work_packages.md`](cell_work_packages.md) · contract: [`notebook_contract.md`](notebook_contract.md)
- Registers: [`decisions.md`](decisions.md) · [`assumptions.md`](assumptions.md)
- Trigger: [2026-08-18 architecture & flow review](../../extra/discussion/2026-08-18_damage_modeling_architecture_and_flow.md)
- Notebook home: [`notebooks/README.md`](../../../notebooks/README.md)
- Pins: [`MACHINE_READABLE_ARTIFACTS.md`](../../contracts/MACHINE_READABLE_ARTIFACTS.md) · cells: [`docs/cells/README.md`](../../cells/README.md)
- Sequencing precedent: [`hazard_asset_coverage`](../hazard_asset_coverage/README.md) (D-002 one pair at a time)
- Evaluators: [`damage_curve_eval.py`](../../../scripts/reference_helpers/damage_curve_eval.py) · [`validate_runtime_contracts.py`](../../../scripts/reference_helpers/validate_runtime_contracts.py)
- Test pattern to mirror: [`tests/test_curve_request_guides.py`](../../../tests/test_curve_request_guides.py)
