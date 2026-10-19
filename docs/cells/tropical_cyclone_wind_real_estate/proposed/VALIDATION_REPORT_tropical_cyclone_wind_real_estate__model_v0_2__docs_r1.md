<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# Validation report — tropical_cyclone_wind_real_estate model v0.2 / docs r1

Package state: **noncanonical proposal**, not in the artifact index or version registry, no `current/` package.
Promotion gate: **blocked** (owner review). Model v0.1 is kept unchanged and still passes its own validator
([v0.1 report](VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)).

## 1. Package files

| File | sha256 |
|---|---|
| `tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__curve_artifact.json` | `99487ff5812e6b1017eeaaeea14d469bcb15ae2265e9d6cf107ce5ca41c85753` |
| `tropical_cyclone_wind_real_estate__model_v0_2__docs_r1__capability.json` | `ecd92ca2e816e3a58b51361a8bfb0ad21282fae711c905af6021a1961927653f` |
| `known_answer_tests_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.json` | `8758825ff2e9530562ef68fc88b5fca981b676d9aeadfd2eea8dc5b8b109b7be` |
| `CURVE_ORDINATES_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv` (governed input) | `d0e1abc7b610071f110e476f364a18d7b13b806ad17e8cff87547ce0df6d27ff` |
| `VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv` | `a03e1b2e9757b653e0c35aab34e891ecb970481bc80b387ee20385db85d5ea8c` |
| `PROFILE_BINDING_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.csv` | `bac98d16df7a08f971c5c1497c53836d0fafb2b3b76c04b4a17ee16c3d3d496b` |
| `damage_curve_records_tropical_cyclone_wind_real_estate__model_v0_2__docs_r1.xlsx` | `115ff705587613a3f940e2ff7ba7758004b2d19c2a62b34dfc68ea928aa31eff` (zip write times change the bytes on each rebuild; content is checked by sheet) |

The ordinates and sensitivity come from `extract_tropical_cyclone_wind_real_estate_v0_2_hazus_ordinates.py` (FEMA Hazus
6.1 extract, TCRE-S002, sha256 `0fe93bbd…`); all 32 curves it reads for a governed or reference row are identical to
SimCenter's independent Hazus 5.1 copy (TCRE-S003). Built by `build_tropical_cyclone_wind_real_estate_v0_2_package.py`;
binding by `tropical_cyclone_wind_real_estate_profile_binding.py`. The registers are shared with model v0.1.

## 2. Validator result

`python scripts/reference_helpers/validate_tropical_cyclone_wind_real_estate_v0_2_package.py` (jsonschema 4.25,
openpyxl 3.1.5):

```text
PASS  required files exist
PASS  embedded capability equals standalone capability
PASS  artifact paths resolve (dossier, workbook, KATs, registers, crosswalk)
PASS  artifact validates against bundle v3
PASS  capability validates against capability v3
PASS  registers rectangular, LF line endings (sources, claims, tiers, crosswalk, ordinates, sensitivity)
PASS  curve, claim, parameter-tier and ordinate source IDs resolve
PASS  artifact ordinates and Hazus variants equal the governed CSV (20 records)
PASS  every record has the 41 published speeds 50..250 mph; values in [0, 1]; 0 at 50 mph
PASS  dips are at most 0.005 (D-TCRE-25); records with dips carry the dip flag (and only they)
PASS  routing fields are exactly the required selectors; selector_match keys equal the routing fields
PASS  optional characteristic selectors admit only reference values
PASS  every building × terrain routes to exactly one record; all records share the pathway valid_range
PASS  no conditioner is required
PASS  builder reproduces the artifact JSON and the known-answer tests
PASS  known-answer tests pass (954)
PASS  cell absent from the artifact index and version registry; no current/ package
PASS  artifact is noncanonical and proposed
PASS  profile binding records and evidence resolve; pinned to one profile revision
PASS  profile binding agrees with the artifact's reference_profile_binding
PASS  workbook has the expected sheets
PASS  Markdown links in the cell resolve
50/50 checks passed
```

## 3. Hand checks

| Request | Evaluator | By hand |
|---|---|---|
| Office, suburban, 120 mph | 0.100962 (`TCRE_OFF_HAZUS_SECBM_SUBURBAN`) | published point |
| Office, open vs light suburban, 120 mph | 0.140212 vs 0.17394 | published values; the crossing is the source's (as for SECBL) |
| Warehouse, open, 122.5 mph | 0.298319 (`TCRE_IND_HAZUS_SPMBL_NEWDECK_OPEN`) | 0.234762 + 0.5 × (0.361876 − 0.234762) |
| House, suburban, 132 mph | 0.3131338 | unchanged from v0.1 |
| Warehouse, open, 120 mph, `hazus_roof_deck_age: old` | withheld, `WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED` | v0.2 publishes only the new-or-average deck |

## 4. Consumer probe (Hazard common v3 loader, read-only)

`drivers/deep/src/deep/damage_loader.py` at Hazard_Modeling `main` @ `509bf435` (blob `4bdadaa1`):

```bash
python scripts/reference_helpers/check_tropical_cyclone_wind_real_estate_hazard_loader.py <dir with damage_loader.py> v0_2
```

**916 of 954 agree**, including every priced value for all four buildings and five terrains, every above-range
withhold and the contents withhold. The differences are the same kinds as in v0.1 (v0.1 report §4), with the new
office and warehouse rows added:

| Requests | This cell | Hazard loader |
|---|---|---|
| 21 gusts below 50 mph | 0, `BELOW_SOURCE_RANGE_ZERO` | error `AXIS_OUTSIDE_VALID_RANGE` |
| 5 non-reference characteristic values | withheld, `WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED` | error `SELECTOR_MISMATCH` (both refuse to price) |
| 1 characteristic the building does not have | error `WIND_CHARACTERISTIC_NOT_APPLICABLE` | priced as the reference |
| 1 unknown `hazus_*` field | error `WIND_CHARACTERISTIC_FIELD_UNKNOWN` | ignored, priced |
| 10 malformed requests (including a profile ID sent as a selector) | specific error codes | generic error codes; both fail closed |

The v0.1 integration needs stand: a terrain-class field per location, the open-terrain gust kept as is, the wind +
flood ≤ 100% rule for one storm, and a real-estate CONUS builder on the Hazard side.

## 5. Not validated here

```text
- loss-claims calibration of the Hazus variants (screening grade);
- code-built house connections by location (stated sensitivity only; needs a code or design-wind zone per cell);
- the effect of the warehouse's large overhead doors (not a Hazus characteristic);
- dollar outputs (the consumer qualifies each reference budget);
- an independent reviewer pass on the package.
```
