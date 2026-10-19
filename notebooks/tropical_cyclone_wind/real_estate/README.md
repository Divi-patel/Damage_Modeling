<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-19
updated: 2026-10-19
status: draft
-->

# hurricane wind × real estate notebooks

Runnable companions for the noncanonical `tropical_cyclone_wind_real_estate` damage-curve cell (model v0.2 proposal): FEMA Hazus hurricane building-loss tables by building type and terrain class, variant sensitivity.

## Notebook order

| Notebook | Purpose |
|---|---|
| [`00_curve_curation_walkthrough.ipynb`](00_curve_curation_walkthrough.ipynb) | Start here. How the curves are built: evidence register, source tables, the derivation (recomputed and compared with the artifact), sensitivity, decisions, parameter tiers and open items. |
| [`01_runtime_curve_walkthrough.ipynb`](01_runtime_curve_walkthrough.ipynb) | Reads the proposed artifact and calls the curves through the cell's reference evaluator: request contract, value grids, fail-closed cases and an illustrative dollar example. |

## Source artifacts

```text
../../../docs/cells/tropical_cyclone_wind_real_estate/proposed/tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json
../../../docs/cells/tropical_cyclone_wind_real_estate/README.md
```

The cell documents are the source of truth; the notebooks only read them. Both notebooks are executed with their
outputs saved; figures are also written to [`outputs/`](outputs/). Run them from inside the repository (the first
cell finds the repository root).

## Boundary

Damage only: hazard intensity to damage ratio for the three Hazard reference buildings. Frequency, yearly loss and
tail metrics belong to Hazard. Dollar figures use the Hazard profile budgets as an illustration only; the artifact
withholds scenario dollars until Hazard qualifies each building value.
