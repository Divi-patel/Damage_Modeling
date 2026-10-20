<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: proposed
scope: Assumptions and watchlist for the cell notebook coverage plan (NB-A*), each with its current treatment and the trigger that reopens it.
-->

# Cell notebook coverage — assumptions and watchlist

Format mirrors [`hazard_asset_coverage/ASSUMPTIONS.md`](../hazard_asset_coverage/ASSUMPTIONS.md).

| ID | Assumption or watch item | Current treatment | Change trigger |
|---|---|---|---|
| NB-A01 | `docs/contracts/machine_readable_artifact_index.json` is the authoritative statement of each current cell's runtime pin | notebooks resolve current cells only through it and verify the SHA | the index is replaced by a published (GCS) index — then the helper resolves that instead |
| NB-A02 | Notebooks are companions; standard 02 does not require them | link from each cell README; no standards change in this plan | owner decides to make notebooks a required package file (NB-D09) |
| NB-A03 | Notebooks never author, publish or mutate governed objects | writes only under `outputs/`; findings route to evidence memos / proposals | never — this is a boundary, not an assumption to relax |
| NB-A04 | The execution environment is the repo `.venv` (`python3.12`, `jupyterlab`, `nbconvert 7.x`, `matplotlib`, `pandas`, `numpy`, `openpyxl`) | `requirements.txt` already lists these; no new dependency | a notebook needs a package not in `requirements.txt` — add it there first, never inline `pip install` |
| NB-A05 | `notebooks/**/outputs/` is tracked (the root-anchored `/outputs/` ignore does not cover it) | keep figures small (PNG, ≤ ~300 KB each); delete figures no longer produced | repository size becomes a concern — switch to regenerated-on-execute with a `.gitignore` entry |
| NB-A06 | Archived and proposal artifacts may be read for narrative in `00`; only the lead artifact is evaluated in `01` | NB-D06 | owner asks for a proposal-comparison notebook — that is a separate `02`/`03`-style notebook, not a change to `01` |
| NB-A07 | Hazard consumer code is context, not a dependency | referenced by repo-relative path and pinned id in prose; never imported | a shared consumer library is published — the `03` notebook may then import it |
| NB-A08 | KAT files exist for five current cells and are absent for three (`flood_solar`, `wind_tornado_wind`, `strong_wind_solar`) as of 2026-08-26 | notebooks reproduce where published and state absence otherwise | owner publishes KATs (gate G4) — the runtime notebook is re-executed and the matrix row updated |
| NB-A09 | Bundle v2 and v3 differ only in where records live (top level vs `pathways[*]`) for the purpose of evaluation and plotting | one resolver in the shared helper | a v4 schema or a multi-pathway v3 artifact appears — extend the resolver and re-run the structure test |
| NB-A10 | The evaluator in `scripts/reference_helpers/damage_curve_eval.py` dispatches `logistic`, `piecewise_linear`, `wind_tornado_logistic_ratio` and `thresholded_logistic_demand` (plus `strong_wind_solar_r_eff`); it has no exact categorical-state lookup (needed by `wildfire_solar`, whose points must not be interpolated) and bundle-v3 pathway record forms are unverified against it | unsupported forms use a titled local helper (for wildfire, mirror `validate_runtime_contracts.exact_state_value`) and are logged as evaluator gaps | the evaluator gains the form — remove the local helper and re-execute |
| NB-A11 | The 2026-08-26 link-check baseline over `docs/`, `notebooks/`, `AGENTS.md`, `README.md` is 1,411 links / 90 broken (pre-existing) | the gate is "the count does not rise", not "zero" | a separate link-debt pass lowers the baseline — update the number here |
| NB-A12 | CI does not exist (`.github/` absent) | headless execution is a manual runner (NB-D10) | a CI plan lands — wire the runner and the structure test into it |

## Watchlist

- Do not let "10/10 cells have notebooks" be read as "10/10 cells have runtime curves"; the matrix carries the
  coverage-plan counting rule (canonical · partial screening · noncanonical proposal · withheld scaffold) on
  every row.
- Do not let a repaired or new notebook quietly become the place a parameter is "corrected"; the artifact is
  the authority and the notebook reports disagreement as a finding.
- Watch the two v2 proposals (`strong_wind_solar`, `wind_tornado_wind`): if either is promoted while this plan
  runs, its `01` is re-pointed by the index change alone and re-executed — no notebook edit should be needed
  beyond prose.
