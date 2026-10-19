<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
-->

# Validation report — tropical_cyclone_wind_real_estate model v0.1 / docs r1

Run on 2026-10-12 against Damage `main` @ `02eba9b` plus this branch, Python 3.12 with jsonschema, referencing and
openpyxl.

## 1. Package files

| File | sha256 |
|---|---|
| `tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json` | `a348092d6e5b0a42631a4729ea56483036174e2139783cae9d0bead117516abd` |
| `tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__capability.json` | `bd13820c138f25f254c6750d1b9ddef0b7e337270f066729a2447236d51b93df` |
| `known_answer_tests_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.json` | `e0891480859aaa434a9b7ff4e50e1dd55dd8f920d20df6650343f6cfdcd84b80` |
| `CURVE_ORDINATES_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv` (governed input) | `2276a79d03ccc7ae05803a4ec2bb2cf3c431cd007689113b30a11971e6a950fc` |
| `damage_curve_records_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.xlsx` | workbook bytes change on every rebuild (the zip stores write times); its content is checked by sheet |

Rebuilding twice gives identical JSON bytes.

## 2. Validator result

```bash
python scripts/reference_helpers/validate_tropical_cyclone_wind_real_estate_v0_1_package.py
```

**47/47 checks pass**, including:

- the artifact against bundle v3, the capability against capability v3, every evaluator output against damage emit v2;
- the 15 records equal the governed ordinates CSV (values, Hazus wbIDs, 41 speeds 50–250 mph, values in [0, 1],
  0 at 50 mph); dips ≤ 0.005 and only above 200 mph, and flagged;
- loader routing: the required selectors are exactly the routing fields, each building × terrain routes to one
  record, all records share the pathway range, optional characteristic selectors admit only reference values;
- the builder reproduces the artifact and the tests byte-for-byte;
- **719 known-answer tests** through the reference evaluator: 615 published points, 45 between points (122.5,
  61.4 and 228.8 mph per record), 15 below-range zeros, 15 above-range withholds, reference-characteristic and
  variant tests per building, contents withheld, and 15 error cases;
- not in the artifact index or version registry; no `current/` package; promotion gate blocked;
- workbook sheets; Markdown links in the cell.

Ordinate extraction and cross-check (source files outside the repo, SHA-256 pinned):

```bash
python scripts/reference_helpers/extract_tropical_cyclone_wind_real_estate_hazus_ordinates.py \
    HazusWindDamFunctions_Hazus61.xlsx loss_repair.csv
# wrote 615 ordinates (15 records) …; cross-checked against SimCenter: identical
```

Repository tests (`PYTHONPATH=src pytest`): 7 pass; the 2 `test_publisher_plan.py` failures are the same as on
`main` and unrelated to this cell.

## 3. Hand checks

| Request | Evaluator | By hand |
|---|---|---|
| House, suburban, 132 mph | 0.3131338 | 0.263409 + 0.4 × (0.387721 − 0.263409) |
| Warehouse, open, 61.4 mph | 6.7875 × 10⁻⁵ | 2.82796e-5 + 0.28 × (1.6969e-4 − 2.82796e-5) |
| Warehouse, trees, 228.8 mph | 1.0 | published 1.0 at 225 and 230 mph |
| Commercial, open vs light suburban, 130 mph | 0.185789 vs 0.277288 | published values; the crossing is the source's (TCRE-C024) |
| Warehouse, suburban, 250.5 mph | withheld, `ABOVE_SOURCE_VALID_RANGE` | above the published 250 mph |
| House, open, 140 mph, `hazus_shutters: yes` | withheld, `WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED` | shuttered variant not published in v0.1 |

## 4. Consumer integration findings (for Hazard, at cutover)

The known-answer requests were run through a copy of Hazard's generic v3 loader
(`drivers/deep/src/deep/damage_loader.py`, `origin/main` @ `e8664800`, read-only):

```bash
python scripts/reference_helpers/check_tropical_cyclone_wind_real_estate_hazard_loader.py <dir with damage_loader.py>
```

**688 of 719 agree**, including every priced value (all published points, all in-between points), every
above-range withhold and the contents withhold. The differences:

| Requests | This cell | Hazard loader | Matters? |
|---|---|---|---|
| 16 gusts below 50 mph (0–40 mph) | 0, `BELOW_SOURCE_RANGE_ZERO` | error `AXIS_OUTSIDE_VALID_RANGE` | No for the CONUS grid (it delivers ≥ 61 mph); align at cutover |
| 4 non-reference characteristic values (e.g. shutters yes) | withheld, `WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED` | error `SELECTOR_MISMATCH` | Both refuse to price it. Before the reference-only selectors were added, the loader priced it **as the reference building** |
| 1 characteristic the building does not have (house + window area `low`) | error `WIND_CHARACTERISTIC_NOT_APPLICABLE` | priced as the reference | Narrow: the loader's selector check is not building-specific, so a value that is the reference for *another* building passes. Harmless while only reference values exist; must be building-aware before measure variants are published |
| 1 unknown `hazus_*` field | error `WIND_CHARACTERISTIC_FIELD_UNKNOWN` | ignored, priced | Loader ignores undeclared fields |
| 9 malformed requests (missing or unknown pathway, building, terrain; negative gust; unknown characteristic value) | specific error codes | generic error codes (`MISSING_REQUIRED_FIELD`, `SELECTOR_MISMATCH`, `UNSUPPORTED_PATHWAY`, `AXIS_OUTSIDE_VALID_RANGE`) | Both fail closed; code names differ |

Other integration needs:

```text
- Hazard must send hazus_terrain_class per building location (no field exists today); the loader fails closed
  (MISSING_REQUIRED_FIELD) without it, which is the intended behaviour;
- the gust must stay the open-terrain gust (Hazard applies no roughness today; keep it that way for this cell);
- combining wind and flood damage on one building in one storm (≤ 100%) is a consumer rule; Hazard's
  return-period rasters carry no storm identity today;
- the hurricane CONUS builders are asset-specific (solar.py, wind_farm.py); a real-estate builder would be new.
```

## 5. Not validated here

```text
- loss-claims calibration of the three Hazus variants (none located; screening grade);
- the Hazus 7.0 software database itself (Windows installer; the 6.1 extract and the 5.1 copy agree, and the 7.0
  manual describes no function change);
- the per-area replacement cost (not selected; scenario dollars withheld);
- a terrain-class mapping from land cover (consumer-owned);
- an independent reviewer pass on the package.
```
