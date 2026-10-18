<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# convective_wind_real_estate damage-code metadata spec — model v0.1 / docs r1

## Damage code

| Field | Value |
|---|---|
| `damage_code_id` | `CONVECTIVE_WIND_REAL_ESTATE_EF_SCREENING_V0_1` |
| Cell / version | `convective_wind_real_estate`, model v0.1, docs r1 |
| Status | noncanonical proposal; promotion gate blocked |
| Artifact | [`convective_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json`](convective_wind_real_estate__model_v0_1__docs_r1__curve_artifact.json) (bundle v3) |
| Reference evaluator | `scripts/reference_helpers/convective_wind_real_estate_curve_eval.py` |

## Pathways

| `pathway_id` | Axis field | Records |
|---|---|---|
| `straight_line_convective` | `convective_gust_3s_10m_mph` | `CWRE_RES_EF_FR12_STRAIGHT_LINE_ONSET96`, `CWRE_IND_EF_MBS_STRAIGHT_LINE_ONSET96`, `CWRE_OFF_EF_LRB_STRAIGHT_LINE_ONSET96` |
| `tornado_direct_hit` | `tornado_gust_3s_10m_mph` | `CWRE_RES_EF_FR12_TORNADO`, `CWRE_IND_EF_MBS_TORNADO`, `CWRE_OFF_EF_LRB_TORNADO` |

## Inputs

### Hazard input

| Field | Unit | Meaning | Range |
|---|---|---|---|
| `convective_gust_3s_10m_mph` | mph | 3-second gust at 10 m, open terrain (Hazard: ASCE 7-22, Exposure C) | 0–255; above withholds; negative error |
| `tornado_gust_3s_10m_mph` | mph | 3-second tornado gust; Hazard's EF band midpoint accepted (damage-inferred) | 0–255; above withholds; negative error |

Each pathway reads only its own field. An EF rating (e.g. `"EF2"`) is not an input.

### Selectors

| Field | Required | Allowed |
|---|---|---|
| `reference_building_id` | yes, no default | `RE_RES_SFD_1S_SLAB`, `RE_IND_WAREHOUSE`, `RE_COM_OFFICE_3S_SLAB` |

Profile IDs (e.g. `re_office_3s_slab`) are not selectors; the profile binding maps them.

### Conditioners

None.

### Exposure

One reference building per call; `failure_unit_id` required (`CWRE_BUILDING_STRUCTURE`; `CWRE_BUILDING_CONTENTS`
returns withheld).

## Outputs

`damage_emit.v2`, `scalar_mean`: `scalar_central_dr` = repair cost / structure replacement cost new for one event,
with `curve_id` and metadata flags. Withheld results carry `scalar_central_dr = null` and reason codes:

| Reason code | When |
|---|---|
| `ABOVE_SOURCE_VALID_RANGE` | gust above 255 mph |
| `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` | contents requested |

Errors (fail closed): `PATHWAY_ID_REQUIRED`, `PATHWAY_ID_UNKNOWN`, `REFERENCE_BUILDING_ID_REQUIRED`,
`REFERENCE_BUILDING_ID_UNKNOWN`, `AXIS_PAYLOAD_REQUIRED`, `AXIS_VALUE_INVALID`, `AXIS_OUTSIDE_VALID_RANGE`,
`FAILURE_UNIT_ID_REQUIRED`, `FAILURE_UNIT_ID_UNKNOWN`. Hazard's generic loader returns its own names for five of
these (validation report §4).

Always-on flags: `NONCANONICAL_PROPOSAL`, `SCREENING_EF_EXPERT_ELICITED_DEGREES_OF_DAMAGE`,
`WHOLE_BUILDING_SOURCE_ATOM`, `COST_RATIOS_ASSIGNED_THROUGH_HAZUS_DAMAGE_STATES`,
`EF_GUST_AT_POINT_OF_DAMAGE_NOT_STATED_EXPOSURE_C`, `REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED`,
`NOT_FIELD_OR_CLAIMS_CALIBRATED`, `PLATFORM_CODES_PROPOSED_NOT_ISSUED`. Straight-line records add
`STRAIGHT_LINE_T4_TRANSFER_OF_TORNADO_EF_EVIDENCE`, `NO_DAMAGE_BELOW_96_MPH_ONSET`,
`ONSET_FIXED_NOT_LOCATION_SPECIFIC`; tornado records add `TORNADO_EF_DEGREE_OF_DAMAGE_EVIDENCE`,
`TORNADO_SPECIFIC_EFFECTS_INSIDE_EF_OBSERVATIONS`, `EF_MIDPOINT_GUST_ACCEPTED_AS_T4_BRIDGE`.

## Capability declaration

Per pathway: failure-unit scalar DR conditional; scenario loss withheld (consumer value qualification); intrinsic
spread not carried; annual and tail metrics consumer-owned and withheld before promotion. Cap binding is
consumer-enforced and fail-closed: exact pin, routing by pathway and building, one pathway per event, and all perils on
one building in one event at most 100% of structure value.

## Example

```json
{"pathway_id": "straight_line_convective", "failure_unit_id": "CWRE_BUILDING_STRUCTURE",
 "reference_building_id": "RE_IND_WAREHOUSE", "convective_gust_3s_10m_mph": 120}
```

→ `CWRE_IND_EF_MBS_STRAIGHT_LINE_ONSET96`, `scalar_central_dr` 0.30783 (30.8% of structure value).
