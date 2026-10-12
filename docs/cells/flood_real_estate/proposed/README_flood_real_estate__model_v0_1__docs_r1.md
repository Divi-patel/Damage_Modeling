<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
scope: Step 0/1 cell definition for flood × real estate — modelling question, boundary, reference buildings, pathways, axis, failure-unit coverage, value link, and capability stance for the model v0.1 scaffold.
-->

# flood_real_estate — flood × real estate, model v0.1 scaffold

> **Status: proposed, not yet reviewed, noncanonical, zero runtime curves.** No current Damage Modeling or
> Hazard Modeling runtime pin changes.

## Status

```yaml
cell_id: flood_real_estate
lifecycle_state: scaffold   # draft needs owner scope acceptance + capability declaration (CELL_LIFECYCLE gate)
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
curve_records: 0   # six proposed records are documented (step 5); none is in a runtime artifact yet
runtime_reason: NO_RUNTIME_CURVE
```

## 1. The modelling question

> For a flood event that puts water at a known depth relative to a building's first floor, what fraction of
> that building's **structure replacement cost new** is physically damaged?

The request comes from the real-estate CONUS screening grid (Hazard plan doc 06, 2026-10-08, proposed by the reviewer
and shared with JL). The grid prices one **reference building per asset type**, not observed buildings. OSM only
decides which reference building a searched building is matched to, so every construction attribute below is
an explicit assumption of the reference building, never an observation.

## 2. Scope

### In scope

```text
- direct physical damage to the building STRUCTURE (shell, interior finishes, fixed building services);
- one whole-building curve per reference building (source-native grain of Hazus / NACCS);
- still-water inundation from riverine, pluvial, and coastal-surge flooding;
- damage ratio = repair cost / structure replacement cost new.
```

### Deferred / out of scope

```text
- contents and inventory (Hazus publishes matching contents curves; a later failure unit, not v0.1);
- wave action and high-velocity flow, including scour (a separate pathway; see §4);
- long-duration, contamination, and mould effects beyond what the source curves already embed;
- business interruption, downtime, loss of use, rent;
- land, site works, and non-building structures;
- financial and insurance terms;
- building types outside the three reference buildings (institutional, agricultural, accessory,
  manufactured homes, parking, tanks) — doc 06 §3 marks them "not supported yet";
- annual and tail metrics (EAL, PML, VaR, TVaR) — consumer-owned, as for every cell.
```

## 3. Reference buildings (selector)

The asset is **real estate**, with three asset types. Each type has one reference building for the first grid
run (doc 06 §5, confirmed by the reviewer 2026-10-05 Slack reply). The reference building is a **fixed-identity
selector** on the single failure unit, in the same way module archetypes select records in `hail_solar`.

| `reference_building_id` (proposed) | Asset type | Reference building (assumed attributes) | Hazus occupancy | Candidate freshwater curve (Hazus default, Table 5-2) | Candidate coastal-surge curve (NACCS 2015) |
|---|---|---|---|---|---|
| `RE_RES_SFD_1S_SLAB` | Residential | Single-family detached; wood frame; 1 story; slab-on-grade; no basement; asphalt-shingle roof | RES1 | DF 129 — USACE-IWR "one story, no basement, Structure" | `RES1-1SNB` (Min / ML / Max) |
| `RE_COM_LOWRISE` | Commercial | Small low-rise (1–3 story) retail or office; masonry or steel frame; low-slope membrane roof; no basement | COM1 / COM4 | DF 217 — Galveston "Average of 47 Retail classes" **or** DF 431 — Galveston "Average prof/tech services" | `COM-ENG` (NACCS Prototype 2, steel frame); `COM-PRE` if the building is defined as masonry |
| `RE_IND_WAREHOUSE` | Industrial | One-story warehouse / light industrial; pre-engineered steel frame; large low-slope roof | IND2 / COM2 | DF 559 — Galveston "Average of 14 Light Industrial classes" **or** DF 341 — Galveston "Average of 22 wholesale/warehouse classes" | `COM-PRE` (NACCS Prototype 3, one-story steel or light metal) |

**Step 4 proposed selections** ([pressure test](PRESSURE_TEST_flood_real_estate__model_v0_1__docs_r1.md)):
house DF 129 / NACCS `RES1-1SNB`; commercial **DF 217** (retail) / NACCS `COM-ENG`; warehouse **DF 341**
(wholesale/warehouse) / NACCS `COM-PRE`. DF 431 (office) and DF 559 (light industrial) become later profiles.
All are proposed, pending owner review (D-FRE-16 to D-FRE-19).
Step 3 verified the candidate ordinates against originals or independent copies and moved the commercial coastal
candidate from `COM-PRE` to `COM-ENG`; see the
[source verification](SOURCE_VERIFICATION_flood_real_estate__model_v0_1__docs_r1.md). First-floor heights are the
NSI 2026 defaults (house 0.75 ft, commercial 0.25 ft, warehouse 0.25 ft; D-FRE-22), replacing the NACCS prototype
heights proposed in step 3. Full attribute table:
[reference buildings](REFERENCE_BUILDINGS_flood_real_estate__model_v0_1__docs_r1.md).

The platform type labels (Hotel → Commercial, Warehouse → Industrial; doc 06 check 4) do not change the curve.
The curve keys on the Hazus occupancy recorded above.

## 4. Pathways and hazard axis

```yaml
- pathway_id: flood_inundation_contact
  physical_mechanism: still floodwater inside the building damages structure, finishes and fixed services
  axis_id: depth_above_first_finished_floor
  input_field: flood_depth_above_first_floor_ft
  unit: ft
  bridge: >
    depth_above_first_floor_ft = depth_above_grade_ft − first_floor_height_ft
    (or water_surface_elevation − first_floor_elevation, same vertical datum required; mismatched or missing
    datums reject, as in flood_wind)
  valid_range: the published table range of the selected curve; outside it withholds (no clamp, no
    extrapolation) — exact range per curve fixed in step 5
  neighboring_cell_boundaries:
    - future wave / velocity pathway (deferred)
    - future contents failure unit (deferred)
    - future tropical_cyclone_wind / hail / convective wind / wildfire × real-estate cells

- pathway_id: flood_wave_velocity      # declared, not built
  physical_mechanism: wave impact and fast-moving water (structural lateral load, scour, undermining)
  status: deferred_out_of_scope
  reason: different mechanism and axis; mirrors the flood_solar scour proxy and flood_wind D-FW-07
```

**Flood source is not a pathway.** Riverine, pluvial, and coastal water share the inundation mechanism. The
existing flood cells follow the same rule: `flood_solar` and `flood_wind` do not split by flood source.

**Water type is an event-time conditioner**, because the two source libraries were built for different water:

```yaml
conditioner: flood_water_type
values:
  freshwater_riverine_or_pluvial: Hazus default curve (Table 5-2)
  coastal_surge_saline: NACCS 2015 curve
  unknown: withhold (no fallback to either library), as in flood_wind
```

## 5. Failure-unit coverage

| pathway_id | Failure unit (proposed) | Subsystem (proposed) | Component (proposed) | Role | Value bucket | treatment/support |
|---|---|---|---|---|---|---|
| `flood_inundation_contact` | `FRE_BUILDING_STRUCTURE` | `BUILDING` | `BUILDING_STRUCTURE_ASSEMBLY` (source-native whole building) | primary_nonzero | Structure replacement cost new, 100% | Candidate; no curve record yet |
| — | `FRE_BUILDING_CONTENTS` | `BUILDING` | `CONTENTS` | out_of_scope_deferred | Contents value | Deferred; not in v0.1 |
| `flood_wave_velocity` | (same structure unit) | `BUILDING` | — | out_of_scope_deferred | — | Deferred pathway |

- **Grain.** One whole-building record per reference building. Doc 06 accepts this as a deliberate v1
  exception, because the sourced flood curves are whole-building. The roof is split out later for hail and wind,
  where the roof is the failure unit. Precedent: `flood_wind` releases a source-native whole-substation Hazus atom
  (`FW_HAZUS_GSU_SUBSTATION_ASSEMBLY`).
- **Subsystem and component codes are proposals.** The platform engineering vocabulary has no building
  subsystem today (solar, wind, BESS and thermal only). Standard 24 requires an exact code join, so these names
  wait for platform codes. Owner: platform / reviewer.

## 6. Value link

```text
loss = DR(FRE_BUILDING_STRUCTURE | reference building, water type, depth) × structure replacement cost new
```

- **Denominator:** replacement cost new of the structure. Excludes land, contents and depreciation, and is not
  market or assessed value. This matches how Hazus and NACCS express damage (% of structure replacement value).
- **Coverage:** the single failure unit covers 100% of structure replacement cost new. No sub-allocation is
  needed at whole-building grain.
- **Open:** the $/m² (or $/ft²) source for each reference building, whose definition must match the denominator
  above. Candidates include USACE NSI `fullrep` (method) and Hazus default replacement costs. Until it is
  resolved, scenario dollars stay withheld.

## 7. Capability declaration summary (scaffold)

```text
failure-unit DR:  withheld — NO_RUNTIME_CURVE
scenario loss:    withheld — NO_RUNTIME_CURVE (and value basis open)
scalar EAL:       withheld — consumer-owned; no runtime curve
PML/VaR/TVaR:     withheld — no runtime curve; NACCS Min/Max is a source band, not a probabilistic spread
```

## 8. Evidence-governance summary

```text
seven-step audit:                 draft (step 6) — steps 1–6 proposed, step 7 partial
source register:                  draft (steps 3–6) — FRE-S001..S011; S006 pending
claim/parameter register:         draft (steps 3–6) — FRE-C001..C025
parameter-tier table:             draft (steps 4–5) — 20 parameters, two open seams
legacy numerical audit:           legacy Real Estate_Hail array noted as rejected (coverage note); no flood legacy array found
site-condition adapter:           draft (step 6, in the seven-step audit) — first-floor height, no protection credit
row-level value crosswalk:        draft (step 6) — structure RCN 100%; exclusions named; per-area cost open
pressure test:                    draft (step 4) — three proposed selections, fresh vs coastal gap recorded
curve records and form:           draft (step 5) — six records, straight lines between published points, 177 ordinates
known-answer tests:               not started (step 7)
```

## 9. Explicit non-changes

```yaml
artifact_index: unchanged
portable_package: unchanged
existing_cells: unchanged
contracts_schemas: unchanged
version_registry: unchanged
Hazard_runtime: unchanged
numeric_damage_emit: not_created
model_v1_0: not_released
```
