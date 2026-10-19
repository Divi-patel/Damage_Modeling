<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# convective_wind_real_estate

Current cell: **convective wind (straight-line wind and tornado) × real estate**, a new **scaffold** whose proposal is
semantic damage-model `model v0.1`, documentation revision `docs r1`. It publishes **no runtime curve yet**. It is not
in the artifact index, not in a package release, and does not change any Hazard pin.

## What this cell is for

Direct physical damage to the **structure** of the Hazard reference profiles r1 — a one-storey house, a one-storey
steel warehouse and a three-storey office, the same buildings as `flood_real_estate` and
`tropical_cyclone_wind_real_estate` — from thunderstorm straight-line wind and from a direct tornado hit. Damage is a
fraction of the structure's **replacement cost new**. The curves come from the EF (Enhanced Fujita) scale's degrees of
damage for each building type, priced through FEMA's Hazus damage states; straight-line wind starts at 96 mph.

## Start here

- [Scope, change classification and coverage check](proposed/README_convective_wind_real_estate__model_v0_1__docs_r1.md)
- [Decision log](proposed/DECISION_LOG_convective_wind_real_estate__model_v0_1__docs_r1.md)
- [Derivation dossier](proposed/convective_wind_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md) (includes the seven-step audit and the NRI check)
- [**Return package for Hazard**](proposed/RETURN_PACKAGE_convective_wind_real_estate__model_v0_1__docs_r1.md) (one card per profile)
- [Curves chart](previews/convective_wind_real_estate_v0_1_curves.png)

**Package — model v0.1:**
[curve artifact](proposed/convective_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json),
[capability](proposed/convective_wind_real_estate__model_v0_1__docs_r1__capability.json),
[EF degree-of-damage table](proposed/EF_DEGREE_OF_DAMAGE_TABLE_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[ordinates](proposed/CURVE_ORDINATES_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[sensitivity](proposed/SENSITIVITY_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[NRI check](proposed/NRI_CHECK_convective_wind_real_estate__model_v0_1__docs_r1.csv) (with its [receipt](proposed/NRI_CHECK_RECEIPT_convective_wind_real_estate__model_v0_1__docs_r1.json)),
[known-answer tests](proposed/known_answer_tests_convective_wind_real_estate__model_v0_1__docs_r1.json),
[workbook](proposed/damage_curve_records_convective_wind_real_estate__model_v0_1__docs_r1.xlsx),
[metadata spec](proposed/convective_wind_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md),
[profile binding](proposed/PROFILE_BINDING_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[validation report](proposed/VALIDATION_REPORT_convective_wind_real_estate__model_v0_1__docs_r1.md)

Registers: [sources](proposed/SOURCE_REGISTER_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[claims](proposed/CLAIM_PARAMETER_REGISTER_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[parameter tiers](proposed/PARAMETER_TIER_TABLE_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[value crosswalk](proposed/VALUE_CROSSWALK_convective_wind_real_estate__model_v0_1__docs_r1.csv).

## Rebuild

```bash
python scripts/reference_helpers/derive_convective_wind_real_estate_ef_curves.py --chart
python scripts/reference_helpers/build_convective_wind_real_estate_v0_1_package.py
python scripts/reference_helpers/convective_wind_real_estate_profile_binding.py
python scripts/reference_helpers/validate_convective_wind_real_estate_v0_1_package.py
```

The NRI check needs a Hazard_Modeling checkout and the NRI parquet:
`convective_wind_real_estate_nri_check.py --hazard-repo <path> --nri <parquet>`.
