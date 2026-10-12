<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
-->

# flood_real_estate damage-code metadata spec — model v0.1 / docs r1

## Damage code

```yaml
damage_code_id: FLOOD_REAL_ESTATE_HAZUS_NACCS_SCREENING_V0_1
cell_id: flood_real_estate
semantic_damage_model_version: model v0.1
documentation_revision: docs r1
artifact_schema_version: damage_curve_record_bundle.v3
canonical_runtime_artifact: false
model_grade: screening_source_native_adopted_tables
reference_evaluator: scripts/reference_helpers/flood_real_estate_curve_eval.py
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
| `depth_above_grade_ft` (preferred for the grid) | `flood_depth_above_grade_ft` (≥ 0), optional `first_floor_height_ft` | Without `first_floor_height_ft` the reference default applies and `REFERENCE_FIRST_FLOOR_HEIGHT_DEFAULT_USED` is flagged. Depth above grade of 0 returns 0 with `NOT_INUNDATED_ABOVE_GRADE`. |
| `depth_above_first_floor_ft` | `flood_depth_above_first_floor_ft` | Flagged `DEPTH_ABOVE_FLOOR_SUPPLIED_DIRECTLY`. |

### Selectors

| Field | Required | Allowed | Effect |
|---|---|---|---|
| `reference_building_id` | yes | `RE_RES_SFD_1S_SLAB`, `RE_COM_LOWRISE`, `RE_IND_WAREHOUSE` | Picks the occupancy-specific record and the default first-floor height (0.75 / 0.25 / 0.25 ft) |

### Conditioners

| Field | Required | Allowed | Numeric when | Otherwise |
|---|---|---|---|---|
| `flood_water_type` | yes | `freshwater_riverine_or_pluvial`, `coastal_surge_saline`, `unknown` | the first two | withheld, `FLOOD_WATER_TYPE_UNKNOWN` |

### Exposure

One reference building. Scenario dollars need structure replacement cost new for that building; not supplied in
v0.1.

## Outputs

`damage_emit.v2`, one result for `FRE_BUILDING_STRUCTURE`:

| Water type | Emit mode | Fields |
|---|---|---|
| freshwater | `scalar_mean` | `scalar_central_dr` |
| coastal surge | `scalar_mean_plus_bounds` | `scalar_central_dr` (NACCS ML) and `scenario_drs.naccs_min_building_variant` / `naccs_max_building_variant` |

Withheld results carry `scalar_central_dr: null` and reason codes: `ABOVE_SOURCE_VALID_RANGE`,
`FLOOD_WATER_TYPE_UNKNOWN`, `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` (contents). Contract errors raise codes such as
`PATHWAY_ID_REQUIRED`, `PATHWAY_ID_UNKNOWN`, `REFERENCE_BUILDING_ID_UNKNOWN`, `AXIS_PAYLOAD_AMBIGUOUS`,
`NEGATIVE_DEPTH_ABOVE_GRADE`.

## Capability declaration

See [`flood_real_estate__model_v0_1__docs_r1__capability.json`](flood_real_estate__model_v0_1__docs_r1__capability.json):
DR conditional; scenario dollars withheld; bounds are a non-probabilistic envelope; annual and tail metrics
consumer-owned and withheld; promotion gate blocked.
