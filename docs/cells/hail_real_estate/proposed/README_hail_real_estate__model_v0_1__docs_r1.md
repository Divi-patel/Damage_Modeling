<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# hail_real_estate — hail × real estate, model v0.1 proposal

Scope, change classification and existing-coverage check (workflow steps 0–2) for a new cell. Decisions are in
the [decision log](DECISION_LOG_hail_real_estate__model_v0_1__docs_r1.md); the full derivation is in the
[dossier](hail_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md).

## Status

- **Noncanonical proposal**, model v0.1 / docs r1, lifecycle `scaffold`, promotion gate blocked.
- Not in the artifact index, the version registry or a package release; no Hazard pin changes.
- Branch `cell/hail-real-estate` (local commits only).

## 1. The modelling question

For one hailstorm, how much of each building part's value has to be replaced, given the largest hailstone at the
building? The answer is given separately for the roof cover and for the walls and windows of the three Hazard
reference buildings. Each part also carries its share of the building's structure value.

## 2. Scope

### In scope

- Pathway `hail_impact`: hailstones striking the building.
- Failure unit `HRE_ROOF_COVER`: the roof cover, replaced whole when hail punctures, fractures or ruptures it or opens
  seams. This is the house's shingles, the warehouse's standing-seam steel panels, and the office's TPO membrane with
  its insulation.
- Failure unit `HRE_WALLS_AND_WINDOWS` (Tier-4 screening): house vinyl siding and windows, and the warehouse and
  office windows. Hazard gets these numbers only with the screening acknowledgement.

### Withheld, not zero

- `HRE_EXPOSED_EQUIPMENT`: the house's outdoor AC condenser and the rooftop units (office 6, warehouse 1). Fin
  denting is mostly cosmetic or comb-repairable, and no evidence of functional damage by hail size was found.
- `HRE_BUILDING_CONTENTS`.

### Out of scope

- Cosmetic denting: metal roof, metal wall panels, overhead doors, gutters.
- Rain entry and interior damage after a roof breach; deck punctures by giant hail; cumulative damage from repeated
  small hail.
- Wind (→ `convective_wind_real_estate`) and flooding (→ `flood_real_estate`) from the same storm.
- Loss of use and business interruption; land and site works.
- Hail frequency, footprint and the radar-to-hail transform: Hazard owns these.

## 3. Reference buildings (selector `reference_building_id`)

| Selector | Hazard profile (r1) | Roof cover (10 years old) | Walls and windows | Roof share of structure value |
|---|---|---|---|---|
| `RE_RES_SFD_1S_SLAB` | `re_house_1s_wood_slab` | asphalt shingles on wood sheathing, 6:12 gable, 2,218 ft² | vinyl siding; windows 15% of wall | 3.75% |
| `RE_IND_WAREHOUSE` | `re_warehouse_1s_steel_slab` | standing-seam metal, 1:12, 100,347 ft² | insulated metal panels (dents excluded); windows 2% | 12% |
| `RE_COM_OFFICE_3S_SLAB` | `re_office_3s_slab` | TPO membrane on insulated metal deck, 18,004 ft² | masonry veneer (excluded); windows 33% | 2.7% |

## 4. Change classification

A **new cell** (no existing records changed). It adds a proposed cell folder and helper scripts only. It is not a
model release: no canonical artifact, no capability change in any released cell, no consumer pin, no package
inclusion. The repository's `hail_impact` pathway ID and Hazard's `mesh_diameter_mm` field are reused unchanged.

## 5. Existing-coverage check

| Where | What exists | Use here |
|---|---|---|
| `hail_solar` (canonical) | Module glass breakage on `mesh_diameter_mm` (logistic, three archetypes) | Axis precedent only. Not transferred: the reviewer's guide forbids a solar-panel response transfer for buildings. |
| `hail_wind` (proposal) | Fail-closed scaffold, pathway `hail_impact`; audit rejecting the legacy `Real Estate_Hail` array | Pathway ID; legacy rejection (D-HRE-14). |
| Other real-estate cells (own branches) | Flood, hurricane and convective wind curves for the same three buildings | Same selectors and structure-value denominator. |
| Public sources | No US building hail vulnerability curve; Hazus has no hail model. Engineering hail thresholds by roofing material exist (Haag); one open radar-to-claims building curve (Swiss) | Thresholds adopted (D-HRE-01, -07); Swiss curve used as a cross-check. |

## 6. Explicit non-changes

No released cell, schema, consumer adapter, artifact index or version registry is modified.
