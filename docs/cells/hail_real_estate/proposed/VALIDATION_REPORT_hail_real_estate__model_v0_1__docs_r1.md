<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# Validation report — hail_real_estate model v0.1 / docs r1

This records what was checked on the proposal, how, and what was not. Run on 2026-10-18 from branch
`cell/hail-real-estate` (base: `main` 81d5309).

## 1. Package files

| File | SHA-256 |
|---|---|
| `hail_real_estate__model_v0_1__docs_r1__curve_artifact.json` | `52cf865d4dfb8b4c593736fb05b5d3e7c341bad2a2441b89499d7e88605fef20` |
| `hail_real_estate__model_v0_1__docs_r1__capability.json` | `5c4f9dd750a0a5fc943c86d135799414fc92b114d0f6a5d189e57b8eed941eb4` |
| `known_answer_tests_hail_real_estate__model_v0_1__docs_r1.json` | `668a0c25eacf57a74f8dc2e8a8e936a4b6f24b17ae7c9b5f06a438fb4f2ab9ef` |
| `CURVE_ORDINATES_hail_real_estate__model_v0_1__docs_r1.csv` | `270fedc842e4c20338a15819203a62790777b2ffcd3111b2b5e56bd475a6d74d` |
| `COMPONENT_FRAGILITY_TABLE_hail_real_estate__model_v0_1__docs_r1.csv` | `29cf91ef3008c3e0e35e24ee3a5b7ebeb2e3c29d4372c61ad1eb35f1e36f4c03` |

The package has six curve records (three buildings × two priced units) with 205 knots each, and 206 known-answer
tests: 180 formula, 12 withheld and 14 error tests.

## 2. Validator result

`python scripts/reference_helpers/validate_hail_real_estate_v0_1_package.py` (Python 3.11.15, jsonschema 4.26,
openpyxl 3.1.5): **68/68 checks pass**. The checks cover:

- **Files and schemas.** Required files; schemas (bundle v3, capability v3, every emit against damage emit v2);
  embedded capability equal to the standalone one.
- **Registers.** Rectangular with LF endings, and every source ID resolving.
- **Fragility table.** Onset below full, hail-facing shares in (0, 1], roof shares at 1. The area-based shares are
  recomputed from the profile geometry, unit cost and budget, and the Hazus roof shares from the Hazus arithmetic.
- **Re-derivation.** The ordinates and sensitivity re-derived from the fragility table match the committed CSVs.
- **Records.** Equal to the ordinates; knots 0–203 mm plus 203.2 mm; values in [0, 1]; non-decreasing; zero at 0 mm;
  roof records reaching 1; walls records levelling off at the value-weighted hail-facing share; unit shares equal to
  the table; unit flags present.
- **Loader compatibility.** Unique routing for every building × unit, one range and one axis field
  (`mesh_diameter_mm`, the same as hail × solar), the acknowledgement on walls records only, and withheld units
  marked `withheld_not_zero`.
- **Reproducibility and tests.** The builder reproduces the JSON outputs; all 206 known-answer tests pass through the
  reference evaluator.
- **Non-promotion.** The cell is absent from the artifact index and version registry, has no `current/`, and its
  gate is blocked.
- **Other.** The NRI receipt pins the current ordinates; the profile binding covers every profile × unit, with
  records and evidence resolving and one profile revision; workbook sheets; Markdown links.

**Reproducibility:** rerunning the derive, build and binding scripts reproduces every file byte for byte, including
the chart. The exception is the Excel workbook, which has the same sheets and values but different zip timestamps.

**Name check:** a separate grep of every committed file of the cell and its scripts found no personal names other
than JL and published authors in citations.

## 3. Hand checks

These were computed directly from the formula with the band numbers typed in again, not through the scripts:

| Case | By hand (exact expression) | Package (1-mm table) |
|---|---|---|
| House roof at 38.98 mm (MESH75 floor) | 0.417256 | 0.417271 |
| Warehouse roof at 76.2 mm (3 in) | 0.554772 | 0.554635 |
| Office windows at 50.8 mm (2 in): 0.25 × P | 0.145580 | 0.145537 |

The largest difference between the 1-mm table and the exact expression, over every record at 0.05-mm steps, is
0.0011, on the house roof near 33.5 mm. That equals 0.004% of the house's structure value. The lognormal spreads are
β 0.102 (warehouse roof), 0.143 (house roof), 0.155 (windows) and 0.211 (office roof).

## 4. Consumer probe (Hazard common v3 loader, read-only)

`check_hail_real_estate_hazard_loader.py` runs every known-answer request through a copy of Hazard's
`drivers/deep/src/deep/damage_loader.py` (main `20de3770b039d709b6867578dcb6d0672c2c7234`, blob `4bdadaa1`).

**198 of 206 agree.** That includes every priced value (both units, all three buildings, the acknowledged walls
unit) and every withheld result (above 203.2 mm; exposed equipment; contents). The eight differences are error-code
names only:

| Cell code | Hazard loader code | Count |
|---|---|---|
| `PATHWAY_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `PATHWAY_ID_UNKNOWN` | `UNSUPPORTED_PATHWAY` | 1 |
| `REFERENCE_BUILDING_ID_REQUIRED` | `MISSING_REQUIRED_FIELD` | 1 |
| `REFERENCE_BUILDING_ID_UNKNOWN` | `SELECTOR_MISMATCH` | 2 |
| `FAILURE_UNIT_ID_REQUIRED` | `FAILURE_UNIT_ID_UNKNOWN` | 1 |
| `SCREENING_ASSUMPTION_SET_REQUIRED` (walls without acknowledgement) | `CURVE_SELECTOR_MATCH_NOT_UNIQUE` | 1 |
| `SCREENING_ASSUMPTION_SET_UNSUPPORTED` | `SELECTOR_MISMATCH` | 1 |

Both sides fail closed in every case: the loader refuses the walls unit without the acknowledgement. The loader needs
no change for this cell, and the Hazard repository was not modified.

## 5. NRI check

This is an order-of-magnitude comparison with FEMA's National Risk Index on Hazard's grid (dossier §13; inputs
pinned in the [receipt](NRI_CHECK_RECEIPT_hail_real_estate__model_v0_1__docs_r1.json)). It is a check, not a
calibration.

**Inputs checked against GCS (read-only, 2026-10-18).** The check ran on local copies. Each matches its GCS original:

| Input | Compared by | Result |
|---|---|---|
| Hazard M1 QC table | SHA-256 | identical (`c92c0219…`) |
| Hazard M0 daily partitions (2,071 files) | MD5 of every file | all identical |
| NRI parquet | SHA-256 | identical (`bc4f8dff…`) |

The GCS URIs are in the receipt.

**Result:** central house and office roof yearly loss is 64–73 times NRI in the median cell, with ranking agreement
0.70. NRI's own national hail building loss is far below insured experience. Under Hazard's earlier Version-1 size
transform, the house would be at NRI's level (1.2×).

## 6. Not validated here

- The roof thresholds come from engineering lab and field work. No US claims data by roof type and hail size validate
  the curves.
- The warehouse roof share, the warehouse full-damage size and the whole walls-and-windows unit are judgment (T4).
- Reading Hazard's MESH75 as the largest hailstone at a building is untested against ground truth.
- No Hazard M2–M4 run was made. The yearly figures in the NRI check apply Hazard's per-pixel rule to the raw radar
  record outside Hazard.
- Owner and reviewer acceptance (promotion gate).
