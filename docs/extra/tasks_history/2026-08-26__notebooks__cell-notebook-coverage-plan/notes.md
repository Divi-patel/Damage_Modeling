# Notes — cell notebook coverage plan session (2026-08-26)

## Investigation commands (all read-only)

```bash
# what exists
find notebooks -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*'
git status --short --ignored | grep -i ipynb

# every notebook ever added / deleted on any ref
git log --all --diff-filter=A  --name-only  --format='@@ %h %ad %s' --date=short -- '*.ipynb'
git log --all --diff-filter=DR --name-status --format='@@ %h %ad %s' --date=short -- '*.ipynb'

# branches, remotes, stash, worktrees, unreachable commits
git fetch --all --prune && git branch -a -vv && git stash list && git worktree list
git ls-remote --heads origin; git ls-remote --heads divi
for c in $(git fsck --unreachable --no-reflogs | awk '/commit/{print $3}'); do git ls-tree -r --name-only $c | grep -c ipynb; done

# remote view
git ls-tree -r --name-only origin/main notebooks/
gh api repos/aamani-ai/Damage_Modeling/contents/notebooks --jq '.[] | "\(.type)  \(.path)"'

# headless execution (outputs to a scratch dir, nothing written into the repo)
.venv/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=180 \
  notebooks/hail/solar/01_runtime_curve_walkthrough.ipynb --output-dir /tmp/nbexec --output hail_01_exec.ipynb
```

## Measured facts used in the plan

| Fact | Value |
|---|---|
| Notebooks in repo | 4 (`hail/solar` 00+01, `flood/solar` 00+01), commit `abd3f3e` 2026-06-25 |
| Remote `origin/main` tip | `ce79b96` 2026-08-19 "Clarify Damage and Resiliency flows" (README only); local `main` `b1523f4`, 1 behind, 0 ahead |
| Fork `divi/main` | `f8b5ec3` 2026-07-12, 20 commits behind `origin/main`; same 4 notebooks |
| Execution result | both tested notebooks fail in cell 1 (`RuntimeError`, root finder requires `docs/damage_curves`) |
| Notebook-pinned artifacts | `hail_solar__model_v1_0__docs_r5`, `flood_solar__model_v1_0__docs_r3` — present only under gitignored `docs/source_drops/extracted/v2_5_implementation_hardened/…/01_cells/` |
| Current pins (artifact index) | hail r7 · flood r4 · wind_tornado r4 · strong_wind_solar r3 · wildfire_solar r3 · flood_wind r1 · wildfire_wind r1 · tc_wind_wind v1.2 r2 |
| Bundle shapes | v2: hail_solar, flood_solar, wind_tornado_wind, strong_wind_solar, wildfire_solar · v3 (1 pathway): flood_wind, wildfire_wind, tropical_cyclone_wind_wind, tropical_cyclone_wind_solar (v2.1 proposal) · v1: hail_wind v0.1 |
| KAT files in `current/` | hail_solar, wildfire_solar, flood_wind, wildfire_wind, tropical_cyclone_wind_wind — none for flood_solar, wind_tornado_wind, strong_wind_solar |
| Evaluator (`scripts/reference_helpers/damage_curve_eval.py`) | `evaluate_curve_record` dispatches `logistic`, `piecewise_linear`, `wind_tornado_logistic_ratio`, `thresholded_logistic_demand`; `strong_wind_solar_r_eff` derives the demand ratio; no exact categorical-state lookup (wildfire_solar needs `validate_runtime_contracts.exact_state_value`) |
| Environment | `.venv` python 3.12.12, nbconvert 7.17.1, matplotlib 3.11.1, pandas 3.0.5 |
| Link-check baseline (docs/, notebooks/, AGENTS.md, README.md) | 1,411 links, 90 broken (pre-existing) |
| CI | `.github/` does not exist |

## Verification performed after writing

- Hazard link check re-run over the same scope: broken count must not rise above the 90 baseline.
- Closed-vocabulary check over every stamped file touched or created (`status:` ∈ draft · proposed · active ·
  settled · superseded · done).
- `git status --short` reviewed so only the intended files are modified/added; no `.ipynb`, no `docs/cells/`,
  no commit, no push.

## Key insights

- "I can't see the notebooks on the remote" had two different true answers: the Damage repo never had them;
  the Hazard repo has them but its GitHub default branch `main` is ~280 commits behind `deploy/hazard-grid-qc`.
  Only the Damage side is this task's scope; the Hazard side is recorded in the conversation.
- A loader that resolves a governed object by *folder path* is a claim that outlives its evidence the moment
  the folder moves; resolving by *index + SHA* is the repository's own statement of the pin.
- Three current cells have no published KAT file; the notebooks must say so rather than invent expected values.
