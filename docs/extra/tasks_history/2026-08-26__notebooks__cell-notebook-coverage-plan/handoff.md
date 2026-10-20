# Handoff — cell notebook coverage plan (2026-08-26)

## 10-bullet summary

1. The other-hazard companion notebooks the owner remembered were **never created in this repo**: every ref,
   stash, worktree and unreachable commit holds only `hail/solar` and `flood/solar` (added 2026-06-25); the
   remote shows the same. Nothing is unpushed.
2. Both existing pairs are **broken** — cell 1 raises `RuntimeError` because the loader requires the removed
   `docs/damage_curves/` tree and pins `docs_r5` / `docs_r3` files that survive only in the gitignored
   `docs/source_drops/extracted/` mirror. Current pins are `docs_r7` / `docs_r4`.
3. A reasoning node now records the verification, options and verdict:
   `docs/extra/discussion/cell_notebook_coverage/README.md` (`status: active`, gates G1–G4 open).
4. The plan of record is `docs/plans/cell_notebook_coverage/README.md` (`status: proposed`): repair first,
   then one cell at a time, hurricane pair first, to 10/10 executing pairs; with `notebook_contract.md`,
   `cell_work_packages.md`, `decisions.md` (NB-D01…D10) and `assumptions.md` (NB-A01…A12).
5. Hazard's plan/discussion conventions are applied here: 5-field stamps, ledger columns (Date · Created by ·
   Related to · Status), the closed status vocabulary, and templates under `docs/plans/_templates/` and
   `docs/extra/discussion/_templates/`.
6. `notebooks/README.md` now carries the 10-cell coverage matrix, the loader rule and the execution state; the
   stale `docs/damage_curves/` path is gone from it and from both per-asset READMEs (which now point at the
   r7/r4 artifacts and say the notebooks are broken until Phase 0).
7. `AGENTS.md` repo map gained rows for `docs/plans/`, `docs/extra/discussion/`, `docs/extra/tasks_history/`
   and a corrected `notebooks/` row; `docs/README.md` gained the `extra/tasks_history/` row.
8. Nothing in `docs/cells/`, `docs/contracts/`, any workbook, KAT or `.ipynb` was changed. **Nothing was
   committed or pushed** — the working tree holds the changes for the owner's review.
9. Known stale claim left in place on purpose: `AGENTS.md` lists `.github/workflows/` as "CI (starter)"; the
   folder does not exist (already flagged by the 2026-08-18 review).
10. Local `main` is one README-only commit behind `origin/main` (`ce79b96`); a plain fast-forward pull is safe
    and does not touch any file changed here.

## Files touched

Created: `docs/extra/discussion/cell_notebook_coverage/README.md` · `docs/plans/cell_notebook_coverage/{README,notebook_contract,cell_work_packages,decisions,assumptions}.md` ·
`docs/plans/_templates/{README,TEMPLATE_plan_README,TEMPLATE_plan_decisions,TEMPLATE_plan_assumptions}.md` ·
`docs/extra/discussion/_templates/{README,TEMPLATE_discussion_node}.md` · this folder.
Modified: `docs/plans/README.md` · `docs/extra/discussion/README.md` · `notebooks/README.md` ·
`notebooks/hail/solar/README.md` · `notebooks/flood/solar/README.md` · `docs/README.md` · `AGENTS.md` ·
`docs/extra/tasks_history/README.md`.

## Repro / verify current state

```bash
git status --short                                   # expect only the files listed above
git rev-list --left-right --count main...origin/main # expect 0	1 (behind by the README commit)
find notebooks -name '*.ipynb' | wc -l               # 4
.venv/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=180 \
  notebooks/hail/solar/01_runtime_curve_walkthrough.ipynb --output-dir /tmp/nbexec   # fails in cell 1 until Phase 0
```

## Next action

### Phase A — owner review (blocking)

Read, in order: [`docs/plans/cell_notebook_coverage/README.md`](../../../plans/cell_notebook_coverage/README.md) →
[`notebook_contract.md`](../../../plans/cell_notebook_coverage/notebook_contract.md) →
[`cell_work_packages.md`](../../../plans/cell_notebook_coverage/cell_work_packages.md) →
[`decisions.md`](../../../plans/cell_notebook_coverage/decisions.md). Answer G1–G4 in the plan README and record
each answer as the corresponding NB-D row (`recommended · gate` → decision). Flip the plan to `active` and the
discussion node to `settled`. Then `git pull --ff-only` and commit the documentation set.

### Phase B — Phase 0 repair (first execution step)

1. Re-point the loader cell in all four notebooks to the index pins (`hail_solar@model_v1_0__docs_r7`,
   `flood_solar@model_v1_0__docs_r4`) via the shared helper (or the per-notebook cell if G2 says so).
2. Re-execute headlessly; diff printed identities and parameters against the r7/r4 artifacts; rewrite prose
   that still describes r5/r3 fields; regenerate `outputs/`.
3. Update the per-asset READMEs' execution-state line to `executing 2026-MM-DD`; update the matrix row.
4. Gate: both pairs execute from a fresh clone.

### Phase C — scaffolding, then the hurricane pair

Follow WP-1, WP-2, WP-3 in [`cell_work_packages.md`](../../../plans/cell_notebook_coverage/cell_work_packages.md).
Do not open WP-3 before WP-2's gate passes.

### Gotchas

- Use the repo `.venv` (`python3.12`); a bare `python3` may lack `expat` and cannot read the workbooks.
- macOS has no `timeout`; use nbconvert's `--ExecutePreprocessor.timeout`.
- `notebooks/**/outputs/` is tracked; the root `/outputs/` ignore does not cover it.
- The Hazard repo is a gitignored symlink — reference its consumer code by path in prose, never import it.
- Bundle v3 keeps `hazard_axis`, `curve_records`, `failure_unit_coverage`, `selector_logic`,
  `exposure_contract` under `pathways[0]`; v2 keeps them at the top level.
