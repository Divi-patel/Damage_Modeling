<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# wildfire_real_estate — wildfire × real estate, model v0.1 proposal

Scope, change classification and existing-coverage check (workflow steps 0–2) for a new cell. Decisions are in
the [decision log](DECISION_LOG_wildfire_real_estate__model_v0_1__docs_r1.md); the full derivation is in the
[dossier](wildfire_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md).

## Status

- **Noncanonical proposal**, model v0.1 / docs r1, lifecycle `scaffold`, promotion gate blocked.
- Not in the artifact index, the version registry or a package release; no Hazard pin changes.
- Branch `cell/wildfire-real-estate` (local commits only).

## 1. The modelling question

When a wildfire burns at a reference building's location, how much of the building's structure value is lost, as a
function of the fire's flame-length class (the severity Hazard delivers) — for the three Hazard reference buildings?

## 2. Scope

### In scope

- Pathway `wildfire_building_exposure`: a wildfire reaching the building location, with embers, radiant heat, flame
  contact and building-to-building spread as they are inside the source response and the inspected outcomes.
- Failure unit `WFRE_BUILDING_STRUCTURE`: the whole structure (shell, roof, openings, interior finishes, fixed
  services) as one unit; y-axis = repair cost / structure replacement cost new.

### Deferred / out of scope

- Contents (`WFRE_BUILDING_CONTENTS`, withheld, not zero); loss of use, business interruption, land, landscaping,
  site works, vehicles.
- Smoke, soot or ash contamination without fire damage; post-fire debris flow, flooding and erosion; power shutoff.
- Fire frequency (burn probability) and the class mix: Hazard owns them.

## 3. Reference buildings (selector `reference_building_id`)

| Selector | Hazard profile (r1) | Curve | Why |
|---|---|---|---|
| `RE_RES_SFD_1S_SLAB` | `re_house_1s_wood_slab` | USFS home response (shrub) | one-storey wood house, vinyl siding, asphalt shingles, vented attic without ember-resistant vents |
| `RE_IND_WAREHOUSE` | `re_warehouse_1s_steel_slab` | 0.8 × house | metal walls and roof; CAL FIRE same-fire ratio for metal commercial buildings 0.79 |
| `RE_COM_OFFICE_3S_SLAB` | `re_office_3s_slab` | 0.9 × house | masonry-veneer three-storey; CAL FIRE same-fire ratio for multi-storey masonry commercial buildings 0.93 |

## 4. Change classification

A **new cell** (no existing records changed). It adds a proposed cell folder and helper scripts only. It is not a
model release: no canonical artifact, no capability change in any released cell, no consumer pin, no package
inclusion. The axis, field name, product selector and error vocabulary follow `wildfire_wind` model v1.0.

## 5. Existing-coverage check

| Where | What exists | Use here |
|---|---|---|
| `wildfire_solar`, `wildfire_wind` (canonical) | Exact FSim class-state tables for solar and turbine equipment (T4 engineering proxies) | Axis and contract precedent only. No building curves. |
| Station wildfire binding (`docs/contracts/hazard_handoff/substation_wildfire_screening_v1/`) | Solar electrical-equipment response reused for station equipment | Not applicable to buildings. |
| Hazus | No wildfire module | — |
| Public sources | USFS Wildfire Risk to Communities publishes a structure response per FSim flame-length class (for a home); CAL FIRE publishes post-fire inspections by structure type and material | Adopted: the USFS response is the curve; CAL FIRE gives the building factors and a level check (D-WFRE-03, -07). |

## 6. Explicit non-changes

No released cell, schema, consumer adapter, artifact index or version registry is modified.
