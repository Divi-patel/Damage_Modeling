<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# convective_wind_real_estate — convective wind × real estate, model v0.1 proposal

Scope, change classification and existing-coverage check (workflow steps 0–2) for a new cell. Decisions are in
the [decision log](DECISION_LOG_convective_wind_real_estate__model_v0_1__docs_r1.md); the full derivation is in the
[dossier](convective_wind_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md).

## Status

- **Noncanonical proposal**, model v0.1 / docs r1, lifecycle `scaffold`, promotion gate blocked.
- Not in the artifact index, the version registry or a package release; no Hazard pin changes.
- Branch `cell/convective-wind-real-estate` (local commits only).

## 1. The modelling question

How much of a building's structure value does one convective wind event destroy, as a function of the 3-second gust
at the building — separately for a thunderstorm straight-line gust and for a direct tornado hit — for the three Hazard
reference buildings?

## 2. Scope

### In scope

- Pathway `straight_line_convective`: downburst, gust front and derecho outflow wind on the building.
- Pathway `tornado_direct_hit`: a tornado passing over the building, after Hazard resolves the hit.
- Failure unit `CWRE_BUILDING_STRUCTURE`: the whole structure (shell, roof, openings, interior finishes, fixed
  services) as one unit; y-axis = repair cost / structure replacement cost new.

### Deferred / out of scope

- Contents (`CWRE_BUILDING_CONTENTS`, withheld, not zero); loss of use, business interruption, land and site works.
- Tropical-cyclone wind (→ `tropical_cyclone_wind_real_estate`), hail (future hail × real estate cell), lightning,
  rainfall flooding (→ `flood_real_estate`).
- Tornado frequency, path probability and the straight-line event rate: Hazard owns them.

## 3. Reference buildings (selector `reference_building_id`)

| Selector | Hazard profile (r1) | EF damage indicator | Why |
|---|---|---|---|
| `RE_RES_SFD_1S_SLAB` | `re_house_1s_wood_slab` | FR12, one- and two-family residences (1,000–5,000 ft²) | one-storey 1,800 ft² wood-frame house |
| `RE_IND_WAREHOUSE` | `re_warehouse_1s_steel_slab` | MBS, metal building systems | one-storey pre-engineered steel warehouse, eight overhead doors |
| `RE_COM_OFFICE_3S_SLAB` | `re_office_3s_slab` | LRB, low-rise building 1–4 storeys | three-storey steel office, TPO roof |

## 4. Change classification

A **new cell** (no existing records changed). It adds a proposed cell folder and helper scripts only. It is not a
model release: no canonical artifact, no capability change in any released cell, no consumer pin, no package
inclusion. The repository's convective pathway IDs are reused unchanged.

## 5. Existing-coverage check

| Where | What exists | Use here |
|---|---|---|
| `strong_wind_solar`, `wind_tornado_wind` (canonical) | Straight-line and tornado curves for solar arrays and turbines | Method precedent only (onset below the design gust; separate pathways). No building curves. |
| Station convective binding (`docs/contracts/hazard_handoff/substation_convective_wind_screening_v1/`) | Hurricane station response reused for strong wind and tornado as a T4 cross-hazard proxy | Recorded as the documented alternative route (D-CWRE-03); not used. |
| `tropical_cyclone_wind_real_estate` (proposal, own branch) | Hazus hurricane building curves for the same buildings | The alternative evidence for the reuse route; not used. |
| Public sources | No published convective building loss function by building type was found; the EF scale publishes expert-elicited gusts per degree of damage by building type | Adopted as the evidence spine (D-CWRE-03, -04). |

## 6. Explicit non-changes

No released cell, schema, consumer adapter, artifact index or version registry is modified.
