<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# wildfire_real_estate

Current cell: **wildfire × real estate**, a new **scaffold** whose proposal is semantic damage-model `model v0.1`,
documentation revision `docs r1`. It publishes **no runtime curve yet**. It is not in the artifact index, not in a
package release, and does not change any Hazard pin.

## What this cell is for

Direct physical damage to the **structure** of the Hazard reference profiles r1 — a one-storey house, a one-storey
steel warehouse and a three-storey office, the same buildings as the flood, hurricane and convective real-estate
cells — when a wildfire burns at the building's location. Damage is a fraction of the structure's **replacement cost
new**, looked up at the exact FSim flame-length class Hazard delivers. The house uses the USFS Wildfire Risk to
Communities structure response (shrub: 20% for flames under 2 ft up to 95% for 12 ft and above); the warehouse and
office use 0.8 and 0.9 times the house, from CAL FIRE post-fire inspections that compare building types inside the
same fires.

## Start here

- [Scope, change classification and coverage check](proposed/README_wildfire_real_estate__model_v0_1__docs_r1.md)
- [Decision log](proposed/DECISION_LOG_wildfire_real_estate__model_v0_1__docs_r1.md)
- [Derivation dossier](proposed/wildfire_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md) (includes the seven-step audit and the NRI check)
- [**Return package for Hazard**](proposed/RETURN_PACKAGE_wildfire_real_estate__model_v0_1__docs_r1.md) (one card per profile)
- [Curves chart](previews/wildfire_real_estate_v0_1_curves.png)

**Package — model v0.1:**
[curve artifact](proposed/wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json),
[capability](proposed/wildfire_real_estate__model_v0_1__docs_r1__capability.json),
[USFS response table](proposed/WRC_RESPONSE_FUNCTION_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv),
[building factors](proposed/BUILDING_FACTOR_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv),
[CAL FIRE comparison](proposed/DINS_BUILDING_COMPARISON_wildfire_real_estate__model_v0_1__docs_r1.csv) (with its [receipt](proposed/DINS_CHECK_RECEIPT_wildfire_real_estate__model_v0_1__docs_r1.json)),
[ordinates](proposed/CURVE_ORDINATES_wildfire_real_estate__model_v0_1__docs_r1.csv),
[sensitivity](proposed/SENSITIVITY_wildfire_real_estate__model_v0_1__docs_r1.csv),
[NRI check](proposed/NRI_CHECK_wildfire_real_estate__model_v0_1__docs_r1.csv) (with its [receipt](proposed/NRI_CHECK_RECEIPT_wildfire_real_estate__model_v0_1__docs_r1.json)),
[known-answer tests](proposed/known_answer_tests_wildfire_real_estate__model_v0_1__docs_r1.json),
[workbook](proposed/damage_curve_records_wildfire_real_estate__model_v0_1__docs_r1.xlsx),
[metadata spec](proposed/wildfire_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md),
[profile binding](proposed/PROFILE_BINDING_wildfire_real_estate__model_v0_1__docs_r1.csv),
[validation report](proposed/VALIDATION_REPORT_wildfire_real_estate__model_v0_1__docs_r1.md)

Registers: [sources](proposed/SOURCE_REGISTER_wildfire_real_estate__model_v0_1__docs_r1.csv),
[claims](proposed/CLAIM_PARAMETER_REGISTER_wildfire_real_estate__model_v0_1__docs_r1.csv),
[parameter tiers](proposed/PARAMETER_TIER_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv),
[value crosswalk](proposed/VALUE_CROSSWALK_wildfire_real_estate__model_v0_1__docs_r1.csv).

## Rebuild

```bash
python scripts/reference_helpers/wildfire_real_estate_dins_check.py --dins <dins_master.csv>
python scripts/reference_helpers/derive_wildfire_real_estate_curves.py --chart
python scripts/reference_helpers/wildfire_real_estate_nri_check.py --m1 <wildfire M1 parquet> --nri <NRI parquet>
python scripts/reference_helpers/build_wildfire_real_estate_v0_1_package.py
python scripts/reference_helpers/wildfire_real_estate_profile_binding.py
python scripts/reference_helpers/validate_wildfire_real_estate_v0_1_package.py
```

The CAL FIRE CSV, the Hazard wildfire M1 parquet and the NRI parquet are not committed; their sources and SHA-256
are in the receipts.
