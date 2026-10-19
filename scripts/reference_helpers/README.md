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
| `review_substation_flood_reuse.py` | Research-only exact-commit reproduction of the Flood/Wind assembly response and the standalone station value ledger. Writes review receipts, never a new cell or loss result. |
| `review_substation_flood_binding.py` | Executes a pinned, non-runtime station-binding candidate and complete value crosswalk; emits labeled audit arithmetic while reportable and annual losses remain null. |
| `validate_substation_flood_binding.py` | Sixteen test methods covering candidate value accounting, source parity, input/hash/domain failures, double counting and rejection of unadmitted metrics. |
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
| `flood_real_estate_curve_eval.py` | Fail-closed reference evaluator for the noncanonical flood × real estate model-v0.1 proposal: reference-building selector, water-type routing, depth-above-grade bridge, record ranges, NACCS bounds; damage emit v2. |
| `build_flood_real_estate_v0_1_package.py` | Deterministic builder for the flood × real estate model-v0.1 artifact, capability, known-answer tests and review workbook (needs openpyxl). |
| `validate_flood_real_estate_v0_1_package.py` | Schema/register/ordinate/reproducibility/KAT/non-promotion/workbook/link validator for the flood × real estate model-v0.1 proposal. |
| `build_flood_real_estate_v0_2_package.py` | Deterministic builder for the flood × real estate model-v0.2 proposal (current): one Hazus record per house, warehouse and office for all still water, retail unchanged; artifact, capability, known-answer tests and review workbook (needs openpyxl). |
| `validate_flood_real_estate_v0_2_package.py` | Validator for the flood × real estate model-v0.2 proposal: v0.1 checks plus the profile binding, its agreement with the artifact, and same-value-for-both-water-types for one-record buildings. |
| `flood_real_estate_form_comparison.py` | Curve-form comparison (linear, PCHIP, anchored logistic/Richards/Weibull; LOOCV and shape gates) for the noncanonical flood × real estate model-v0.1 scaffold. Needs numpy, scipy and matplotlib. |
| `flood_real_estate_nfip_claims_check.py` | NFIP claims check for the noncanonical flood × real estate model-v0.1 proposal: fetches OpenFEMA NfipClaims v3 into gitignored `build/nfip_claims`, compares band means with the proposed curves, writes the comparison, sensitivity, by-storeys and manifest files and the chart. Needs numpy and matplotlib. |
| `flood_real_estate_profile_binding.py` | Binds the flood × real estate model-v0.2 records to the Hazard reference profiles r1 (binding table with explicit gaps) and computes the profiles' floor-height sensitivity through the reference evaluator. Standard library only. |
| `extract_tropical_cyclone_wind_real_estate_hazus_ordinates.py` | Extracts the fifteen proposed tropical-cyclone wind × real estate records from the FEMA Hazus 6.1 wind extract and cross-checks them against SimCenter's Hazus 5.1 copy (source files outside the repo; SHA-256 pinned). Needs openpyxl. |
| `tropical_cyclone_wind_real_estate_curve_eval.py` | Fail-closed reference evaluator for the noncanonical tropical-cyclone wind × real estate model-v0.1 proposal: reference-building and terrain selectors, reference-only wind characteristics, 50–250 mph records; damage emit v2. |
| `build_tropical_cyclone_wind_real_estate_v0_1_package.py` | Deterministic builder for the tropical-cyclone wind × real estate model-v0.1 artifact, capability, known-answer tests and review workbook (needs openpyxl). |
| `validate_tropical_cyclone_wind_real_estate_v0_1_package.py` | Schema/register/ordinate/loader-routing/reproducibility/KAT/non-promotion/workbook/link validator for the tropical-cyclone wind × real estate model-v0.1 proposal. |
| `check_tropical_cyclone_wind_real_estate_hazard_loader.py` | Read-only consumer check (model v0.1 or v0.2 as a second argument): runs the proposal's known-answer requests through a copy of Hazard's generic v3 loader and lists the differences (validation report §4). |
| `extract_tropical_cyclone_wind_real_estate_v0_2_hazus_ordinates.py` | Extracts the model-v0.2 tropical-cyclone wind × real estate ordinates (house, retail, warehouse new-or-average deck, office SECBM; 20 records) and the variant sensitivity from the FEMA Hazus 6.1 wind extract, cross-checked against SimCenter's Hazus 5.1 copy (needs openpyxl; a few minutes). |
| `build_tropical_cyclone_wind_real_estate_v0_2_package.py` | Deterministic builder for the tropical-cyclone wind × real estate model-v0.2 proposal (current): artifact, capability, known-answer tests and review workbook (needs openpyxl). |
| `validate_tropical_cyclone_wind_real_estate_v0_2_package.py` | Validator for the tropical-cyclone wind × real estate model-v0.2 proposal: v0.1 checks plus the profile binding and its agreement with the artifact. |
| `tropical_cyclone_wind_real_estate_profile_binding.py` | Binds the tropical-cyclone wind × real estate model-v0.2 records to the Hazard reference profiles r1 (binding table with explicit gaps). Standard library only. |

These helpers are not a full production package. Their purpose is to make the intended implementation seam unambiguous.

`validate_flood_substation_v1.py` validates the standalone cell schema, inherited knots, value partition and evidence paths.

`validate_substation_wildfire_binding.py` checks the standalone Wildfire electrical binding,
unchanged canonical categorical response, 31-row value partition and installed Hazard pins.
