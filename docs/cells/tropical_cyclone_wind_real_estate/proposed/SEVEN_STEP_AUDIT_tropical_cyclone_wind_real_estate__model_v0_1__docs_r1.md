<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
-->

# Seven-step audit — tropical_cyclone_wind_real_estate model v0.1 / docs r1

## Governing y-axis and loss contract

```text
DR(b, t, v) = repair cost of the structure of reference building b
              / replacement cost new of the same structure
              | tropical-cyclone wind with peak 3-s gust v (10 m, open terrain, mph) at a site of terrain class t
              (wind pressure, windborne debris and rain entering through wind damage, combined)

loss = DR × structure replacement cost new      (one failure unit, 100% of structure RCN; no support line)
```

Excluded: contents, land, site works, loss of use and business interruption, storm surge and waves, rainfall
flooding, TC-spawned tornadoes, tree fall on the house (deferred additive term).

## Step 1 — define the asset and boundary

The three `flood_real_estate` reference buildings, with wind attributes stated in the
[reference buildings](REFERENCE_BUILDINGS_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md) §1. Boundary:
the building structure only. Value vintage: open (value basis not selected).

## Step 2 — decompose the asset into failure units

One failure unit, `TCRE_BUILDING_STRUCTURE`, at the source-native whole-building grain (D-TCRE-05). Roof, walls,
openings and interior are inside the Hazus loss ratio; no source separates them into priced units. Contents are a
deferred unit (D-TCRE-08).

## Step 3 — choose the y-axis and value basis

Structure replacement cost new; Hazus loss is over total building replacement cost (TCRE-C004). Depreciated,
market and assessed values are rejected, as in `flood_real_estate`.

## Step 4 — split the value basis row by row

[Value crosswalk](VALUE_CROSSWALK_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv): structure RCN
(direct, 100%); contents, tree fall, land, site works and loss of use excluded with reasons.

## Step 5 — allocate physical value by failure unit and zone

The single unit carries 100% of structure RCN. No zones, no at-risk fraction below one, no support allocation.

## Step 6 — specify the site-condition exposure adapter

| Site condition | Treatment in v0.1 | Double-counting guard |
|---|---|---|
| Terrain roughness | Required selector, five Hazus classes; picks the record | Applied once: never also as a gust reduction (Hazard applies none) |
| Topographic speed-up (hills, escarpments) | Not modelled; must already be in the delivered gust if wanted | Never applied both in the gust and in the curve |
| Windborne-debris environment | Fixed inside the selected record (house: WSF1 model; commercial: environment B) | No separate debris pathway (D-TCRE-04) |
| Nearby trees | Tree fall deferred; trees' sheltering is inside the terrain class | Tree fall must not raise the base record when added later |
| Opening protection, roof upgrades | None in the reference buildings; later measures are field changes on the same source family | One field, one record; no curve-side credit on top |
| Storm surge, rain flooding | `flood_real_estate` | Consumer keeps combined damage ≤ 100% (D-TCRE-11) |

## Step 7 — apply qualified curves and reconcile loss, or withhold

Fifteen proposed records exist ([curve form](CURVE_FORM_DECISION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md)).
Damage ratios are supportable at screening grade. Scenario dollars are blocked until a per-area replacement cost is
selected. Until owner review and canonical promotion, the cell stays a proposal (`NO_RUNTIME_CURVE` for runtime).

## Audit outcome

| Step | Status | Evidence passed | Blocking seam | Required next evidence |
|---|---|---|---|---|
| 1. Define asset | proposed | Reference buildings shared with flood; wind attributes stated | Owner acceptance of the scope | reviewer sign-off |
| 2. Decompose asset | proposed | Whole-building unit, source-native grain | — | — |
| 3. Choose basis | proposed | RCN matches the Hazus loss definition | — | — |
| 4. Split basis | proposed | Crosswalk complete; exclusions named | — | — |
| 5. Allocate value | proposed | 100% to one unit | Per-area cost source open (shared with flood) | Select option A–D |
| 6. Site adapter | proposed | Terrain required, applied once | Hazard has no roughness field yet | Hazard terrain-class field and mapping rule |
| 7. Curves/loss | partial | Fifteen records, ordinates verified in two copies | Dollars need step 5; owner review; consumer terrain input | Steps 5 and 7 |

| pathway_id | failure_unit_id | axis/bridge status | evidence/curve status | value status | final support | reason code |
|---|---|---|---|---|---|---|
| `tropical_cyclone_wind` | `TCRE_BUILDING_STRUCTURE` | defined (open-terrain 3-s gust, mph; terrain selector) | fifteen proposed records, T2 | share fixed, dollars open | DR proposed; dollars withheld | `NO_RUNTIME_CURVE` (scaffold) |
| — | `TCRE_BUILDING_CONTENTS` | — | deferred | excluded | withheld | `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` |
