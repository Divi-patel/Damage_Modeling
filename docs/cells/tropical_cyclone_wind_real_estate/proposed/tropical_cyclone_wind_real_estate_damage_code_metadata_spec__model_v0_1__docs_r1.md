<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
-->

# tropical_cyclone_wind_real_estate damage-code metadata spec — model v0.1 / docs r1

## Damage code

```yaml
damage_code_id: TROPICAL_CYCLONE_WIND_REAL_ESTATE_HAZUS_SCREENING_V0_1
cell_id: tropical_cyclone_wind_real_estate
semantic_damage_model_version: model v0.1
documentation_revision: docs r1
artifact: tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json (damage_curve_record_bundle.v3, proposed_draft)
canonical_runtime_artifact: false
reference_evaluator: scripts/reference_helpers/tropical_cyclone_wind_real_estate_curve_eval.py
emit: damage_emit.v2, scalar_mean
```

## Pathways

| pathway_id | Status | Axis |
|---|---|---|
| `tropical_cyclone_wind` | proposed, numeric | peak 3-second gust at 10 m, open terrain, mph |

## Inputs

### Hazard input

| Field | Unit | Valid | Notes |
|---|---|---|---|
| `tc_peak_gust_3s_10m_mph` | mph | number ≥ 0 | Open-terrain gust. Do not reduce it for terrain; terrain is a selector. 0–50 returns 0 (`BELOW_SOURCE_RANGE_ZERO`); > 250 withholds (`ABOVE_SOURCE_VALID_RANGE`); negative or non-number is an error. |

### Selectors

| Field | Required | Allowed | Effect |
|---|---|---|---|
| `reference_building_id` | yes | `RE_RES_SFD_1S_SLAB`, `RE_COM_LOWRISE`, `RE_IND_WAREHOUSE` | Picks the Hazus type (WSF1 / SECBL / SPMBL) and characteristics |
| `hazus_terrain_class` | yes, no default | `open`, `light_suburban`, `suburban`, `light_trees`, `trees` | Picks the terrain record; never interpolated |

### Wind building characteristics (optional)

Omitted → the reference value is used and `REFERENCE_WIND_CHARACTERISTICS_DEFAULT_USED` is flagged. Supplied and equal
to the reference → used. Supplied, valid, different → **withheld**, `WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED`.
A field the building does not have, or a value outside the list, is an error.

| Field | House (reference · allowed) | Commercial | Warehouse |
|---|---|---|---|
| `hazus_roof_shape` | `gable` · gable, hip | — | — |
| `hazus_secondary_water_resistance` | `no` · no, yes | — | — |
| `hazus_roof_deck_attachment` | `6d_6_12` · 6d_6_12, 8d_6_12, 6d8d_mix_6_6, 8d_6_6 | — | — |
| `hazus_roof_to_wall_connection` | `toe_nail` · toe_nail, strap | — | — |
| `hazus_garage_door` | `none` · none, weak, standard, sfbc_1994 | — | — |
| `hazus_roof_cover` | `shingle` · shingle | `bur` · bur, spm | — |
| `hazus_window_area` | — | `low` · low, medium, high | — |
| `hazus_windborne_debris_environment` | — | `varies_by_direction` · residential_commercial, varies_by_direction, residential, none | — |
| `hazus_metal_deck_attachment` | — | `standard` · standard, superior | `standard` · standard, superior |
| `hazus_roof_deck_age` | — | — | `old` · old, new_or_average |
| `hazus_shutters` | `no` · no, yes | `no` · no, yes | `no` · no, yes |

The same fields are also declared as optional selectors that admit only the reference values, so a generic loader
that does not read `wind_characteristic_contract` refuses a variant instead of pricing it as the reference.

### Conditioners

None.

### Exposure

One reference building per call. No protection credit outside the published characteristic values.

## Outputs

| Status | Fields |
|---|---|
| `conditional` | `scalar_central_dr` (fraction of structure replacement cost new), `curve_id`, flags |
| `withheld` | `scalar_central_dr: null`, `withheld_reason_codes` |

Reason codes (withheld): `ABOVE_SOURCE_VALID_RANGE`, `WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED`,
`NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT`, `CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT`.

Error codes: `PATHWAY_ID_REQUIRED`, `PATHWAY_ID_UNKNOWN`, `REFERENCE_BUILDING_ID_REQUIRED`,
`REFERENCE_BUILDING_ID_UNKNOWN`, `TERRAIN_CLASS_REQUIRED`, `TERRAIN_CLASS_UNKNOWN`, `AXIS_PAYLOAD_REQUIRED`,
`AXIS_VALUE_INVALID`, `NEGATIVE_GUST`, `FAILURE_UNIT_ID_UNKNOWN`, `WIND_CHARACTERISTIC_FIELD_UNKNOWN`,
`WIND_CHARACTERISTIC_NOT_APPLICABLE`, `WIND_CHARACTERISTIC_VALUE_UNKNOWN`.

Flags always present: `NONCANONICAL_PROPOSAL`, `SCREENING_SOURCE_NATIVE_ADOPTED_TABLE`, `WHOLE_BUILDING_SOURCE_ATOM`,
`HAZUS_COMBINED_PRESSURE_DEBRIS_RAIN_INGRESS`, `REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED`,
`NOT_FIELD_OR_CLAIMS_CALIBRATED`, `PLATFORM_CODES_PROPOSED_NOT_ISSUED`. Record flags add the source and building
caveats (tree fall deferred; SECBL = MECBL; commercial terrain order; warehouse floor area; SPMB family anomaly;
small dips).

## Capability declaration

```text
failure-unit DR:   conditional (proposal; owner acceptance required)
scenario loss:     withheld (per-area replacement cost not selected)
spread:            not carried
annual/tail:       consumer-owned; withheld
promotion gate:    blocked
```

## Example

```json
{"pathway_id": "tropical_cyclone_wind", "reference_building_id": "RE_RES_SFD_1S_SLAB",
 "hazus_terrain_class": "suburban", "tc_peak_gust_3s_10m_mph": 132.0}
```

returns `scalar_central_dr` 0.3131338 (`TCRE_RES_HAZUS_WSF1_SUBURBAN`; 0.263409 at 130 mph and 0.387721 at 135 mph,
straight line) with `REFERENCE_WIND_CHARACTERISTICS_DEFAULT_USED`.
