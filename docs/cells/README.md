# docs/cells/

Shallow entrypoints for the current hazard x asset damage-curve cells.

These pages are the current cell entrypoints. Current packages, archives, previews, and runtime JSON artifacts
live under each cell folder.

| Cell | Model / human docs / runtime docs | Damage code | Entry point |
|---|---|---|---|
| `flood_substation` | model v1.0 / docs r1; depth-only screening | `FLOOD_SUBSTATION_DEPTH_SCREENING_V1` | [`flood_substation/`](flood_substation/README.md) |
| `hail_solar` | model v1.0 / human docs r8; runtime pin docs r7 | `HAIL_SOLAR_PV_MODULE_V1` | [`hail_solar/`](hail_solar/README.md) |
| `flood_solar` | model v1.0 / human docs r5; runtime pin docs r4 | `FLOOD_SOLAR_ELECTRICAL_INUNDATION_V1` | [`flood_solar/`](flood_solar/README.md) |
| `wind_tornado_wind` | model v1.0 / human docs r5; runtime pin docs r4 | `WIND_TORNADO_WIND_V1` | [`wind_tornado_wind/`](wind_tornado_wind/README.md) |
| `strong_wind_solar` | model v1.0 / human docs r4; runtime pin docs r3 | `STRONG_WIND_SOLAR_V1` | [`strong_wind_solar/`](strong_wind_solar/README.md) |
| `wildfire_solar` | model v1.0 / human docs r4; runtime pin docs r3; screening engineering proxy | `WILDFIRE_SOLAR_FSIM_SCREENING_V1` | [`wildfire_solar/`](wildfire_solar/README.md) |
| `flood_wind` | model v1.0 / docs r1; partial screening | `FLOOD_WIND_FEMA_HAZUS_SUBSTATION_SCREENING_V1` | [`flood_wind/`](flood_wind/README.md) |
| `wildfire_wind` | model v1.0 / docs r1; Tier-4 partial screening | `WILDFIRE_WIND_PARTIAL_ELECTRICAL_SCREENING_V1` | [`wildfire_wind/`](wildfire_wind/README.md) |
| `tropical_cyclone_wind_wind` | model v1.2 / docs r2; owner-approved tower-only screening | `TROPICAL_CYCLONE_WIND_WIND_JAIMES_TOWER_SCREENING_V1_2` | [`tropical_cyclone_wind_wind/`](tropical_cyclone_wind_wind/README.md) |

Active research proposal: `wind_tornado_wind` has a noncanonical
[`model v2.0 / docs r1` pathway-aware package](wind_tornado_wind/proposed/README_wind_tornado_wind__model_v2_0__docs_r1.md).
It does not change the current runtime pin, is absent from the artifact index, and excludes
hurricane/tropical-cyclone wind. Model v1.0/docs r4 remains the runtime pin; human docs r5 only add basics.

`strong_wind_solar` also has a noncanonical
[`model v2.0 / docs r1` convective-wind package](strong_wind_solar/proposed/README_strong_wind_solar__model_v2_0__docs_r1.md).
It separates fixed tilt from exact-system-qualified trackers, excludes hurricane/tornado/synoptic wind, and
leaves model v1.0/docs r3 as the canonical runtime pin; human docs r4 only add basics.

`tropical_cyclone_wind_wind` now has a canonical
[`model v1.1 / docs r1` owner-approved partial-screening release](tropical_cyclone_wind_wind/current/README.md).
It preserves the three source-native Jaimes selectors and adds one exact 3.3-MW-source → canonical-5-MW
screening route with no capacity scaling. Rotor+nacelle+tower bind to 63% of project TIV; the other 37% stays
withheld. Model v1.0 remains an exact offline reproduction archive, not a live GCS pin.

`flood_wind` now has a canonical
[`model v1.0 / docs r1` partial-screening release](flood_wind/current/README.md). It preserves the exact legacy FEMA
Hazus-MH 2.1 whole-substation depth-damage table for one mutually exclusive source-native GSU/substation
assembly atom. All component and wind-specific units remain withheld; current Hazus 7.0 disables electric-
power loss results. Same-unit scenario loss requires explicit substation value and exposure. The model-v0.1
zero-curve scaffold remains the component-level evidence audit.

`tropical_cyclone_wind_solar` now leads with a noncanonical
[`model v2.1 / docs r1` coverage-complete screening candidate](tropical_cyclone_wind_solar/proposed/README_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md). It preserves v2.0's Perry and four array records, adds five Tier-4 site-facility records, and reconciles a named 100%-physical-value profile into plant DR, loss per kWdc, and optional scenario dollars. The qualified fixed/tracker/site axes and attained-state controls remain; annual/tail metrics remain consumer-owned. Models v0.1, v1.0, and v2.0 remain preserved alternatives. The v2.1 candidate has no
artifact-index entry, `current/` package, changelog event, package release, or consumer cutover.

`hail_wind` is a new, noncanonical
[`model v0.1 / docs r2` research scaffold](hail_wind/README.md). It keeps source hail descriptors separate
from a future turbine-local contact-demand bridge, treats the blade assembly as the primary candidate without
pooling nacelle/BOP subjects, and rejects the mislabeled legacy real-estate curve. Independent deep curation
added seven sources and nine claims but found no source-native disposition/economic atom; the package
publishes zero runtime records and withholds every numeric output with `NO_RUNTIME_CURVE`.

`wildfire_wind` now has a canonical
[`model v1.0 / docs r1` Tier-4 partial-screening release](wildfire_wind/current/README.md). It publishes exact
FSim-class tables for `WT_PAD_ELECTRICAL` and `WT_GSU_PROTECTION_CONTROL_DC` only. Every other unit remains
withheld, source/assumption acknowledgement is mandatory, and whole-farm or annual defaults are prohibited.
The model-v0.1 zero-curve scaffold remains the strict evidence-earned alternative and audit history.

Five Real Estate cells arrive from Jung A Lim's `cell/real-estate` branch (merged 2026-10-19) as
noncanonical draft proposals bound to the Hazard reference profiles r1 (one-storey house, one-storey warehouse,
three-storey office): [`flood_real_estate`](flood_real_estate/README.md) and
[`tropical_cyclone_wind_real_estate`](tropical_cyclone_wind_real_estate/README.md) at `model v0.2 / docs r1`
(v0.1 kept beside each), and [`convective_wind_real_estate`](convective_wind_real_estate/README.md),
[`hail_real_estate`](hail_real_estate/README.md) and [`wildfire_real_estate`](wildfire_real_estate/README.md)
at `model v0.1 / docs r1`. None is in the artifact index or has a current/runtime release. The earlier
flood v0.1 intake and office source check are recorded in
[intake and next work](../extra/discussion/real_estate_conus/03_junga_research_intake_and_next_work.md).

## Portable-package boundary

`wildfire_solar`, `flood_wind`, `wildfire_wind`, and `tropical_cyclone_wind_wind` are repository-current and canonical but are not included
in preserved portable package v2.5. Their proposal/scaffold packages remain as research and rejection audits.

Authoritative package registry:
[`VERSION_REGISTRY.md`](VERSION_REGISTRY.md).

Runtime artifact index:
[`MACHINE_READABLE_ARTIFACTS.md`](../contracts/MACHINE_READABLE_ARTIFACTS.md).

## Cell basics layer

Each hazard × asset cell owns a three-page reader layer under:

```text
docs/cells/<cell_id>/basics/
├── README.md                  understand the physical idea and terminology
├── HOW_THE_MODEL_IS_BUILT.md  follow evidence through SHIP
└── MODEL_REFERENCE.md         look up exact curves, fields, tests, and sources
```

This avoids a duplicate parallel basics hierarchy and keeps cell-specific terminology, physical/spatial
references, ASCII diagrams, worked examples, exact tables, and caveats with the cell that owns them.

| Cell | Basics status |
|---|---|
| `flood_solar` | [Complete](flood_solar/basics/README.md) — first reference implementation |
| `hail_solar` | [Complete](hail_solar/basics/README.md) |
| `wind_tornado_wind` | [Complete](wind_tornado_wind/basics/README.md) |
| `strong_wind_solar` | [Complete](strong_wind_solar/basics/README.md) |
| `wildfire_solar` | [Complete](wildfire_solar/basics/README.md) |
| `tropical_cyclone_wind_wind` | [Complete for current model v1.1](tropical_cyclone_wind_wind/basics/README.md) — canonical-Wind-Farm partial-screening proxy; 63% covered value |
| `flood_wind` | [Complete for current model v1.0](flood_wind/basics/README.md) — legacy source-native whole-substation partial-screening release |
| `tropical_cyclone_wind_solar` | [Complete for proposed model v2.1/docs r1](tropical_cyclone_wind_solar/basics/README.md) — ten records plus complete named-value plant physical-damage assembly; noncanonical and no-cutover |
| `hail_wind` | [Complete for model v0.1/docs r2](hail_wind/basics/README.md) — independently deep-curated, fail-closed turbine/blade and BOP research scaffold |
| `wildfire_wind` | [Complete for current model v1.0/docs r1](wildfire_wind/basics/README.md) — two-unit Tier-4 electrical partial-screening release; v0.1 strict alternative preserved |

Reusable authoring templates:

- [`README`](../method/templates/TEMPLATE_cell_basics_README.md)
- [`HOW_THE_MODEL_IS_BUILT`](../method/templates/TEMPLATE_cell_basics_HOW_THE_MODEL_IS_BUILT.md)
- [`MODEL_REFERENCE`](../method/templates/TEMPLATE_cell_basics_MODEL_REFERENCE.md)

The basics set is the source manuscript for later reader-facing publication. A Google Drive document, DOCX,
presentation, or review note should be generated or curated as a subset; it is not a fourth technical source
of truth.
