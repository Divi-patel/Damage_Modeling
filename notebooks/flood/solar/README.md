# flood × solar notebooks

This folder contains runnable companions for the `flood_solar` damage-curve cell.

## Notebook order

| Notebook | Purpose |
|---|---|
| [`00_curve_curation_walkthrough.ipynb`](00_curve_curation_walkthrough.ipynb) | Start here. Explains the curation process: evidence classes, failure-unit coverage, local-depth axis choice, piecewise/state curve form, selectors/conditioners/exposure, value linkage, and open seams. |
| [`01_runtime_curve_walkthrough.ipynb`](01_runtime_curve_walkthrough.ipynb) | Read the canonical runtime artifact, evaluate the multi-failure-unit piecewise curves, demonstrate local-depth transforms, and assemble conditional loss from explicit value/exposure inputs. |

## Execution state

> **Broken as of 2026-08-26 — repair is Phase 0 (WP-0b) of the
> [cell notebook coverage plan](../../../docs/plans/cell_notebook_coverage/README.md).** Both notebooks stop
> in their first code cell: the loader looks for the removed `docs/damage_curves/…` tree and pins
> `flood_solar__model_v1_0__docs_r3`, which now exists only in the gitignored `docs/source_drops/extracted/`
> mirror. The repository-current pin is `flood_solar@model_v1_0__docs_r4` (below). Do not re-point the path by
> hand without re-executing and reconciling the prose and figures to r4.

## Source artifacts

Canonical runtime artifact (repository-current pin `flood_solar@model_v1_0__docs_r4`, resolved through
[`docs/contracts/MACHINE_READABLE_ARTIFACTS.md`](../../../docs/contracts/MACHINE_READABLE_ARTIFACTS.md)):

- [`flood_solar__model_v1_0__docs_r4__curve_artifact.json`](../../../docs/cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json)
- known-answer tests: none is published in `current/` as of 2026-08-26 (plan gate G4); the runtime notebook
  must say so rather than invent expected values.

Process / evidence narrative:

- [`flood_solar_curve_derivation_dossier_v1_0.md`](../../../docs/cells/flood_solar/current/flood_solar_curve_derivation_dossier_v1_0.md)
- [`flood_solar_damage_code_metadata_spec_v1_0.md`](../../../docs/cells/flood_solar/current/flood_solar_damage_code_metadata_spec_v1_0.md)
- cell entry point: [`docs/cells/flood_solar/README.md`](../../../docs/cells/flood_solar/README.md)

## What the notebooks cover

`00_curve_curation_walkthrough.ipynb` covers:

- Why flood × solar cannot be a whole-plant flood curve.
- How each evidence source is assigned a role and limitation.
- Why the accepted x-axis is local depth above component datum.
- Why flood uses piecewise/state curves rather than logistics.
- Which curve ordinates are source-anchored versus engineering parameterization.
- How selectors, conditioners, exposure variables, and value linkage differ.
- Where future curation/code work should replace placeholders.

`01_runtime_curve_walkthrough.ipynb` covers:

- Canonical JSON identity and capability declaration.
- Failure-unit coverage across electrical, cable, module, and foundation pathways.
- Local-depth axis: `h_i = max(0, WSE - z_i_crit)`.
- Piecewise-linear depth-damage/state curves.
- Foundation velocity/scour proxy as a conditional placeholder.
- Selector / conditioner / exposure fields carried by the artifact.
- Example conditional loss assembly:

```text
loss_i = DR_i × value_i × fraction_value_exposed_i
```

## What it does not cover

- Annual flood frequency, site inundation probability, or portfolio risk metrics.
- A full curation proof trail; that belongs in the planned `00` notebook.
- Claims-calibrated uncertainty or tail distributions; the current artifact emits scalar mean / deterministic state-table curves only.
