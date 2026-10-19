# notebooks/ — damage-curve walkthroughs and derivation companions

Runnable notebooks live here as companions to the formal cell packages under `docs/damage_curves/`.
The docs remain the source of truth for the shipped curve artifact; notebooks are for inspection, fitting
checks, evidence walkthroughs, and consumer-facing examples.

## Organization

Use the same shape as the Hazard notebooks:

```text
notebooks/
  <hazard>/
    README.md
    <asset>/
      README.md
      00_curve_curation_walkthrough.ipynb
      01_runtime_curve_walkthrough.ipynb
      02_derivation_or_fit_check.ipynb
      outputs/
```

Name folders by the cell id parts where possible (`hail/solar/` for `hail_solar`). This keeps the path stable
when a cell later grows from one failure-unit curve to multiple failure-unit records.

## Notebook roles

| Prefix | Role | Boundary |
|---|---|---|
| `00_curve_curation_walkthrough` | Explain how evidence is curated into anchors, fitted parameters, selectors, conditioners, exposure/value logic, and capability gates. | Teaching/QA view of the cell dossier; source of truth remains the docs package. |
| `01_runtime_curve_walkthrough` | Read the canonical JSON artifact, evaluate the curve, and show selector / conditioner / exposure logic. | M3 severity only; no hazard frequency or EAL/PML. |
| `02_derivation_or_fit_check` | Reproduce or audit fitted parameters from source anchors/workbooks. | Evidence and fit QA; not the runtime contract. |
| `03_consumer_integration_example` | Show how a Hazard M3 consumer should call the artifact for a concrete asset/value basis. | Conditional loss assembly only unless explicitly paired with Hazard outputs. |

## Current notebooks

| Cell | Notebook | Purpose |
|---|---|---|
| `hail_solar` | [`hail/solar/00_curve_curation_walkthrough.ipynb`](hail/solar/00_curve_curation_walkthrough.ipynb) | Step-by-step curation walkthrough: evidence classes, interpreted anchors, logistic fits, selectors, conditioners, exposure/value logic, and open seams. |
| `hail_solar` | [`hail/solar/01_runtime_curve_walkthrough.ipynb`](hail/solar/01_runtime_curve_walkthrough.ipynb) | Canonical artifact walkthrough, plots, evidence/provenance fields, and M3 conditional-loss example. |
| `flood_solar` | [`flood/solar/00_curve_curation_walkthrough.ipynb`](flood/solar/00_curve_curation_walkthrough.ipynb) | Step-by-step curation walkthrough for multi-failure-unit flood modeling, evidence roles, local-depth axis, piecewise/state curves, value linkage, and open seams. |
| `flood_solar` | [`flood/solar/01_runtime_curve_walkthrough.ipynb`](flood/solar/01_runtime_curve_walkthrough.ipynb) | Canonical artifact walkthrough for multi-failure-unit flood curves, local-depth transforms, exposure/value scaling, and conditional loss assembly. |
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

- Runtime notebooks read the canonical `*__curve_artifact.json`; they do not copy curve parameters by hand.
- Mark assumptions explicitly, especially example value bases, exposure fractions, and placeholder adjustments.
- Do not compute EAL/PML/VaR in this repo unless the notebook is explicitly demonstrating a downstream Hazard
  integration. The damage layer owns `intensity → damage ratio`, not hazard frequency or financial metrics.
- Export important figures to the local `outputs/` folder so they can be reviewed outside Jupyter.
