<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# Validation report — wildfire_real_estate model v0.1 / docs r1

What was checked on the proposal, how, and what was not. Run on 2026-10-18 from branch
`cell/wildfire-real-estate` (base: `main` 81d5309).

## 1. Package files

| File | SHA-256 |
|---|---|
| `wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json` | `6b7c771d88b46d60e2c0b1339009ab06753f93f6376e8c8f30e40c91f31474ee` |
| `wildfire_real_estate__model_v0_1__docs_r1__capability.json` | `88154281f57cea2d450aff454409040f17b43f4653fed04519a1c3c003b3dee9` |
| `known_answer_tests_wildfire_real_estate__model_v0_1__docs_r1.json` | `c1e19fdd8ac61c0a5374a23530c05c8389863ad4075f1e67d604a4681b4e5ff6` |
| `CURVE_ORDINATES_wildfire_real_estate__model_v0_1__docs_r1.csv` | `d6d6895bc47ad31666f96682d9987109eb14d4c6757b15b540ddf7115af37951` |
| `WRC_RESPONSE_FUNCTION_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv` | `b4550c3a64d9b0a29f4189e5764ca99baf5ae7f01d605a4bdc9fa28e2ca9670f` |
| `BUILDING_FACTOR_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv` | `086a9234f1911432bb8f3b90c75870d3b81bcb4ff21c2e15a8b289297a4bc423` |
| `DINS_BUILDING_COMPARISON_wildfire_real_estate__model_v0_1__docs_r1.csv` | `4186716873dada6d072068b67ea949cb0d8535d5a1dd921b2cb2970ccc50e640` |

Three curve records (one per building), seven exact states each; 44 known-answer tests (24 formula, 3 withheld,
17 error).

## 2. Validator result

`python scripts/reference_helpers/validate_wildfire_real_estate_v0_1_package.py` (Python 3.11, jsonschema,
openpyxl): **75/75 checks pass**. The checks cover:

- files, schemas (bundle v3, capability v3, every emit against damage emit v2), embedded = standalone capability;
- registers rectangular with LF endings, every source ID resolving;
- the USFS response table (3 lifeforms × 6 classes, shrub = the published 20/35/50/65/80/95, increasing with class,
  tree ≥ shrub ≥ grass, class IDs = the artifact's class map, only shrub adopted);
- the building factors (house 1.0, warehouse 0.8, office 0.9; each adopted factor equals the CAL FIRE same-fire ratio
  rounded to one decimal; the CAL FIRE receipt pins the analysed download);
- the ordinates and sensitivity re-derived from the tables and identical to the committed CSVs;
- records equal to the ordinates, exactly states 0–6, state 0 = 0, values in [0, 1], non-decreasing,
  warehouse ≤ office ≤ house at every state, building flags present;
- loader compatibility (routing fields = the two required selectors, unique routing per building, one range,
  exact-integer axis);
- builder reproducibility of the JSON outputs; all 44 known-answer tests through the reference evaluator;
- non-promotion (absent from the artifact index and version registry, no `current/`, gate blocked);
- the NRI receipt pinning the current ordinates and Hazard's M1 table; the profile binding (every profile, records,
  factors and evidence resolve, one profile revision); workbook sheets; Markdown links.

Reproducibility: rerunning the CAL FIRE check, derive, NRI check, build and binding scripts reproduces every file
byte for byte, including the chart, except the Excel workbook (same sheets and values; zip timestamps differ).

## 3. Hand checks

| Case | By hand | Package |
|---|---|---|
| Warehouse, state 2 (2–4 ft) | 0.8 × 35 / 100 = 0.28 | 0.28 |
| Office, state 4 (6–8 ft) | 0.9 × 65 / 100 = 0.585 | 0.585 |
| Office, state 6 (12+ ft) | 0.9 × 95 / 100 = 0.855 | 0.855 |
| Warehouse, state 6 | 0.8 × 95 / 100 = 0.76 | 0.76 |
| CAL FIRE same-fire ratio with Destroyed read as 75% | — | 0.80 (warehouse), 0.94 (office) |

The USFS values in the response table were checked against the downloaded metadata text (WFRE-S001,
Process_Step 5); the FSim class boundaries against the FSim metadata (WFRE-S003).

## 4. Consumer probe (Hazard common v3 loader, read-only)

`check_wildfire_real_estate_hazard_loader.py` runs every known-answer request through a copy of Hazard's
`drivers/deep/src/deep/damage_loader.py` (main `08748ae5217e18e2f6c3aec482ee579e32d9f7b6`, blob `4bdadaa1`):

**30 of 44 agree**, including every priced value (21 states plus three states sent as whole floats) and every
withheld result (contents). Of the 14 differences, 12 are error-code names or fail closed either way:

| Cell code | Hazard loader result | Count |
|---|---|---|
| `PATHWAY_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `PATHWAY_ID_UNKNOWN` | `UNSUPPORTED_PATHWAY` | 1 |
| `REFERENCE_BUILDING_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `REFERENCE_BUILDING_ID_UNKNOWN` | `SELECTOR_MISMATCH` | 2 |
| `SOURCE_WILDFIRE_PRODUCT_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `SOURCE_WILDFIRE_PRODUCT_ID_UNSUPPORTED` | `SELECTOR_MISMATCH` | 1 |
| `INVALID_CLASS_STATE` (class label; boolean) | `AXIS_VALUE_INVALID` | 2 |
| `INVALID_CLASS_STATE` (state −1) | `AXIS_OUTSIDE_VALID_RANGE` | 1 |
| `INVALID_CLASS_STATE` (state 7) | withheld `ABOVE_SOURCE_VALID_RANGE` | 1 |
| `FAILURE_UNIT_ID_REQUIRED` | `FAILURE_UNIT_ID_UNKNOWN` | 1 |

Two are real behaviour differences (Hazard-side items, return package §6):

| Request | Cell | Hazard loader |
|---|---|---|
| State 2.5 | error `INVALID_CLASS_STATE` | interpolates: 0.425 for the house. Its exact-integer rule is keyed to `cell_id == "wildfire_wind"` only |
| State 4 with `burn_probability` in the call | error `FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL` | ignores the field and returns 0.65 |

Hazard's own wildfire Damage consumer (`perils/wildfire/src/wildfire/damage.py`) enforces both rules; the generic
loader does not for this cell. The Hazard repository was not modified.

## 5. NRI check

Order-of-magnitude comparison with FEMA's National Risk Index on Hazard's grid (dossier §13; inputs pinned in the
[receipt](NRI_CHECK_RECEIPT_wildfire_real_estate__model_v0_1__docs_r1.json)): 2.0× (house), 1.6× (warehouse) and
1.8× (office) nationally, rank correlation 0.88. It is a check, not a calibration.

## 6. Not validated here

- The USFS response values are agency judgment; no field or claims data validate them by flame-length class.
- The building factors come from California commercial buildings of mixed size and use, not the reference
  warehouse and office.
- The shrub default is not tested against a lifeform-resolved result.
- No Hazard M2–M4 run; the yearly figures in the NRI check reproduce Hazard's arithmetic outside Hazard.
- Owner and reviewer acceptance (promotion gate).
