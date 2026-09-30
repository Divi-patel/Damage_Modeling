# Runtime helper snippets

These files are reference implementations for downstream notebooks/services. They are intentionally dependency-light and use only Python's standard library.

| File | Purpose |
|---|---|
| `damage_curve_eval.py` | Evaluate the current JSON artifact curve forms: logistic, piecewise-linear, wind/tornado logistic ratio, and strong-wind solar thresholded demand logistic. |
| `height_bridge.py` | Convert source-native wind speeds, especially 10m gusts, to hub-height gusts before wind-turbine M3 damage evaluation. |
| `cap_binding_preflight.py` | Known-answer check for whether scalar EAL may pass a cap-binding gate or must emit spread/state samples. |
| `pathway_damage_curve_eval.py` | Reference evaluator for the noncanonical pathway-aware wind-turbine v2 proposal. |
| `validate_wind_tornado_v2_proposal.py` | Full research-package validator for the wind-turbine v2 proposal. |
| `convective_solar_damage_curve_eval.py` | Reference evaluator and bounded cascade/salvage loss assembler for the noncanonical convective solar v2 proposal. |
| `validate_strong_wind_solar_v2_proposal.py` | Schema/KAT/register/value/workbook/current-pin validator for the convective solar v2 proposal. |
| `validate_runtime_contracts.py` | Validate the five repository-current canonical artifact/capability/KAT contracts. |
| `validate_tropical_cyclone_wind_wind_v0_1_scaffold.py` | Fail-closed package validator for the noncanonical TC-wind × wind model-v0.1 scaffold. |
| `tropical_cyclone_wind_wind_curve_eval.py` | Exact selector/range/value fail-closed evaluator for the noncanonical TC-wind × wind model-v1.0 Jaimes source-family proposal. |
| `validate_tropical_cyclone_wind_wind_v1_proposal.py` | Bundle/schema/KAT/register/value/workbook/QA/link/index validator for the TC-wind × wind model-v1.0 proposal. |
| `validate_flood_wind_v0_1_scaffold.py` | Fail-closed package plus shared flood-electrical substrate validator for flood × wind model v0.1. |
| `flood_wind_curve_eval.py` | Exact source-knot, axis-bridge, selector/conditioner, range, unit, and artifact-pin evaluator for the noncanonical flood × wind whole-substation model-v1 proposal. |
| `validate_flood_wind_v1_proposal.py` | Schema/semantic-curve/KAT/register/value/shared-substrate/workbook/link/index validator for the flood × wind model-v1 proposal. |
| `build_flood_wind_v1_workbook.mjs` | `@oai/artifact-tool` builder, renderer, and QA inspector for the governed model-v1 review workbook. |
| `validate_tropical_cyclone_wind_solar_v0_1_scaffold.py` | Fail-closed architecture/value/GSU package validator for TC-wind × solar model v0.1. |
| `derive_tropical_cyclone_wind_solar_v1_fit.py` | Exact Perry source-cohort filter, percent conversion, PAVA fit, sparse-tail quarantine, and event-sensitivity derivation for the noncanonical model-v1 proposal. |
| `tropical_cyclone_wind_solar_curve_eval.py` | Exact axis/selector/range/value fail-closed evaluator for the source-specific Perry visible-module screening atom. |
| `validate_tropical_cyclone_wind_solar_v1_proposal.py` | Schema/source-reproduction/KAT/register/value/workbook/link/index validator for the noncanonical TC-wind × solar model-v1 screening exception. |
| `build_tropical_cyclone_wind_solar_v1_workbook.mjs` | `@oai/artifact-tool` builder, renderer, and QA inspector for the TC-wind × solar model-v1 audit workbook. |
| `tropical_cyclone_wind_solar_v2_curve_eval.py` | Fail-closed reference evaluator for the noncanonical model-v2 Perry compatibility, fixed-tilt synthetic Tier-4, qualified-tracker synthetic Tier-4, and directly queried withheld-unit routes. |
| `build_tropical_cyclone_wind_solar_v2_package.py` | Deterministic builder for the noncanonical model-v2 artifact, capability, KAT, registers, audit comparison profile, and governed workbook. |
| `validate_tropical_cyclone_wind_solar_v2_proposal.py` | Schema/semantic/KAT/register/workbook/pin/link/non-promotion validator for the five-record model-v2 proposal. |
| `tropical_cyclone_wind_solar_v2_1_curve_eval.py` | Exact-identity evaluator for the proposed and canonical coverage-complete component DR and named-value full-plant physical-damage assembly. |
| `build_tropical_cyclone_wind_solar_v2_1_package.py` | Deterministic builder for the ten-record model-v2.1 artifact, capability, KATs, registers, old/new table, and workbook. |
| `validate_tropical_cyclone_wind_solar_v2_1_proposal.py` | Preservation, schema, numeric coverage, plant assembly, value reconciliation, KAT, workbook and exact-pin validator for the immutable model-v2.1 proposal. |
| `validate_tropical_cyclone_wind_solar_v2_1_release.py` | Canonical identity, schema, exact promotion-diff, supporting-byte, proposal/current dual-read, KAT and artifact-index validator for the model-v2.1 release. |
| `validate_hail_wind_v0_1_scaffold.py` | Fail-closed source/contact/value/workbook/link validator for hail × wind model v0.1. |
| `validate_wildfire_wind_v0_1_scaffold.py` | Fail-closed JSON/register/value/workbook/link validator for the noncanonical wildfire x wind model-v0.1 scaffold. |

These helpers are not a full production package. Their purpose is to make the intended implementation seam unambiguous.
