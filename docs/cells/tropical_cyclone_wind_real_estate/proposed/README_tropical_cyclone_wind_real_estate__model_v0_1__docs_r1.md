<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
scope: Step 0/1 cell definition for tropical-cyclone (hurricane) wind × real estate — modelling question, boundary, reference buildings, pathway, axis, failure-unit coverage, value link, and capability stance for the model v0.1 scaffold.
-->

# tropical_cyclone_wind_real_estate — hurricane wind × real estate, model v0.1 scaffold

> **Status: proposed, not yet reviewed, noncanonical, zero runtime curves.** No current Damage Modeling or
> Hazard Modeling runtime pin changes.

## Status

```yaml
cell_id: tropical_cyclone_wind_real_estate
lifecycle_state: scaffold   # draft needs owner scope acceptance (CELL_LIFECYCLE gate)
semantic_damage_model_version: model v0.1
released_model_version: null
promotion_status: proposed
review_status: not_yet_reviewed
documentation_revision: docs r1
documentation_status: working_revision
canonical_runtime_artifact: false
package_release: unreleased
package_baseline: library v2.5
package_inclusion_status: not_included
curve_records: 0
runtime_reason: NO_RUNTIME_CURVE
```

## 1. The modelling question

> For a tropical cyclone whose peak 3-second gust at the building's location (10 m height, open terrain) is
> known, what fraction of the building's **structure replacement cost new** is physically damaged by the wind?

The request comes from the real-estate CONUS screening grid (Hazard plan doc 06, 2026-10-08, proposed by the
reviewer and shared with JL), which orders the perils flood → **hurricane wind** → hail → convective wind →
wildfire. The grid prices one **reference building per asset type**, not observed buildings. OSM only decides
which reference building a searched building is matched to, so every construction attribute below is an
explicit assumption of the reference building, never an observation.

## 2. Scope

### In scope

```text
- direct physical damage to the building STRUCTURE (shell, roof, openings, interior finishes, fixed services)
  caused by tropical-cyclone wind;
- the damage the source library attributes to the wind event as a whole, which (to be verified in step 3)
  includes wind pressure on the roof and walls, windborne-debris (missile) impact on openings, and rain
  entering through a wind-breached envelope (§4);
- one source-native whole-building curve per reference building;
- damage ratio = repair cost / structure replacement cost new.
```

### Deferred / out of scope

```text
- storm surge and wave action — owned by flood_real_estate (coastal water type); Hazard routes surge to
  Flood Coastal;
- tropical-cyclone rainfall flooding (water rising from the ground) — owned by flood_real_estate; Hazard
  routes it to Flood Pluvial / Riverine;
- tornadoes spawned by the tropical cyclone — a future convective-wind × real-estate cell;
- tree fall onto the building as a separately valued mechanism (unless embedded in the source curve);
- contents and inventory, loss of use / additional living expense, business interruption, rent;
- land, site works, non-building structures, signage, rooftop equipment as separate units;
- financial and insurance terms;
- building types outside the three reference buildings, including manufactured homes (doc 06 §3:
  "need their own wind curves");
- annual and tail metrics (EAL, PML, VaR, TVaR) — consumer-owned, as for every cell.
```

## 3. Reference buildings (selector)

Identical IDs and attributes to [`flood_real_estate`](https://github.com/aamani-ai/Damage_Modeling/tree/cell/flood-real-estate/docs/cells/flood_real_estate),
so the two cells line up on the same building.

| `reference_building_id` | Asset type | Reference building (assumed attributes) | Candidate Hazus hurricane building type (doc 06 §5; to verify in step 3) |
|---|---|---|---|
| `RE_RES_SFD_1S_SLAB` | Residential | Single-family detached; 1 story; wood frame; slab; no basement; asphalt-shingle roof; no opening protection | `WSF1` (wood single-family, one story) |
| `RE_COM_LOWRISE` | Commercial | Small low-rise (1–3 story) retail or office; masonry or steel frame; low-slope membrane roof; no opening protection | `MLRM1` (masonry low-rise strip mall) **or** `SECBL` (steel engineered commercial, low-rise); `MECBL` (masonry engineered commercial, low-rise) is a further candidate |
| `RE_IND_WAREHOUSE` | Industrial | One-story pre-engineered steel warehouse; large low-slope roof (membrane or metal); no opening protection | `SPMBL` (steel pre-engineered metal building, large); `SPMBM` and `MLRI` (masonry low-rise industrial / warehouse) are further candidates |

These are **candidates**, not decisions. Step 3 verifies each type's definition against the Hazus Hurricane
Technical Manual and the FEMA function extract; step 4 proposes a selection.

**Wind building characteristics.** Hazus hurricane functions are not one curve per building type. Each type is
split by wind building characteristics such as roof shape, roof cover, secondary water resistance, roof-deck
attachment, roof-to-wall connection, opening protection (shutters), garage door, and terrain (to be confirmed
per type in step 3). The reference building fixes the ones we know (roof cover, no shutters); the others must be
either fixed as stated assumptions or taken as Hazus's default mix — an owner decision (D-TCRE-07). Because
these attributes are explicit in the source, a future resiliency measure (shutters, roof straps, a better roof
deck or roof cover) becomes a change of one selector value on the same curve family — the doc 06 §8 ask.

## 4. Pathway and hazard axis

```yaml
- pathway_id: tropical_cyclone_wind
  physical_mechanism: >
    tropical-cyclone wind loads the roof cover, roof deck, roof-to-wall connections, walls and openings;
    windborne debris breaks unprotected openings; once the envelope is breached, wind pressure rises inside
    and rain enters, damaging interior finishes and services. The source library (Hazus) simulates these
    together and publishes one building loss ratio per wind speed.
  source_native_axis: peak 3-second gust at 10 m in open terrain (to verify in step 3: Hazus TM §4.4.7
    states damage and loss functions are given as a function of peak gust, not one-minute sustained wind)
  axis_id: TC_PEAK_GUST_3S_10M_OPEN_TERRAIN_MPH
  input_field: tc_peak_gust_3s_10m_mph
  unit: mph
  height_duration_datum_basis: 3-second gust, 10 m above ground, open terrain (Exposure C, z0 ≈ 0.03 m)
  bridge: none inside Damage. Hazard converts STORM 10-minute sustained wind to the 3-second gust
    (U3s = U10min × 1/0.88 × 1.20); Damage does not repeat or undo it.
  hazard_delivered_range: about 61–229 mph (STORM thresholds 20–75 m/s; Hazard origin/main @ e8664800)
  valid_range: the published range of the selected curves (Hazus extract tabulated about 50–250 mph, to
    verify); outside it withholds (no clamp, no extrapolation)
  neighboring_cell_boundaries:
    - flood_real_estate (storm surge, wave, rainfall flooding)
    - future convective_wind × real estate (TC-spawned tornado, straight-line thunderstorm wind)
    - future hail × real estate (roof cover impact)
```

**One pathway, with debris and rain ingress inside it — a deliberate difference from the sibling cells.**
`tropical_cyclone_wind_solar` and `tropical_cyclone_wind_wind` exclude windborne debris and wind-driven rain,
because their source curves model wind loading only. For a building, the source curves (Hazus) are built from a
simulation in which debris impact and rain ingress are part of the same wind event and cannot be separated in
the published loss ratio (to verify in step 3). Splitting them into pathways would need component-level output
that the source does not publish. The guardrail is the reverse one: **no separate debris or rain-ingress pathway
may be added to this cell while its records are Hazus-based**, or the same damage would be counted twice
(D-TCRE-04).

**Terrain is not on the axis.** Hazard delivers an open-terrain gust with no roughness adjustment. Hazus
functions differ by surface roughness (open, suburban, wooded…), which changes both the local wind and the
amount of debris. How this cell handles terrain is an open owner decision (D-TCRE-06); it must never be applied
twice (once in Hazard, once in Damage).

## 5. Failure-unit coverage

| pathway_id | Failure unit (proposed) | Subsystem (proposed) | Component (proposed) | Role | Value bucket | v0.1 treatment |
|---|---|---|---|---|---|---|
| `tropical_cyclone_wind` | `TCRE_BUILDING_STRUCTURE` | `BUILDING` | `BUILDING_STRUCTURE_ASSEMBLY` (source-native whole building) | primary_nonzero | Structure replacement cost new, 100% | Candidate; no curve record yet |
| — | `TCRE_BUILDING_CONTENTS` | `BUILDING` | `CONTENTS` | out_of_scope_deferred | Contents value | Deferred (Hazus publishes contents functions) |
| — | `TCRE_LOSS_OF_USE` | — | — | out_of_scope_deferred | not physical value | Deferred; disruption stage |

- **Grain.** One whole-building record per reference building. Doc 06 asks to split the roof out for wind
  "where the sources support it". The Hazus loss function is whole-building; its roof-related attributes enter as
  selectors, not as a separate roof failure unit. Whether any source supports a separate roof unit is checked in
  step 3 (D-TCRE-05).
- **Subsystem and component codes** are the same proposals as `flood_real_estate` (no platform building
  vocabulary yet; standard 24 exact join). The failure-unit IDs are cell-scoped (`TCRE_…`), so the two cells'
  losses on the same building are added, not merged.

## 6. Value link

```text
loss = DR(TCRE_BUILDING_STRUCTURE | reference building, wind characteristics, terrain, gust) × structure replacement cost new
```

- **Denominator:** replacement cost new of the structure, as in `flood_real_estate` (Hazus expresses building
  loss as a fraction of building replacement value — to verify). Excludes land, contents and depreciation.
- **Per-area cost:** shared open seam with `flood_real_estate`; scenario dollars stay withheld until JL selects a
  source.
- **Same building, several perils.** Wind and flood losses on the same building are computed by separate cells.
  Combining them for one storm (so a building is not repaired more than 100%) is a consumer rule, recorded in the
  scope but not solved here; Hazard's return-period rasters carry no storm identity today.

## 7. Capability declaration summary (scaffold)

```text
failure-unit DR:  withheld — NO_RUNTIME_CURVE
scenario loss:    withheld — NO_RUNTIME_CURVE (and value basis open)
scalar EAL:       withheld — consumer-owned; no runtime curve
PML/VaR/TVaR:     withheld — no runtime curve
```

## 8. Explicit non-changes

```yaml
artifact_index: unchanged
portable_package: unchanged
existing_cells: unchanged   # including flood_real_estate and both tropical_cyclone_wind cells
contracts_schemas: unchanged
version_registry: unchanged
Hazard_runtime: unchanged
numeric_damage_emit: not_created
model_v1_0: not_released
```
