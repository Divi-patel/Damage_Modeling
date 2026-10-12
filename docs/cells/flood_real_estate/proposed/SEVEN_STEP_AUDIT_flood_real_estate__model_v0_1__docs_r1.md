<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
-->

# Seven-step audit — flood_real_estate model v0.1 / docs r1

## Governing y-axis and loss contract

```text
DR(b, w, d) = repair cost of the structure of reference building b
              / replacement cost new of the same structure
              | still floodwater of type w at depth d above the first finished floor

loss = DR × structure replacement cost new      (one failure unit, 100% of structure RCN; no support line)
```

Excluded: contents, land, site works, depreciation, business interruption, wave and high-velocity damage
(deferred pathway), mould and long-duration effects beyond what the source curves embed.

## Step 1 — define the asset and boundary

Three reference buildings (house, small low-rise commercial, one-story warehouse), each a stated assumption, not
an appraisal of a real building ([reference buildings](REFERENCE_BUILDINGS_flood_real_estate__model_v0_1__docs_r1.md) §1).
Boundary: the building structure only. Value vintage: open (value basis not selected).

## Step 2 — decompose the asset into failure units

One failure unit, `FRE_BUILDING_STRUCTURE`, at the source-native whole-building grain (D-FRE-03). Contents are a
second, deferred unit (D-FRE-12). No pathway control (fence, levee, floodwall) is treated as a vulnerable
component. Roof, walls and services are inside the whole-building ratio for flood and are split later for hail
and wind.

## Step 3 — choose the y-axis and value basis

Structure replacement cost new, matching both libraries (FRE-C001) and NSI `fullrep` (FRE-C024). Depreciated,
market and assessed values are rejected.

## Step 4 — split the value basis row by row

[Value crosswalk](VALUE_CROSSWALK_flood_real_estate__model_v0_1__docs_r1.csv): structure RCN (direct, 100%);
contents, land, site works and business interruption excluded with reasons. NSI's depreciated `val_struct` is not a
value row; it is rejected as a denominator (reference buildings §3).

## Step 5 — allocate physical value by failure unit and zone

The single unit carries 100% of structure RCN. No zones, no at-risk fraction below one and no support allocation
are needed at whole-building grain: the source curves already express damage over the whole structure.

## Step 6 — specify the site-condition exposure adapter

| Site condition | Treatment in v0.1 | Double-counting guard |
|---|---|---|
| First-floor height | Stated per reference building (NSI 2026: 0.75 / 0.25 / 0.25 ft); converts depth above grade to depth above floor | Applied once, in the axis bridge only |
| Flood protection (levee, floodwall, berm, dry floodproofing) | No credit. Protection, if any, must already be reflected in the delivered water depth | Never applied both in delivered depth and as a curve reduction |
| Elevation as a measure | A change to first-floor height only (later resiliency work) | Same single bridge |
| Water type | Conditioner: freshwater → Hazus, coastal surge → NACCS, unknown → withheld | Libraries never blended (D-FRE-19) |
| Waves, fast flow, debris | Separate deferred pathway; withheld, not zero | Not inside any still-water curve (D-FRE-06) |
| Flood duration, contamination, mould | Not a v0.1 input; NACCS Max is advised where extensive mould is likely (FRE-C010) | No silent switch to Max |

## Step 7 — apply qualified curves and reconcile loss, or withhold

Six proposed records exist ([curve form](CURVE_FORM_DECISION_flood_real_estate__model_v0_1__docs_r1.md)).
Damage ratios are supportable at screening grade. Scenario dollars are blocked until a per-area replacement cost
is selected. Until owner review and the runtime artifact, every output remains withheld (`NO_RUNTIME_CURVE`).

## Audit outcome

| Step | Status | Evidence passed | Blocking seam | Required next evidence |
|---|---|---|---|---|
| 1. Define asset | proposed | Three reference buildings with stated attributes | Owner acceptance of the scope | reviewer sign-off |
| 2. Decompose asset | proposed | Whole-building unit, source-native grain | — | — |
| 3. Choose basis | proposed | RCN matches both libraries and NSI `fullrep` | — | — |
| 4. Split basis | proposed | Crosswalk complete; exclusions named | — | — |
| 5. Allocate value | proposed | 100% to one unit | Per-area cost source open | Select option A–D (reference buildings §4) |
| 6. Site adapter | proposed | First-floor height sourced (NSI 2026); no protection credit | Commercial/industrial default is read from data, not documented (T3) | NSI documentation of non-residential defaults |
| 7. Curves/loss | partial | Six records with verified ordinates | Scenario dollars need step 5; runtime artifact and owner review | Steps 5 and 7 |

| pathway_id | failure_unit_id | axis/bridge status | evidence/curve status | value status | final support | reason code |
|---|---|---|---|---|---|---|
| `flood_inundation_contact` | `FRE_BUILDING_STRUCTURE` | defined (depth above floor; FFH bridge) | six proposed records, T2 | share fixed, dollars open | DR proposed; dollars withheld | `NO_RUNTIME_CURVE` (scaffold) |
| `flood_wave_velocity` | `FRE_BUILDING_STRUCTURE` | not defined | none | — | withheld | `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` |
| — | `FRE_BUILDING_CONTENTS` | — | deferred | excluded | withheld | `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` |
