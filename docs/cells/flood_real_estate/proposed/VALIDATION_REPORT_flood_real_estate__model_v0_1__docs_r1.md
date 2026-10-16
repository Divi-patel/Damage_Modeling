<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-16
status: draft
-->

# Validation report — flood_real_estate model v0.1 / docs r1

Package state: **noncanonical proposal**, not in the artifact index or version registry, no `current/` package.
Promotion gate: **blocked** (owner review).

## 1. Package files

| File | sha256 |
|---|---|
| `flood_real_estate__model_v0_1__docs_r1__curve_artifact.json` | `106e3b53c8ac84f3dba7c233a261e32a8663012794d90c898e6ccab9dbd128e1` |
| `flood_real_estate__model_v0_1__docs_r1__capability.json` | `d0cd4c60c348424662ebda0bd5f16a4b7f859794034918c140722907a68cb2c5` |
| `known_answer_tests_flood_real_estate__model_v0_1__docs_r1.json` | `681ac67507c19bd3429e744604a93b496382909170baf5da7a74822ba3cc4cc7` |
| `CURVE_ORDINATES_flood_real_estate__model_v0_1__docs_r1.csv` (governed input) | `7a0e4e6a4689f3c186f9729683044f86d4086f4de84bfc0140fff3b22362918d` |
| `damage_curve_records_flood_real_estate__model_v0_1__docs_r1.xlsx` | `beb95814bc8909bd9a855cb835e15eb2c4d3d146f82a1e93a38c2d184382ef39` (workbook bytes change on every rebuild because the zip stores write times; its content is checked by sheet) |

Built by `scripts/reference_helpers/build_flood_real_estate_v0_1_package.py`; the validator confirms the builder
reproduces the artifact and test JSON exactly.

## 2. Validator result

`python scripts/reference_helpers/validate_flood_real_estate_v0_1_package.py` (jsonschema 4.23, openpyxl 3.1.5):

```text
PASS  required files exist
PASS  embedded capability equals standalone capability
PASS  artifact paths resolve (dossier, workbook, KATs, registers, crosswalk)
PASS  artifact validates against bundle v3
PASS  capability validates against capability v3
PASS  registers rectangular (sources, claims, tiers, crosswalk, ordinates)
PASS  curve, claim and parameter-tier source IDs resolve to the source register
PASS  artifact ordinates equal the governed ordinates CSV (12 records)
PASS  every record is non-decreasing with depth
PASS  builder reproduces the artifact JSON and the known-answer tests
PASS  known-answer tests pass (166), each output also valid against damage emit v2
PASS  cell absent from the artifact index and version registry; no current/ package
PASS  artifact is noncanonical and proposed; promotion gate blocked
PASS  workbook has the expected sheets
PASS  Markdown links in the cell resolve
29/29 checks passed
```

The 166 known-answer tests cover every published point of the six point records, one interior point per record,
the depth-above-grade bridge with the reference first-floor height, the dry-ground rule, below-range and
above-range behaviour, the coastal Min/Max bounds at 4 ft, unknown water type, the withheld contents unit, a
first-floor-height override, and eleven contract errors. Expected values are computed by the builder from the
ordinates CSV with its own interpolation, separately from the evaluator.

## 3. Hand checks

| Request | Evaluator | By hand |
|---|---|---|
| House, freshwater, 2 ft above grade (floor 0.75 ft) | 0.2525 | 0.23 + 0.25 × (0.32 − 0.23) = 0.2525 |
| House, coastal, 4 ft above floor | 0.375; bounds 0.25 / 0.525 | (0.33 + 0.42) / 2; (0.20 + 0.30) / 2; (0.45 + 0.60) / 2 |
| Warehouse, coastal, 12 ft above grade | withheld, `ABOVE_SOURCE_VALID_RANGE` | 11.75 ft > NACCS 10 ft |

## 4. Consumer integration findings (for Hazard, at cutover)

The proposed artifact was run through Hazard's common v3 evaluator
(`drivers/deep/src/deep/damage_loader.py`, Hazard_Modeling `main` @ `7d703c34`, blob `4bdadaa1`), read-only:

| Request | Hazard loader | This cell's contract |
|---|---|---|
| House, freshwater, 2 ft above floor | error `CURVE_SELECTOR_MATCH_NOT_UNIQUE` | 0.32 |
| House, coastal, 12 ft above floor | error `CURVE_SELECTOR_MATCH_NOT_UNIQUE` | withheld |
| House, unknown water | withheld, `FLOOD_WATER_TYPE_UNKNOWN` | withheld (agrees) |

1. **Record routing.** The loader narrows records by selector fields only. This cell routes by
   `reference_building_id` (selector) and `flood_water_type` (conditioner, an event-time state), so each building
   has two records and the loader cannot choose. Resolution options at cutover: route on the declared
   `record_routing_fields`, or reclassify water type as a routing selector by a reviewed contract change.
2. **Record-level ranges** (by code reading; not reachable while finding 1 blocks the call). The loader checks the
   pathway axis range (−4 to 24 ft) and then holds a record's last value above its last point. The coastal
   records end at 10 ft and must withhold above it (D-FRE-21), so the consumer must enforce each record's
   `valid_range`.
3. **Dry ground and the bridge.** The loader reads the direct axis field only. The depth-above-grade mode, the
   reference first-floor height and the dry-ground rule (D-FRE-24) are implemented in this cell's reference
   evaluator and would need the same at cutover.

None of these changes the scientific content. They are recorded so the consumer cutover is a deliberate,
reviewed step.

## 5. Not validated here

```text
- calibration against observed losses (curves are not refit; a comparison with NFIP claims is reported in
  NFIP_CLAIMS_CHECK, see §6)
- dollar outputs (per-area replacement cost not selected)
- independent review of the package (promotion gate item)
```

## 6. Comparison with NFIP claims (2026-10-16)

The [NFIP claims check](NFIP_CLAIMS_CHECK_flood_real_estate__model_v0_1__docs_r1.md) compares the proposed curves with 67,241 paid claims for
one-floor slab buildings (source FRE-S012, claims FRE-C026 to FRE-C031). The freshwater records agree within about
5–6 points over most depths; the NACCS coastal records sit 12–23 points below the house claims in the first 2 ft and
6–12 points above the commercial claims from 1 ft. No record changes; the coastal source decision (D-FRE-18) is open.
