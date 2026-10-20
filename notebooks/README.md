<!--
author: Divi-patel (2026-06-25) · revision 2026-08-26 owner-directed (Divy) · agent-drafted
created: 2026-06-25
updated: 2026-08-26
status: active
scope: Home of the companion notebooks — roles, folder shape, the loader rule, the 10-cell coverage matrix with execution state, and the rules. Coverage plan: docs/plans/cell_notebook_coverage/.
-->

# notebooks/ — damage-curve walkthroughs and derivation companions

Runnable notebooks live here as companions to the formal cell packages under
[`docs/cells/`](../docs/cells/README.md). The docs remain the source of truth for the shipped curve artifact;
notebooks are for inspection, fitting checks, evidence walkthroughs, and consumer-facing examples. A notebook
**reads** a pinned artifact; it never authors, edits or publishes one.

> **State on 2026-08-26.** Two of ten cells have a notebook pair, and **both pairs fail in their first code
> cell** — their loader targets the removed `docs/damage_curves/…` tree and pins `docs_r5` / `docs_r3`
> artifacts that now exist only in the gitignored `docs/source_drops/extracted/` mirror. Repair (Phase 0) and
> the remaining eight cells are planned one cell at a time in
> [`docs/plans/cell_notebook_coverage/`](../docs/plans/cell_notebook_coverage/README.md); every notebook
> follows the [companion-notebook contract](../docs/plans/cell_notebook_coverage/notebook_contract.md).

## Organization

Use the same shape as the Hazard notebooks:

```text
notebooks/
  README.md                       this file — roles, loader rule, coverage matrix
  _shared/                        (Phase 1) repo_paths.py — root discovery · index lookup · SHA check · v2/v3 resolver · KAT runner
  _templates/                     (Phase 1) blank 00 / 01 notebooks carrying the contract's sections
  <hazard>/
    README.md
    <asset>/
      README.md                   order · source artifacts · execution state · covers / does not cover
      00_curve_curation_walkthrough.ipynb
      01_runtime_curve_walkthrough.ipynb
      02_derivation_or_fit_check.ipynb          optional
      03_consumer_integration_example.ipynb     optional, only where a Hazard consumer exists
      outputs/                    saved review figures (tracked; keep them small)
```

Name folders by the cell id parts (`hail/solar/` for `hail_solar`, `tropical_cyclone_wind/wind/` for
`tropical_cyclone_wind_wind`). This keeps the path stable when a cell later grows from one failure-unit curve
to multiple failure-unit records.

## Notebook roles

| Prefix | Role | Boundary |
|---|---|---|
| `00_curve_curation_walkthrough` | Explain how evidence is curated into anchors, fitted/interpolated parameters, selectors, conditioners, exposure/value logic, and capability gates. | Teaching/QA view of the cell dossier; source of truth remains the docs package. |
| `01_runtime_curve_walkthrough` | Resolve the pinned artifact through the artifact index, verify its SHA, evaluate the curve, show selector / conditioner / exposure logic, reproduce the known-answer tests, show a consumer-style assembly. | M3 severity only; no hazard frequency or EAL/PML. |
| `02_derivation_or_fit_check` | Reproduce or audit fitted parameters from source anchors/workbooks. | Evidence and fit QA; not the runtime contract. |
| `03_consumer_integration_example` | Show how a Hazard M3 consumer should call the artifact for a concrete asset/value basis. | Conditional loss assembly only unless explicitly paired with Hazard outputs. |

## Loader rule (why the first pairs broke, and how the next ones will not)

```text
repo root      = first ancestor with AGENTS.md AND docs/cells
current cell   → docs/contracts/machine_readable_artifact_index.json → path · consumer_pin · sha256 → verify SHA
proposal cell  → docs/cells/<cell>/proposed/<file> named explicitly + NONCANONICAL / WITHHELD banner
records        v2: artifact["curve_records"]   ·   v3: pathways[*]["curve_records"]
never          docs/source_drops/extracted/ · GCS · the Hazard repo · a folder path copied from a deliverable tree
```

Full rules (identity block, evaluators, KATs, figures, execution, boundary):
[`notebook_contract.md`](../docs/plans/cell_notebook_coverage/notebook_contract.md).

## Coverage matrix (10 cells · measured 2026-08-26)

| Cell | Repository-current runtime | Lead artifact the notebooks read | Notebooks | Execution state | Package |
|---|---|---|---|---|---|
| [`hail_solar`](../docs/cells/hail_solar/README.md) | canonical model v1.0 · runtime docs r7 | `current/hail_solar__model_v1_0__docs_r7__curve_artifact.json` | [`hail/solar/00`](hail/solar/00_curve_curation_walkthrough.ipynb) · [`01`](hail/solar/01_runtime_curve_walkthrough.ipynb) | **broken — loader** (pins r5, removed path) | WP-0a |
| [`flood_solar`](../docs/cells/flood_solar/README.md) | canonical v1.0 · r4 | `current/flood_solar__model_v1_0__docs_r4__curve_artifact.json` | [`flood/solar/00`](flood/solar/00_curve_curation_walkthrough.ipynb) · [`01`](flood/solar/01_runtime_curve_walkthrough.ipynb) | **broken — loader** (pins r3, removed path) | WP-0b |
| [`tropical_cyclone_wind_wind`](../docs/cells/tropical_cyclone_wind_wind/README.md) | canonical v1.2 · r2 tower-only partial screening | `current/tropical_cyclone_wind_wind__model_v1_2__docs_r2__curve_artifact.json` | none | — | WP-2 |
| [`tropical_cyclone_wind_solar`](../docs/cells/tropical_cyclone_wind_solar/README.md) | **no canonical runtime**; noncanonical v2.1 · r1 lead | `proposed/tropical_cyclone_wind_solar__model_v2_1__docs_r1__curve_artifact.json` | none | — | WP-3 (gate G3) |
| [`wildfire_solar`](../docs/cells/wildfire_solar/README.md) | canonical screening v1.0 · r3 | `current/wildfire_solar__model_v1_0__docs_r3__curve_artifact.json` | none | — | WP-4 |
| [`strong_wind_solar`](../docs/cells/strong_wind_solar/README.md) | canonical v1.0 · r3 (+ noncanonical v2.0 proposal) | `current/strong_wind_solar__model_v1_0__docs_r3__curve_artifact.json` | none | — | WP-5 |
| [`wind_tornado_wind`](../docs/cells/wind_tornado_wind/README.md) | canonical v1.0 · r4 (+ noncanonical v2.0 proposal) | `current/wind_tornado_wind__model_v1_0__docs_r4__curve_artifact.json` | none | — | WP-6 |
| [`flood_wind`](../docs/cells/flood_wind/README.md) | canonical partial screening v1.0 · r1 | `current/flood_wind__model_v1_0__docs_r1__curve_artifact.json` | none | — | WP-7 |
| [`wildfire_wind`](../docs/cells/wildfire_wind/README.md) | canonical Tier-4 partial screening v1.0 · r1 | `current/wildfire_wind__model_v1_0__docs_r1__curve_artifact.json` | none | — | WP-8 |
| [`hail_wind`](../docs/cells/hail_wind/README.md) | **no runtime**; model v0.1 · docs r2 fail-closed scaffold | `proposed/hail_wind__model_v0_1__docs_r1__curve_artifact.json` | none | — | WP-9 (gate G3) |

"Notebooks exist" is not "a runtime curve exists": the runtime column carries the coverage plan's counting
rule (canonical · partial screening · noncanonical proposal · withheld scaffold) on every row. Work-package
details: [`cell_work_packages.md`](../docs/plans/cell_notebook_coverage/cell_work_packages.md).

## Real Estate proposal notebooks (from `cell/real-estate`, merged 2026-10-19)

Jung A Lim's five Real Estate cells are **noncanonical proposals** (no current runtime); their notebooks read
the proposed artifact named explicitly, per the proposal-cell loader rule above. They sit outside the 10-cell
matrix measured on 2026-08-26; their execution state has not been re-measured against the notebook contract.

| Cell | Notebook | Purpose |
|---|---|---|
| `flood_real_estate` | [`flood/real_estate/00_curve_curation_walkthrough.ipynb`](flood/real_estate/00_curve_curation_walkthrough.ipynb) | Curation walkthrough for the model v0.2 proposal: FEMA Hazus depth-damage functions per building (NACCS for retail coastal), NFIP claims check, first-floor height. |
| `flood_real_estate` | [`flood/real_estate/01_runtime_curve_walkthrough.ipynb`](flood/real_estate/01_runtime_curve_walkthrough.ipynb) | Runtime walkthrough: reads the proposed artifact and calls the curves through the cell's reference evaluator. |
| `tropical_cyclone_wind_real_estate` | [`tropical_cyclone_wind/real_estate/00_curve_curation_walkthrough.ipynb`](tropical_cyclone_wind/real_estate/00_curve_curation_walkthrough.ipynb) | Curation walkthrough for the model v0.2 proposal: FEMA Hazus hurricane building-loss tables by building type and terrain class, variant sensitivity. |
| `tropical_cyclone_wind_real_estate` | [`tropical_cyclone_wind/real_estate/01_runtime_curve_walkthrough.ipynb`](tropical_cyclone_wind/real_estate/01_runtime_curve_walkthrough.ipynb) | Runtime walkthrough: reads the proposed artifact and calls the curves through the cell's reference evaluator. |
| `convective_wind_real_estate` | [`convective_wind/real_estate/00_curve_curation_walkthrough.ipynb`](convective_wind/real_estate/00_curve_curation_walkthrough.ipynb) | Curation walkthrough for the model v0.1 proposal: EF-scale degrees of damage priced through the Hazus damage states; tornado and straight-line pathways; 96 mph straight-line onset; NRI check. |
| `convective_wind_real_estate` | [`convective_wind/real_estate/01_runtime_curve_walkthrough.ipynb`](convective_wind/real_estate/01_runtime_curve_walkthrough.ipynb) | Runtime walkthrough: reads the proposed artifact and calls the curves through the cell's reference evaluator. |
| `hail_real_estate` | [`hail/real_estate/00_curve_curation_walkthrough.ipynb`](hail/real_estate/00_curve_curation_walkthrough.ipynb) | Curation walkthrough for the model v0.1 proposal: roof-cover hail thresholds by material times the roof's share of building cost; Tier-4 walls and windows; NRI check. |
| `hail_real_estate` | [`hail/real_estate/01_runtime_curve_walkthrough.ipynb`](hail/real_estate/01_runtime_curve_walkthrough.ipynb) | Runtime walkthrough: reads the proposed artifact and calls the curves through the cell's reference evaluator. |
| `wildfire_real_estate` | [`wildfire/real_estate/00_curve_curation_walkthrough.ipynb`](wildfire/real_estate/00_curve_curation_walkthrough.ipynb) | Curation walkthrough for the model v0.1 proposal: USFS Wildfire Risk to Communities home response by flame-length class; CAL FIRE same-fire factors for the warehouse and office; NRI check. |
| `wildfire_real_estate` | [`wildfire/real_estate/01_runtime_curve_walkthrough.ipynb`](wildfire/real_estate/01_runtime_curve_walkthrough.ipynb) | Runtime walkthrough: reads the proposed artifact and calls the curves through the cell's reference evaluator. |

## Rules

- Runtime notebooks read the canonical `*__curve_artifact.json` resolved through the artifact index; they do
  not copy curve parameters by hand and do not read from `docs/source_drops/extracted/`.
- Import the repository evaluators (`scripts/reference_helpers/damage_curve_eval.py`) for supported curve
  forms; an unsupported form is evaluated by a clearly titled local helper and logged as an evaluator gap.
- Mark assumptions explicitly, especially example value bases, exposure fractions, and placeholder adjustments.
- Do not compute EAL/PML/VaR in this repo unless the notebook is explicitly demonstrating a downstream Hazard
  integration. The damage layer owns `intensity → damage ratio`, not hazard frequency or financial metrics.
- Export important figures to the local `outputs/` folder so they can be reviewed outside Jupyter; write
  nothing anywhere else.
- Every notebook must execute headlessly top-to-bottom
  (`.venv/bin/jupyter nbconvert --to notebook --execute <notebook>`) from a fresh clone.
