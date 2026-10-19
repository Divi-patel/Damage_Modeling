<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# wildfire_real_estate damage-code metadata spec — model v0.1 / docs r1

## Damage code

| Field | Value |
|---|---|
| `damage_code_id` | `WILDFIRE_REAL_ESTATE_WRC_FSIM_SCREENING_V0_1` |
| Cell / version | `wildfire_real_estate`, model v0.1, docs r1 |
| Status | noncanonical proposal; promotion gate blocked |
| Artifact | [`wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json`](wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json) (bundle v3) |
| Reference evaluator | `scripts/reference_helpers/wildfire_real_estate_curve_eval.py` |

## Pathway and records

| `pathway_id` | Axis field | Records |
|---|---|---|
| `wildfire_building_exposure` | `conditional_flame_length_class_state` | `WFRE_RES_WRC_SHRUB`, `WFRE_IND_WRC_SHRUB_X0_8`, `WFRE_OFF_WRC_SHRUB_X0_9` |

| State | Flame-length class | House | Warehouse | Office |
|---|---|---|---|---|
| 0 | no event (control) | 0 | 0 | 0 |
| 1 | < 2 ft | 0.20 | 0.16 | 0.18 |
| 2 | 2 to < 4 ft | 0.35 | 0.28 | 0.315 |
| 3 | 4 to < 6 ft | 0.50 | 0.40 | 0.45 |
| 4 | 6 to < 8 ft | 0.65 | 0.52 | 0.585 |
| 5 | 8 to < 12 ft | 0.80 | 0.64 | 0.72 |
| 6 | 12+ ft | 0.95 | 0.76 | 0.855 |

## Inputs

### Hazard input

| Field | Unit | Meaning | Range |
|---|---|---|---|
| `conditional_flame_length_class_state` | source-native class | exact FSim conditional flame-length class at the building location (USFS RDS-2016-0034-3); native class IDs `lt_2_ft` … `gte_12_ft` map to 1 … 6; 0 = no event | integers 0–6; anything else is an error |

Burn probability is frequency and is never passed to the damage call. A flame length in feet, a fire-line intensity
or a class label is not the input.

### Selectors

| Field | Required | Allowed |
|---|---|---|
| `reference_building_id` | yes, no default | `RE_RES_SFD_1S_SLAB`, `RE_IND_WAREHOUSE`, `RE_COM_OFFICE_3S_SLAB` |
| `source_wildfire_product_id` | yes, no default | `USFS_RDS_2016_0034_3_270M` |

Profile IDs (e.g. `re_office_3s_slab`) are not selectors; the profile binding maps them.

### Conditioners

None. No lifeform, vegetation-clearance or construction-mitigation input in model v0.1 (the shrub response is used
everywhere).

### Exposure

One reference building per call; `failure_unit_id` required (`WFRE_BUILDING_STRUCTURE`; `WFRE_BUILDING_CONTENTS`
returns withheld).

## Outputs

`damage_emit.v2`, `scalar_mean`: `scalar_central_dr` = repair cost / structure replacement cost new given a fire at
the building location in that class, with `curve_id` and metadata flags. Withheld results carry
`scalar_central_dr = null` and reason codes:

| Reason code | When |
|---|---|
| `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` | contents requested |

Errors (fail closed): `PATHWAY_ID_REQUIRED`, `PATHWAY_ID_UNKNOWN`, `REFERENCE_BUILDING_ID_REQUIRED`,
`REFERENCE_BUILDING_ID_UNKNOWN`, `SOURCE_WILDFIRE_PRODUCT_ID_REQUIRED`, `SOURCE_WILDFIRE_PRODUCT_ID_UNSUPPORTED`,
`AXIS_PAYLOAD_REQUIRED`, `INVALID_CLASS_STATE`, `FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL`,
`FAILURE_UNIT_ID_REQUIRED`, `FAILURE_UNIT_ID_UNKNOWN`. Hazard's generic loader differs on some of these
(validation report §4).

Always-on flags: `NONCANONICAL_PROPOSAL`, `SCREENING_AGENCY_RESPONSE_FUNCTION_NOT_FIELD_CALIBRATED`,
`WRC_SHRUB_LIFEFORM_DEFAULT_LIFEFORM_NOT_SUPPLIED`, `WRC_LOSS_VALUE_READ_AS_REPAIR_COST_RATIO`,
`FSIM_CLASS_IS_NOT_LOCAL_HEAT_FLUX_OR_EMBER_EXPOSURE`, `WHOLE_BUILDING_SOURCE_ATOM`,
`REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED`, `NOT_FIELD_OR_CLAIMS_CALIBRATED`, `CURVE_INTRINSIC_SPREAD_NOT_CARRIED`,
`PLATFORM_CODES_PROPOSED_NOT_ISSUED`. The house record adds `WRC_HOME_RESPONSE_USED_DIRECTLY` and
`NO_EMBER_RESISTANT_VENT_OR_DEFENSIBLE_SPACE_CREDIT`; the warehouse and office records add
`WRC_HOME_RESPONSE_TIMES_DINS_SAME_FIRE_FACTOR` and `BUILDING_FACTOR_T4_TRANSFER_FROM_CALIFORNIA_COMMERCIAL_STOCK`.

## Capability declaration

Failure-unit scalar DR conditional; scenario loss withheld (consumer value qualification); intrinsic spread not
carried; annual and tail metrics consumer-owned and withheld before promotion. Cap binding is consumer-enforced and
fail-closed: exact pin, routing by building and product, exact integer states, no burn probability in the damage
call, and all perils on one building in one event at most 100% of structure value.

## Example

```json
{"pathway_id": "wildfire_building_exposure", "failure_unit_id": "WFRE_BUILDING_STRUCTURE",
 "reference_building_id": "RE_IND_WAREHOUSE", "source_wildfire_product_id": "USFS_RDS_2016_0034_3_270M",
 "conditional_flame_length_class_state": 4}
```

→ `WFRE_IND_WRC_SHRUB_X0_8`, `scalar_central_dr` 0.52 (52% of structure value).
