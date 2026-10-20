# Task context — cell notebook coverage plan

**Date:** 2026-08-26 · **Area:** notebooks · **Author:** owner-directed (Divy) · agent-drafted

## Objective

Explain why the `notebooks/` folder holds companion notebooks for only two of ten cells, and leave a detailed,
executable plan (plus the plan/discussion conventions the sibling `Hazard_modeling` repo uses) so the
remaining eight cells can be covered one at a time.

## Background

The owner remembered creating companion notebooks "for almost all hazards" and could not see them in the
remote repository. The 2026-08-18 architecture review had already recorded "Notebooks cover 2 of 10 cells"
and recommended notebooks for the eight uncovered cells, hurricane first; nothing followed it.

## What was found

1. On disk and across every git ref (`main`, `origin/main`, `divi/main`) there are exactly four notebooks:
   `notebooks/{hail,flood}/solar/{00_curve_curation,01_runtime_curve}_walkthrough.ipynb`, added once in
   `abd3f3e` (2026-06-25). No notebook was ever deleted, renamed, stashed, left on another branch or in an
   unreachable commit. Local `main` is one README-only commit behind `origin/main`; nothing local is unpushed.
   The remote (git and GitHub API) shows the same four. Other-hazard notebooks were **never created here**.
2. The per-hazard damage notebooks the owner remembered are in the consumer repo
   (`Hazard_modeling/Notebooks/<peril>/…/m3/`); they narrate how Hazard consumes each curve, not how Damage
   curated it.
3. Both existing pairs are **broken**: headless execution (`jupyter nbconvert --execute`) fails in cell 1 with
   `RuntimeError: Could not find damage_modeling repo root` because the loader requires the removed
   `docs/damage_curves/` tree and pins `docs_r5` / `docs_r3` artifacts that now exist only in the gitignored
   `docs/source_drops/extracted/` mirror. Current pins are `docs_r7` / `docs_r4`.
4. `notebooks/README.md` and both per-asset READMEs still cite the removed `docs/damage_curves/` path.
5. `docs/plans/` and `docs/extra/discussion/` exist but their indexes lacked the Hazard ledger columns
   (Date · Created by · Related to), the 5-field stamp, the closed status vocabulary and templates.

## What was created / changed

**Created**

- `docs/extra/discussion/cell_notebook_coverage/README.md` — reasoning node (question, verification, options,
  pressure tests, verdict, owner gates G1–G4).
- `docs/plans/cell_notebook_coverage/` — `README.md` (plan of record, `status: proposed`),
  `notebook_contract.md`, `cell_work_packages.md`, `decisions.md` (NB-D01…D10), `assumptions.md` (NB-A01…A12).
- `docs/plans/_templates/` — README + plan README / decisions / assumptions templates.
- `docs/extra/discussion/_templates/` — README + discussion node template.
- this task-history folder.

**Modified**

- `docs/plans/README.md` — stamp, ledger columns, new row, workflow + vocabulary + templates link.
- `docs/extra/discussion/README.md` — stamp, ledger columns, new row, templates link.
- `notebooks/README.md` — stale path fixed, 10-cell coverage matrix, loader rule, execution state, plan link.
- `notebooks/hail/solar/README.md`, `notebooks/flood/solar/README.md` — current artifact paths + broken-state
  notice pointing at Phase 0.
- `docs/README.md` — `extra/tasks_history/` row; templates named in the plans / discussion rows.
- `AGENTS.md` — repo-map rows for `docs/plans/`, `docs/extra/discussion/`, `docs/extra/tasks_history/`;
  `notebooks/` row corrected from "(TBD)" to the measured state.
- `docs/extra/tasks_history/README.md` — this session's row.

**Not changed:** any curve artifact, workbook, KAT, contract, schema, notebook `.ipynb` file, or anything in
`docs/cells/`. Nothing was committed or pushed.

## Current status

- [x] Root cause of "missing notebooks" established and written down (never created here; existing pairs broken).
- [x] Detailed plan + contract + per-cell packages + registers in place, `status: proposed`.
- [x] Hazard plan/discussion conventions applied (stamps, ledgers, closed vocabulary, templates).
- [x] Stale `docs/damage_curves/` references in the notebook READMEs corrected.
- [ ] Owner answers gates G1–G4 (plan README).
- [ ] Phase 0 repair executed (`hail_solar`, `flood_solar`).
- [ ] Phases 1–6.

## Next steps

See [`handoff.md`](handoff.md).
