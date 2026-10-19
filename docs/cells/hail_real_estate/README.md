<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# hail_real_estate

Current cell: **hail × real estate**, a new **scaffold** whose proposal is semantic damage-model `model v0.1`,
documentation revision `docs r1`. It is not in the artifact index or a package release, and it does not change any
Hazard pin.

## What this cell is for

Direct physical hail damage to the Hazard reference profiles r1: a one-storey house, a one-storey steel warehouse and
a three-storey office. These are the same buildings as the flood, hurricane and convective real-estate cells. Damage
is given per building part:

- **The roof cover:** the chance it must be replaced at a given hail size, from Haag's hail-damage thresholds for
  shingles, TPO membrane and steel panels.
- **The walls and windows:** a Tier-4 screening unit.

Each part carries its share of the structure's **replacement cost new**, from FEMA Hazus cost ratios (house, office)
or judgment (warehouse). Cosmetic denting is not counted.

## Start here

- [Scope, change classification and coverage check](proposed/README_hail_real_estate__model_v0_1__docs_r1.md)
- [Decision log](proposed/DECISION_LOG_hail_real_estate__model_v0_1__docs_r1.md)
- [Derivation dossier](proposed/hail_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md) (includes the seven-step audit and the NRI check)
- [**Return package for Hazard**](proposed/RETURN_PACKAGE_hail_real_estate__model_v0_1__docs_r1.md) (one card per profile)
- [Curves chart](previews/hail_real_estate_v0_1_curves.png)

**Package — model v0.1:**
[curve artifact](proposed/hail_real_estate__model_v0_1__docs_r1__curve_artifact.json),
[capability](proposed/hail_real_estate__model_v0_1__docs_r1__capability.json),
[component fragility table](proposed/COMPONENT_FRAGILITY_TABLE_hail_real_estate__model_v0_1__docs_r1.csv),
[ordinates](proposed/CURVE_ORDINATES_hail_real_estate__model_v0_1__docs_r1.csv),
[sensitivity](proposed/SENSITIVITY_hail_real_estate__model_v0_1__docs_r1.csv),
[NRI check](proposed/NRI_CHECK_hail_real_estate__model_v0_1__docs_r1.csv) (with its [receipt](proposed/NRI_CHECK_RECEIPT_hail_real_estate__model_v0_1__docs_r1.json)),
[known-answer tests](proposed/known_answer_tests_hail_real_estate__model_v0_1__docs_r1.json),
[workbook](proposed/damage_curve_records_hail_real_estate__model_v0_1__docs_r1.xlsx),
[metadata spec](proposed/hail_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md),
[profile binding](proposed/PROFILE_BINDING_hail_real_estate__model_v0_1__docs_r1.csv),
[validation report](proposed/VALIDATION_REPORT_hail_real_estate__model_v0_1__docs_r1.md)

Registers: [sources](proposed/SOURCE_REGISTER_hail_real_estate__model_v0_1__docs_r1.csv),
[claims](proposed/CLAIM_PARAMETER_REGISTER_hail_real_estate__model_v0_1__docs_r1.csv),
[parameter tiers](proposed/PARAMETER_TIER_TABLE_hail_real_estate__model_v0_1__docs_r1.csv),
[value crosswalk](proposed/VALUE_CROSSWALK_hail_real_estate__model_v0_1__docs_r1.csv).

## Rebuild

```bash
python scripts/reference_helpers/derive_hail_real_estate_curves.py --chart
python scripts/reference_helpers/hail_real_estate_nri_check.py --hazard-repo <Hazard_Modeling checkout> --nri <NRI parquet>
python scripts/reference_helpers/build_hail_real_estate_v0_1_package.py
python scripts/reference_helpers/hail_real_estate_profile_binding.py
python scripts/reference_helpers/validate_hail_real_estate_v0_1_package.py
```

The NRI check needs a Hazard_Modeling checkout holding the hail M0/M1 grid data and the NRI parquet. Both are on GCS;
the URIs are in the receipt. The loader probe needs a copy of Hazard's `damage_loader.py`:
`check_hail_real_estate_hazard_loader.py <folder>`.
