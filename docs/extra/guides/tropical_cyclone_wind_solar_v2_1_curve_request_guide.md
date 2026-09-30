# Guide: requesting the usable tropical-cyclone wind × solar v2.1 curve

> V2.1 is the canonical coverage-complete screening release. It emits numeric plant physical DR and event
> scenario loss; it is not calibrated, claims-validated or bankable.

Canonical consumer pin: `tropical_cyclone_wind_solar@model_v2_1__docs_r2`.

## Exact pin

```json
{
  "cell_id": "tropical_cyclone_wind_solar",
  "semantic_damage_model_version": "model v2.1",
  "documentation_revision": "docs r2",
  "schema_version": "damage_curve_record_bundle.v3",
  "artifact_sha256": "2fbc34fbf8f91df408fe1b3c8d01d260d013119cbcba594b6a9a60044cd2113e"
}
```

## Full fixed-tilt screening request

Run from the repository root:

```bash
.venv/bin/python \
  scripts/reference_helpers/tropical_cyclone_wind_solar_v2_1_curve_eval.py \
  docs/cells/tropical_cyclone_wind_solar/current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__curve_artifact.json \
  '{"artifact_pin":{"cell_id":"tropical_cyclone_wind_solar","semantic_damage_model_version":"model v2.1","documentation_revision":"docs r2","schema_version":"damage_curve_record_bundle.v3","artifact_sha256":"2fbc34fbf8f91df408fe1b3c8d01d260d013119cbcba594b6a9a60044cd2113e"},"event_id":"TC-USE-1","event_family_id":"TC-FAMILY-USE-1","pathway_id":"tropical_cyclone_wind","array_architecture":"fixed_tilt_ground_mount_tc_synthetic_t4_v1","tc_fixed_event_to_design_net_pressure_ratio":1.0,"tc_wind_field_bridge_id":"TCWF-BRIDGE-V1","tc_directional_history_bridge_id":"TCDIR-BRIDGE-V1","tc_duration_cycling_bridge_id":"TCDUR-BRIDGE-V1","aerodynamic_demand_bridge_id":"TCFIXED-PRESSURE-BRIDGE-V1","array_zone":"edge","array_spatial_object_id":"FIXED-ARRAY-ZONE-EDGE-A","tc_duration_class":"sustained_1_to_6h","tc_direction_evolution_class":"evolving","rain_ingress_indicator":false,"windborne_debris_indicator":false,"flood_or_surge_indicator":false,"tc_tornado_indicator":false,"output_mode":"full_plant_screening","tc_site_event_to_design_wind_pressure_ratio":1.0,"site_facility_demand_bridge_id":"TC-SITE-FACILITY-BRIDGE-V1","array_exposure_basis":"representative_site_array_zone","value_profile_id":"NLR_Q1_2025_UPV_PV_ONLY_2024_USD_PHYSICAL_V1","capacity_kwdc":100000.0}'
```

At both demand ratios equal to 1.0, the central output is:

```text
physical_replacement_dr                 0.1441695907
physical_loss_2024_usd_per_kwdc       126.5514471
installed_capex_physical_loss_fraction 0.1129923635
scenario_physical_loss_2024_usd        12,655,144.71  (100 MWdc)
```

The lower-resistance/higher-damage scenario is 0.3335660993 DR; the upper-resistance/lower-damage scenario
is 0.0562454851 DR.

## Full tracker screening request

Use the exact attained-state tracker payload in the
[v2 route guide](tropical_cyclone_wind_solar_v2_curve_request_guide.md#exact-tracker-request), then add the
same five full-plant fields used above:

```yaml
output_mode: full_plant_screening
tc_site_event_to_design_wind_pressure_ratio: <0..2>
site_facility_demand_bridge_id: <non-empty>
array_exposure_basis: representative_site_array_zone
value_profile_id: NLR_Q1_2025_UPV_PV_ONLY_2024_USD_PHYSICAL_V1
```

Commanded stow is still insufficient. The attained tracker state and exact qualification identity must pass
before the array and plant outputs are returned.

For the site-facility axis, a caller may replace the direct pressure ratio with both
`tc_peak_gust_3s_10m_mps` and `qualified_site_design_3s_gust_mps`; the helper then evaluates their squared
speed ratio. Partial or mixed axis payloads reject.

## Direct GSU request

GSU is evaluated on the site-facility axis, without inheriting the array axis or architecture:

```json
{
  "artifact_pin": {
    "cell_id": "tropical_cyclone_wind_solar",
    "semantic_damage_model_version": "model v2.1",
    "documentation_revision": "docs r2",
    "schema_version": "damage_curve_record_bundle.v3",
    "artifact_sha256": "2fbc34fbf8f91df408fe1b3c8d01d260d013119cbcba594b6a9a60044cd2113e"
  },
  "event_id": "TC-GSU-1",
  "event_family_id": "TC-FAMILY-GSU-1",
  "pathway_id": "tropical_cyclone_wind",
  "failure_unit_id": "PV_GSU_SUBSTATION",
  "tc_site_event_to_design_wind_pressure_ratio": 1.0,
  "site_facility_demand_bridge_id": "TC-SITE-FACILITY-BRIDGE-V1",
  "tc_duration_class": "sustained_1_to_6h",
  "tc_direction_evolution_class": "evolving",
  "rain_ingress_indicator": false,
  "windborne_debris_indicator": false,
  "flood_or_surge_indicator": false,
  "tc_tornado_indicator": false
}
```

This returns numeric lower/central/upper same-GSU DRs. It is a wind-only Tier-4 proxy, not a flood/surge or
array-inherited response.

## What the result contains

`damage_emit` contains seven numeric direct/civil failure-unit results for the selected architecture.
`physical_damage_assembly` contains:

- all unit losses on the named 2024 USD/kWdc profile;
- replacement support allocated once;
- complete physical replacement DR;
- installed-capex physical loss fraction;
- scenario dollars when `capacity_kwdc` is present.

Frequency, EAL, and tail metrics remain Hazard-tier calculations. Their absence here does not make the curve
partial: they require an event-frequency/annual aggregation object that this repository intentionally does not
own.

The capability-v3 field `consumer_annual_metrics.status_before_promotion=withheld_noncanonical_proposal` is
historical transition metadata. The adjacent `status_after_promotion` governs this current release. Neither
field delegates EAL/PML physics to Damage: those metrics remain consumer-computable only after Hazard's exact
frequency, coupling, value and cap gates pass.

## Machine files

- [artifact](../../cells/tropical_cyclone_wind_solar/current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__curve_artifact.json)
- [capability](../../cells/tropical_cyclone_wind_solar/current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__capability.json)
- [metadata contract](../../cells/tropical_cyclone_wind_solar/current/tropical_cyclone_wind_solar_damage_code_metadata_spec__model_v2_1__docs_r2.md)
- [known-answer tests](../../cells/tropical_cyclone_wind_solar/current/known_answer_tests_tropical_cyclone_wind_solar__model_v2_1__docs_r2.json)
- [full-plant curve table](../../cells/tropical_cyclone_wind_solar/current/FULL_PLANT_SCREENING_CURVE_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r2.csv)
- [reference evaluator](../../../scripts/reference_helpers/tropical_cyclone_wind_solar_v2_1_curve_eval.py)
- [release validator](../../../scripts/reference_helpers/validate_tropical_cyclone_wind_solar_v2_1_release.py)
