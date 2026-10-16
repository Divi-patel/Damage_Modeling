<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# flood_real_estate damage-code metadata spec — model v0.2 / docs r1

## Damage code

```yaml
damage_code_id: FLOOD_REAL_ESTATE_HAZUS_NACCS_SCREENING_V0_2
cell_id: flood_real_estate
semantic_damage_model_version: model v0.2
documentation_revision: docs r1
artifact_schema_version: damage_curve_record_bundle.v3
canonical_runtime_artifact: false
model_grade: screening_source_native_adopted_tables
reference_evaluator: scripts/reference_helpers/flood_real_estate_curve_eval.py
supersedes_proposal: model v0.1 / docs r1 (kept for reproducibility)
```

## Pathways

| pathway_id | Status | Axis |
|---|---|---|
| `flood_inundation_contact` | proposed, numeric | depth above the first finished floor, ft |
| `flood_wave_velocity` | declared, deferred; not in the artifact | — |

## Inputs

### Hazard inputs

Exactly one axis mode per request:

| Mode | Fields | Notes |
|---|---|---|
| `depth_above_grade_ft` (reference evaluator) | `flood_depth_above_grade_ft` (≥ 0), optional `first_floor_height_ft` | Without `first_floor_height_ft` the reference default applies and `REFERENCE_FIRST_FLOOR_HEIGHT_DEFAULT_USED` is flagged. Depth above grade of 0 returns 0 with `NOT_INUNDATED_ABOVE_GRADE`. |
| `depth_above_first_floor_ft` (source-native; read by the common v3 loader) | `flood_depth_above_first_floor_ft` | Flagged `DEPTH_ABOVE_FLOOR_SUPPLIED_DIRECTLY`. The consumer converts from grade once and applies the dry-ground rule. |

### Selectors

| Field | Required | Allowed | Reference profile | First-floor height |
|---|---|---|---|---|
| `reference_building_id` | yes | `RE_RES_SFD_1S_SLAB` | `re_house_1s_wood_slab` | 0.75 ft |
| | | `RE_IND_WAREHOUSE` | `re_warehouse_1s_steel_slab` | 0.25 ft |
| | | `RE_COM_OFFICE_3S_SLAB` | `re_office_3s_slab` | 0.25 ft |
| | | `RE_COM_LOWRISE` (retail) | none | 0.25 ft |

### Conditioners

| Field | Required | Allowed | Numeric when | Otherwise |
|---|---|---|---|---|
| `flood_water_type` | yes | `freshwater_riverine_or_pluvial`, `coastal_surge_saline`, `unknown` | the first two | withheld, `FLOOD_WATER_TYPE_UNKNOWN` |

House, warehouse and office return the same record for both numeric water types; retail routes to its freshwater
or coastal record.

### Exposure

One reference building. Scenario dollars need structure replacement cost new for that building; the consumer
qualifies the reference budget.

## Outputs

`damage_emit.v2`, one result for `FRE_BUILDING_STRUCTURE`:

| Building, water | Record | Emit mode |
|---|---|---|
| House, either | `FRE_RES_HAZUS_DF129` | `scalar_mean` |
| Warehouse, either | `FRE_IND_HAZUS_DF341` | `scalar_mean` |
| Office, either | `FRE_OFF_HAZUS_DF431` | `scalar_mean` |
| Retail, freshwater | `FRE_COM_FRESH_HAZUS_DF217` | `scalar_mean` |
| Retail, coastal surge | `FRE_COM_COAST_NACCS_P2` | `scalar_mean_plus_bounds` (NACCS Min/Max building-variant bounds) |

Withheld results carry `scalar_central_dr: null` and reason codes: `ABOVE_SOURCE_VALID_RANGE`,
`FLOOD_WATER_TYPE_UNKNOWN`, `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` (contents). Contract errors raise codes such as
`PATHWAY_ID_REQUIRED`, `REFERENCE_BUILDING_ID_UNKNOWN`, `AXIS_PAYLOAD_AMBIGUOUS`, `NEGATIVE_DEPTH_ABOVE_GRADE`.

## Capability declaration

See [`flood_real_estate__model_v0_2__docs_r1__capability.json`](flood_real_estate__model_v0_2__docs_r1__capability.json).
