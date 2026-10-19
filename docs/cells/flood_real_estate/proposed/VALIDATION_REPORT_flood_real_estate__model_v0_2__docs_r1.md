<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# Validation report — flood_real_estate model v0.2 / docs r1

Package state: **noncanonical proposal**, not in the artifact index or version registry, no `current/` package.
Promotion gate: **blocked** (owner review). Model v0.1 is kept unchanged and still passes its own validator
([v0.1 report](VALIDATION_REPORT_flood_real_estate__model_v0_1__docs_r1.md), 29/29).

## 1. Package files

| File | sha256 |
|---|---|
| `flood_real_estate__model_v0_2__docs_r1__curve_artifact.json` | `99fe3f1f6430caada7943a4a83fe74a2f94895c8c454d7789fda97fabfafe9af` |
| `flood_real_estate__model_v0_2__docs_r1__capability.json` | `ae049535b2d448b7ee41b3c9792d965164d5b835c70ff2e5fe6070bdff8d8a7b` |
| `known_answer_tests_flood_real_estate__model_v0_2__docs_r1.json` | `0d6263113b96985b7cd8f5b5f8df82114413bf2af08d3ead990f853e3e584106` |
| `CURVE_ORDINATES_flood_real_estate__model_v0_2__docs_r1.csv` (governed input) | `80448faa5a55fcc4e44dc966f4fae452d4f012cfd4a7cb1b376b2f4306f8bc92` |
| `PROFILE_BINDING_flood_real_estate__model_v0_2__docs_r1.csv` | `e5e9ad57753b2276cd0fd8efdbbde44c5eacd8f9f8e322baea5e8f6280454cfa` |
| `damage_curve_records_flood_real_estate__model_v0_2__docs_r1.xlsx` | `62c56e8e0b265cec09cc4990e2edff08fd1c259be814c2f6867825be42e13ef8` (zip write times change the bytes on each rebuild; content is checked by sheet) |

Built by `scripts/reference_helpers/build_flood_real_estate_v0_2_package.py`; the binding and sensitivity tables by
`flood_real_estate_profile_binding.py`. The registers are shared with model v0.1 and keep their docs-r1 names.

## 2. Validator result

`python scripts/reference_helpers/validate_flood_real_estate_v0_2_package.py` (jsonschema 4.25, openpyxl 3.1.5):

```text
PASS  required files exist
PASS  embedded capability equals standalone capability
PASS  artifact paths resolve (dossier, workbook, KATs, registers, crosswalk)
PASS  artifact validates against bundle v3
PASS  capability validates against capability v3
PASS  registers rectangular (sources, claims, tiers, crosswalk, ordinates)
PASS  curve, claim and parameter-tier source IDs resolve to the source register
PASS  artifact ordinates equal the governed ordinates CSV (7 records)
PASS  every record is non-decreasing with depth
PASS  builder reproduces the artifact JSON and the known-answer tests
PASS  known-answer tests pass (185), each output also valid against damage emit v2
PASS  cell absent from the artifact index and version registry; no current/ package
PASS  artifact is noncanonical and proposed; promotion gate blocked
PASS  profile binding records and evidence resolve; pinned to one profile revision
PASS  profile binding agrees with the artifact's reference_profile_binding
PASS  one-record buildings return the same value for both water types
PASS  workbook has the expected sheets
PASS  Markdown links in the cell resolve
33/33 checks passed
```

The 185 known-answer tests cover every published point of the five point records, interior points, the
depth-above-grade bridge, the dry-ground rule, below- and above-range behaviour for **both water types** on the
house, warehouse and office records, the retail NACCS bounds at 4 ft, unknown water type for every building, the
withheld contents unit, a first-floor-height override, and twelve contract errors (including a profile ID sent as
a selector).

## 3. Hand checks

| Request | Evaluator | By hand |
|---|---|---|
| House, coastal surge, 2 ft above grade (floor 0.75 ft) | 0.2525 (`FRE_RES_HAZUS_DF129`) | 0.23 + 0.25 × (0.32 − 0.23) = 0.2525; v0.1 gave 0.205 (NACCS 5A) |
| Office, freshwater, 2 ft above grade (floor 0.25 ft) | 0.1475 (`FRE_OFF_HAZUS_DF431`) | 0.11 + 0.75 × (0.16 − 0.11) = 0.1475 |
| Warehouse, coastal surge, 12 ft above grade | 0.40 (`FRE_IND_HAZUS_DF341`) | DF 341 at 11.75 ft above the floor: 0.40 (straight line between the 11 and 12 ft points); v0.1 withheld (NACCS range ends at 10 ft) |

## 4. Consumer probe (Hazard common v3 loader, read-only)

`drivers/deep/src/deep/damage_loader.py` at Hazard_Modeling `main` @ `509bf435` (blob `4bdadaa1`), function
`evaluate_v3_damage_call`, requests with `flood_depth_above_first_floor_ft`:

| Building | Water | ft above floor | Hazard loader | Reference evaluator |
|---|---|---|---|---|
| House | freshwater | 2 | conditional, DF 129, 0.32 | same |
| House | coastal surge | 2 | conditional, DF 129, 0.32 | same |
| Warehouse | freshwater / coastal | 2 | conditional, DF 341, 0.08 | same |
| Office | freshwater / coastal | 2 | conditional, DF 431, 0.16 | same |
| House | coastal surge | 30 | withheld, `ABOVE_SOURCE_VALID_RANGE` | same |
| House | unknown | 2 | withheld, `FLOOD_WATER_TYPE_UNKNOWN` | same |
| House | freshwater | −0.75 (dry slab) | conditional, 0.055 | same with floor-relative input; 0 with above-grade input |
| Retail (unbound) | coastal surge | 2 | error `CURVE_SELECTOR_MATCH_NOT_UNIQUE` | 0.30 (NACCS P2) |

Findings against the v0.1 integration notes (v0.1 report §4):

1. **Record routing: resolved for the three profiles.** Each has one record whose `selector_match.flood_water_type`
   lists both water types, a form the loader already accepts. It remains for the unbound retail record only.
2. **Record-level ranges: no longer needed for the three profiles.** Their records run to 24 ft, the pathway
   range the loader enforces. Only the retail coastal record (10 ft) still needs record-level enforcement.
3. **Dry ground: still a consumer rule.** With floor-relative depth the loader returns 0.055 for a dry slab house
   (DF 129 between −1 and 0 ft). Hazard must return 0 when depth above grade is 0 or less, or send depth above
   grade to an evaluator that applies D-FRE-24.
4. **Axis field.** The loader reads `hazard_axis.preferred_input_field`; it stays
   `flood_depth_above_first_floor_ft` (an earlier v0.2 draft that preferred depth above grade made every loader call
   fail with `AXIS_PAYLOAD_REQUIRED` and was reverted).

## 5. Not validated here

```text
- calibration against observed losses (the curves are compared with NFIP claims, not refit; NFIP claims check)
- dollar outputs (the consumer qualifies each reference budget against the structure denominator)
- coastal behaviour outside the Gulf states, and wave-exposed coastal sites (deferred wave pathway)
- independent review of the package (promotion gate item)
```
