<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# hail_real_estate damage-code metadata spec — model v0.1 / docs r1

## Damage code

| Field | Value |
|---|---|
| `damage_code_id` | `HAIL_REAL_ESTATE_ROOF_THRESHOLD_SCREENING_V0_1` |
| Cell / version | `hail_real_estate`, model v0.1, docs r1 |
| Status | noncanonical proposal; promotion gate blocked |
| Artifact | [`hail_real_estate__model_v0_1__docs_r1__curve_artifact.json`](hail_real_estate__model_v0_1__docs_r1__curve_artifact.json) (bundle v3) |
| Reference evaluator | `scripts/reference_helpers/hail_real_estate_curve_eval.py` |

## Pathways

| `pathway_id` | Axis field | Records |
|---|---|---|
| `hail_impact` | `mesh_diameter_mm` | roof cover: `HRE_RES_ROOF_ASPHALT_SHINGLE_LAMINATED`, `HRE_IND_ROOF_STANDING_SEAM_STEEL`, `HRE_OFF_ROOF_TPO_MEMBRANE_AND_INSULATION`; walls and windows (Tier-4): `HRE_RES_WALLS_WINDOWS_T4`, `HRE_IND_WINDOWS_T4`, `HRE_OFF_WINDOWS_T4` |

## Inputs

### Hazard input

| Field | Unit | Meaning | Range |
|---|---|---|---|
| `mesh_diameter_mm` | mm | Hazard's MESH75 hail diameter for the native pixel (15.096 × ((raw/2.54)²)^0.206, capped at 203.2 mm), read as the largest hailstone at the building | 0–203.2; above withholds; negative error |

Hazard sends no damage for pixels below raw MESH 25.4 mm, so the smallest nonzero input it passes is 38.98 mm.
Inch fields, report counts and cell maxima are not inputs.

### Selectors

| Field | Required | Allowed |
|---|---|---|
| `reference_building_id` | yes, no default | `RE_RES_SFD_1S_SLAB`, `RE_IND_WAREHOUSE`, `RE_COM_OFFICE_3S_SLAB` |
| `screening_assumption_set_id` | only for `HRE_WALLS_AND_WINDOWS` | `HRE_T4_WALLS_WINDOWS_SCREENING_2026_10_18` |

Profile IDs (e.g. `re_house_1s_wood_slab`) are not selectors; the profile binding maps them.

### Conditioners

None. Shingle type, TPO attachment and roof age are fixed by the profile and assumptions.

### Exposure

One reference building per call. `failure_unit_id` is required:

- `HRE_ROOF_COVER` and `HRE_WALLS_AND_WINDOWS` are priced.
- `HRE_EXPOSED_EQUIPMENT` and `HRE_BUILDING_CONTENTS` return withheld.

## Outputs

The output is `damage_emit.v2`, mode `scalar_mean`. `scalar_central_dr` is the replaced fraction of **the unit's own
replacement value** for one event, returned with `curve_id` and metadata flags.

To get the building level, multiply by the unit's share of structure replacement cost new
(`failure_units[].share_of_structure_rcn`):

| Unit | House | Warehouse | Office |
|---|---|---|---|
| `HRE_ROOF_COVER` | 0.0375 | 0.12 | 0.027 |
| `HRE_WALLS_AND_WINDOWS` | 0.060689 | 0.005673 | 0.053387 |

Withheld results carry `scalar_central_dr = null` and reason codes:

| Reason code | When |
|---|---|
| `ABOVE_SOURCE_VALID_RANGE` | diameter above 203.2 mm |
| `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` | exposed equipment or contents requested (with `FUNCTIONAL_EQUIPMENT_HAIL_EVIDENCE_NOT_FOUND` or `CONTENTS_DEFERRED_SEPARATE_FAILURE_UNIT`) |

Errors (fail closed):

- **Request fields:** `PATHWAY_ID_REQUIRED`, `PATHWAY_ID_UNKNOWN`, `REFERENCE_BUILDING_ID_REQUIRED`,
  `REFERENCE_BUILDING_ID_UNKNOWN`, `FAILURE_UNIT_ID_REQUIRED`, `FAILURE_UNIT_ID_UNKNOWN`.
- **Axis:** `AXIS_PAYLOAD_REQUIRED`, `AXIS_VALUE_INVALID`, `AXIS_OUTSIDE_VALID_RANGE`.
- **Acknowledgement:** `SCREENING_ASSUMPTION_SET_REQUIRED` (walls without the acknowledgement),
  `SCREENING_ASSUMPTION_SET_UNSUPPORTED` (wrong acknowledgement).

Hazard's generic loader returns its own names for seven of these (validation report §4).

**Always-on flags:**

- `NONCANONICAL_PROPOSAL`, `SCREENING_MATERIAL_THRESHOLD_CURVES`, `COMPONENT_FAILURE_UNITS_OWN_VALUE_DENOMINATOR`
- `AXIS_IS_HAZARD_MESH75_READ_AS_HAILSTONE_DIAMETER`, `THRESHOLD_BAND_READ_AS_90_PERCENT_RANGE`
- `COSMETIC_DENTING_EXCLUDED`, `CONSEQUENTIAL_INTERIOR_LEAKAGE_NOT_PRICED`, `CUMULATIVE_SUB_SEVERE_HAIL_NOT_MODELLED`
- `REFERENCE_BUILDING_ASSUMPTIONS_NOT_OBSERVED`, `NOT_FIELD_OR_CLAIMS_CALIBRATED`, `PLATFORM_CODES_PROPOSED_NOT_ISSUED`

**Unit flags:**

- Roof records add `ROOF_COVER_HAIL_THRESHOLD_EVIDENCE`, `WHOLE_ROOF_COVER_REPLACED_WHEN_DAMAGED` and
  `ROOF_COVER_SHARE_FROM_HAZUS_COST_RATIOS_OR_JUDGMENT`.
- Walls-and-windows records add `TIER4_SCREENING_WALLS_AND_WINDOWS`, `NO_PUBLIC_WALL_OR_WINDOW_HAIL_THRESHOLD` and
  `HAIL_FACING_SHARE_JUDGMENT`.

**Building flags:**

- House: `ROOF_ASPHALT_SHINGLE_LAMINATED_ASSUMED_NOT_IMPACT_RATED`.
- Warehouse: `METAL_ROOF_FUNCTIONAL_DAMAGE_ONLY_COSMETIC_DENTING_EXCLUDED`, `WAREHOUSE_ROOF_COST_SHARE_JUDGMENT`.
- Office: `TPO_ATTACHMENT_AND_COVER_BOARD_NOT_STATED`.

## Capability declaration

- **Supported:** failure-unit scalar DR, conditional.
- **Withheld:** scenario loss (until the consumer qualifies the value); intrinsic spread is not carried; annual and
  tail metrics are consumer-owned and withheld before promotion.
- **Cap binding** (consumer-enforced, fail-closed): exact pin; routing by unit and building; unit DR multiplied by
  the same unit's share; the walls unit only with the acknowledgement; all perils on one building in one event at most
  100% of structure value.

## Example

```json
{"pathway_id": "hail_impact", "failure_unit_id": "HRE_ROOF_COVER",
 "reference_building_id": "RE_RES_SFD_1S_SLAB", "mesh_diameter_mm": 50.8}
```

→ `HRE_RES_ROOF_ASPHALT_SHINGLE_LAMINATED`, `scalar_central_dr` 0.94972: a 95% chance the roof cover is replaced.
That is 0.94972 × 0.0375 = 3.56% of structure value.
