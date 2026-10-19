<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
-->

# tropical_cyclone_wind_real_estate curve derivation dossier — model v0.1 / docs r1

> Noncanonical proposal. Fifteen proposed curve records in a bundle-v3 artifact that is **not** in the artifact
> index, the version registry or any package. Runtime status: `NO_RUNTIME_CURVE` until owner review and promotion.

## 1. Scope, asset boundary, and failure mechanisms

Physical damage to the **structure** of three reference buildings (house, small low-rise commercial, one-story
warehouse) from tropical-cyclone wind, as a fraction of structure replacement cost new. Out of scope: surge, waves
and rainfall flooding (`flood_real_estate`), TC-spawned tornadoes, tree fall on the house (deferred), contents,
loss of use, land and site works. Full scope: [scope README](README_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md) §2.

### 1A. Pathway architecture

One pathway, `tropical_cyclone_wind`. It contains everything the Hazus building loss function contains: wind
pressure, windborne-debris impact and rain entering through wind damage (TCRE-C002). This deliberately differs
from `tropical_cyclone_wind_solar` and `tropical_cyclone_wind_wind`, whose wind-loading-only sources exclude debris
and rain. Guardrail: no separate debris or rain-ingress pathway may be added while records are Hazus-based
(D-TCRE-04).

```yaml
pathway_id: tropical_cyclone_wind
physical_mechanism: wind pressure + windborne debris + rain ingress through wind damage (Hazus combined)
source_native_axis: peak gust at 10 m in open terrain (Hazus TM §4.3 p. 4-81)
runtime_input_field: tc_peak_gust_3s_10m_mph
unit: mph
height_duration_datum_basis: 3-second gust, 10 m, open terrain z0 0.03 m
physics_bridge: none in Damage (Hazard converts STORM 10-minute wind)
failure_units_supported: [TCRE_BUILDING_STRUCTURE]
failure_units_withheld: [TCRE_BUILDING_CONTENTS]
curve_record_ids: TCRE_{RES_HAZUS_WSF1,COM_HAZUS_SECBL,IND_HAZUS_SPMBL}_{OPEN,LIGHT_SUBURBAN,SUBURBAN,LIGHT_TREES,TREES}
capability_state: conditional DR (proposed); dollars withheld
consumer_event_identity_rule: one event_family_id; wind + flood on one building ≤ 100% of structure value
neighboring_cell_boundaries: flood_real_estate; future convective-wind and hail × real estate
```

## 2. Failure-unit decomposition and coverage

| Failure unit | Role | Value bucket | v0.1 |
|---|---|---|---|
| `TCRE_BUILDING_STRUCTURE` (`BUILDING` / `BUILDING_STRUCTURE_ASSEMBLY`) | primary_nonzero | structure RCN, 100% | fifteen proposed records |
| `TCRE_BUILDING_CONTENTS` | out_of_scope_deferred | contents | withheld (`NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT`) |

Whole-building grain is source-native (D-TCRE-05); no source prices a separate roof unit. Platform codes are
proposals (same as `flood_real_estate`).

## 3. Source-native hazard axis and local exposure bridge

Axis: peak 3-second gust at 10 m, open terrain, mph — what the Hazus functions are indexed to (TCRE-C001) and what
Hazard delivers (TCRE-C020). Terrain enters only by choosing the record (`hazus_terrain_class`, required, five
classes, no interpolation; D-TCRE-06). Range 50–250 mph; below 50 returns 0; above 250 withholds (D-TCRE-18).

## 4. Source register summary

[SOURCE_REGISTER](SOURCE_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv): Hazus 7.0 Hurricane TM
(method, T2), FEMA Hazus 6.1 extract via the OS-Climate mirror (ordinates, T2), SimCenter Hazus 5.1 copy
(independent verification, T2), physrisk documentation (provenance), the Hazard consumer, `flood_real_estate`,
doc 06, the legacy library (rejected), and the sibling hurricane cells.

## 5. Claim/parameter provenance map

[CLAIM_PARAMETER_REGISTER](CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
TCRE-C001–C024. Load-bearing: C001 (axis), C002 (mechanisms), C004 (denominator), C006–C008 (types), C010
(characteristics), C011 (ordinates verified), C005 (terrain).

## 6. Evidence and legacy numerical pressure test

[Pressure test](PRESSURE_TEST_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md): chain complete at
screening grade; terrain and the commercial type choice are the largest sensitivities; source anomalies (SPMB
superior deck, commercial terrain order) are contained. Legacy: two arrays rejected (TCRE-C023).

## 7. Y-axis and row-level value crosswalk

Y-axis: Hazus building loss ratio = repair cost / total building replacement cost (TCRE-C004).
[Value crosswalk](VALUE_CROSSWALK_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv): structure RCN 100%;
contents, tree fall, land, site works, loss of use excluded. Per-area cost open (shared with flood).

## 8. Site-condition adapter and double-counting matrix

[Seven-step audit](SEVEN_STEP_AUDIT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md) step 6: terrain once
(record choice, never also on the gust); topography only in the delivered gust; debris inside the record; tree fall
deferred; opening protection and roof upgrades only as published characteristic values; surge and rain flooding in
`flood_real_estate`, combined by the consumer at ≤ 100%.

## 9. Curve-form decision

[Curve form](CURVE_FORM_DECISION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md): straight lines between
the published 5-mph points; published values kept, including dips ≤ 0.2 points above 200 mph (D-TCRE-17).

## 10. Parameter derivation and tiers

[Parameter tiers](PARAMETER_TIER_TABLE_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv): ordinates and axis
T2; commercial and warehouse type T3 (story count, floor-area assumption); characteristics T4 assumptions drawn
from T2 frequencies; per-area value open.

## 11. Seven-step audit

All seven steps proposed; step 7 partial (dollars withheld). See the audit outcome table.

## 12. Derivation rationale / combination narrative

The curves are adopted, not derived. FEMA's Hazus hurricane model simulates each building type with each
combination of wind characteristics in many storms and tabulates mean building loss against open-terrain peak gust,
for five terrains. This cell picks, for each reference building, the Hazus type that matches it and the most common
value of every unknown characteristic (Table C-2), and takes the five terrain rows unchanged. The two independent
copies of the Hazus database agree exactly, so the numbers are the published model, not a transcription.

## 13. Capability and fail-closed decision

[Capability](tropical_cyclone_wind_real_estate__model_v0_1__docs_r1__capability.json): failure-unit DR conditional;
scenario loss withheld; spread not carried; annual and tail metrics consumer-owned; promotion gate blocked. The
reference evaluator withholds variants, unknown units and out-of-range gusts and errors on malformed requests
([metadata spec](tropical_cyclone_wind_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md)).

## 14. Open seams and update triggers

```text
owner review of scope and selections                       before any canonical use
per-area replacement cost new                              shared with flood_real_estate (D-TCRE-09)
Hazard terrain class per location + mapping rule           consumer (D-TCRE-06)
reference warehouse floor area (> 50,000 ft2 assumed)      ties Hazus size class and value (D-TCRE-16)
tree fall add-on for the house                             needs tree data (D-TCRE-13)
measure variants (shutters, straps, roof deck, SWR)        publish as additional records later (D-TCRE-19)
SPMB superior-deck anomaly                                 FEMA clarification (TCRE-C016)
wind + flood combination on one building                   consumer rule; needs storm identity (D-TCRE-11)
Hazard loader alignment (below-50 zero, variant withhold)  validation report §4
contents failure unit                                      Hazus contents functions available (TCRE-C021)
```

## 15. Validation/QC

[Validation report](VALIDATION_REPORT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md): validator, hand checks,
consumer-loader check, and what is not validated.
