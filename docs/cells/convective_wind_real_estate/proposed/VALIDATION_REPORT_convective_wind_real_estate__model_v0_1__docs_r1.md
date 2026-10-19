<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# Validation report — convective_wind_real_estate model v0.1 / docs r1

What was checked on the proposal, how, and what was not. Run on 2026-10-18 from branch
`cell/convective-wind-real-estate` (base: `main` 81d5309).

## 1. Package files

| File | SHA-256 |
|---|---|
| `convective_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json` | `e676fb077ca3fb96a1d0efce7b1e408c2a82265ec97ea2eb4ebbef7e5aeeef3d` |
| `convective_wind_real_estate__model_v0_1__docs_r1__capability.json` | `37359c51f9580508739a73e0713766eb363cba3c160aab062691f1b9bbff6c56` |
| `known_answer_tests_convective_wind_real_estate__model_v0_1__docs_r1.json` | `ad02455a10093cec51de7fde11df3b06a07277559984329acebd271bfee672f3` |
| `CURVE_ORDINATES_convective_wind_real_estate__model_v0_1__docs_r1.csv` | `dcd9b07d2a36e7907726aa0b18c6ab9a8142d52ce388a2a88600a839915327ac` |
| `EF_DEGREE_OF_DAMAGE_TABLE_convective_wind_real_estate__model_v0_1__docs_r1.csv` | `05265c3ee885e041fa22180a4dab82074b60ca2e124a8eda6652a94368fef621` |

Six curve records (three buildings × two pathways), 256 knots each; 166 known-answer tests (141 formula, 12 withheld,
13 error).

## 2. Validator result

`python scripts/reference_helpers/validate_convective_wind_real_estate_v0_1_package.py` (Python 3.11, jsonschema 4.26,
openpyxl 3.1): **67/67 checks pass**. The checks cover:

- files, schemas (bundle v3, capability v3, every emit against damage emit v2), embedded = standalone capability;
- registers rectangular with LF endings, every source ID resolving;
- the EF table (LB < EXP < UB, costs on the Hazus ladder and non-decreasing, 10/8/7 degrees);
- the ordinates and sensitivity re-derived from the EF table and identical to the committed CSVs;
- records equal to the ordinates, 1-mph knots 0–255, values in [0, 1], non-decreasing, straight-line zero at and below
  96 mph, tornado ≥ straight-line at every knot, pathway flags present;
- loader compatibility per pathway (one required selector, unique routing, one range, distinct axis fields);
- builder reproducibility of the JSON outputs; all 166 known-answer tests through the reference evaluator;
- non-promotion (absent from the artifact index and version registry, no `current/`, gate blocked);
- the NRI receipt pinning the current ordinates; the profile binding (every profile × pathway, records and evidence
  resolve, one profile revision); workbook sheets; Markdown links.

Reproducibility: rerunning the derive, build and binding scripts reproduces every file byte for byte, including the
chart, except the Excel workbook (same sheets and values; zip timestamps differ).

## 3. Hand checks

Computed directly from the formula with the EF numbers typed in again (not through the scripts):

| Case | By hand | Package |
|---|---|---|
| House, tornado, 120 mph | 0.359375 | 0.359375 (knot) |
| Warehouse, straight-line, 120 mph (onset 96) | 0.307830 | 0.307830 (knot) |
| Office, tornado, 150.5 mph (EF3 midpoint) | 0.464431 | 0.464392 (between knots) |

Largest difference between the 1-mph table and the exact expression, over every record at 0.1-mph steps:
0.00017 (house straight-line near 113.5 mph). Lognormal spreads β range 0.087–0.131.

## 4. Consumer probe (Hazard common v3 loader, read-only)

`check_convective_wind_real_estate_hazard_loader.py` runs every known-answer request through a copy of Hazard's
`drivers/deep/src/deep/damage_loader.py` (main `f19c604830954a43e293749be390fd37b6eb6e11`, blob `4bdadaa1`):

**160 of 166 agree**, including every priced value (both pathways, all three buildings) and every withheld result
(above 255 mph; contents). The six differences are error-code names only:

| Cell code | Hazard loader code | Count |
|---|---|---|
| `PATHWAY_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `PATHWAY_ID_UNKNOWN` | `UNSUPPORTED_PATHWAY` | 1 |
| `REFERENCE_BUILDING_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `REFERENCE_BUILDING_ID_UNKNOWN` | `SELECTOR_MISMATCH` | 2 |
| `FAILURE_UNIT_ID_REQUIRED` | `FAILURE_UNIT_ID_UNKNOWN` | 1 |

Both fail closed in every case. The loader needs no change for this cell. The Hazard repository was not modified.

## 5. NRI check

Order-of-magnitude comparison with FEMA's National Risk Index on Hazard's grid (dossier §13; inputs pinned in the
[receipt](NRI_CHECK_RECEIPT_convective_wind_real_estate__model_v0_1__docs_r1.json)). It is a check, not a calibration.

## 6. Not validated here

- The EF expected and bound speeds are expert estimates; no field or claims data validate the curves.
- The cost assigned to each EF degree is judgment (D-CWRE-07); no repair-cost data by EF degree exist.
- The straight-line use of tornado evidence (D-CWRE-10) is untested against straight-line damage data.
- No Hazard M2–M4 run; the yearly figures in the NRI check reproduce Hazard's arithmetic outside Hazard.
- Owner and reviewer acceptance (promotion gate).
