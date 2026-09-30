# Damage-code metadata spec — tropical-cyclone wind × solar model v2.1

## Exact identity

```yaml
cell_id: tropical_cyclone_wind_solar
model_version: model v2.1
documentation_revision: docs r1
artifact_schema: damage_curve_record_bundle.v3
failure_unit_emit_schema: damage_emit.v2
plant_assembly_schema: physical_damage_assembly.v1
pathway_id: tropical_cyclone_wind
```

Every CLI call must supply the exact cell/model/docs/schema/SHA pin.

## Component mode

Supply exactly one `failure_unit_id`.

- Array units require the fixed or tracker architecture payload defined by v2.0.
- Foundation, power/collection, GSU, SCADA, and civil units require
  `tc_site_event_to_design_wind_pressure_ratio` or the complete 10 m gust/design-gust proxy plus
  `site_facility_demand_bridge_id`.
- Replacement support has no intrinsic DR and is available only in full-plant assembly.

## Full-plant screening mode

Required additions:

```yaml
output_mode: full_plant_screening
value_profile_id: NLR_Q1_2025_UPV_PV_ONLY_2024_USD_PHYSICAL_V1
array_exposure_basis: representative_site_array_zone
site_facility_demand_bridge_id: <non-empty>
tc_site_event_to_design_wind_pressure_ratio: <0..2>
capacity_kwdc: <optional positive number>
```

The output wrapper contains a schema-valid `damage_emit.v2` with seven numeric direct/civil failure units and
a `physical_damage_assembly.v1` with central/lower/upper plant DR and loss.

## Status semantics

`conditional` means a numeric screening proxy is emitted when the named input gates pass. It does not mean
the output is withheld. Calibration grade is carried through limitation flags.

Annual and tail metrics remain downstream-consumer objects because this cell has no hazard-frequency or
annual aggregation object.

