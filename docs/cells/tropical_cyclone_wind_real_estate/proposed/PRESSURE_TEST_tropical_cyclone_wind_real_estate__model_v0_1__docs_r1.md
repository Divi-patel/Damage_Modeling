<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-16
status: draft
scope: Step 4 (judge evidence) for tropical-cyclone wind × real estate — what each verified curve can and cannot support, how much the unknown building details and terrain move the answer, the source anomalies found, and what stays withheld.
-->

# Evidence pressure test — tropical_cyclone_wind_real_estate model v0.1 / docs r1

> **Model v0.2 note (2026-10-16):** this step document describes model v0.1. Model v0.2 binds the cell to the
> Hazard reference profiles r1: a new three-storey office (Hazus SECBM, single-ply membrane, medium windows,
> D-TCRE-23), a new-or-average warehouse roof deck (D-TCRE-24); house and retail unchanged (D-TCRE-25). See the
> [v0.2 dossier](tropical_cyclone_wind_real_estate_curve_derivation_dossier__model_v0_2__docs_r1.md).

Inputs: [source verification](SOURCE_VERIFICATION_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md),
[sources](SOURCE_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
[claims](CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
[variant sensitivity](VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv).
Parameter tiers: [PARAMETER_TIER_TABLE](PARAMETER_TIER_TABLE_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv).

The building types, terrain handling and characteristic rule were chosen by JL on 2026-10-12 (checkpoint 2). Every
other selection here is **proposed**.

## 1. The chain each curve must support

```text
STORM 10-minute wind (Hazard)
  -> 3-second peak gust at 10 m, open terrain, mph       (Hazard's bridge; not repeated in Damage)
  -> terrain class at the building                       (required selector; consumer maps site roughness)
  -> Hazus building loss ratio                           (published ordinate, 5-mph steps, 50-250 mph)
  -> × structure replacement cost new                    (value link, step 6)
```

| Link | Status | Evidence |
|---|---|---|
| Axis: open-terrain 3-s gust at 10 m | Supported — same quantity on both sides | TCRE-C001, C020 |
| Ordinate: building loss ratio | Supported — two independent copies identical | TCRE-C011 |
| Mechanisms inside the ordinate | Pressure + debris + rain ingress, stated by FEMA | TCRE-C002 |
| Reference-building match | By Hazus type + most-common characteristics | TCRE-C006–C010 |
| Terrain | Five classes in the source; consumer must supply one | TCRE-C005, C018 |
| Denominator | Total building replacement cost (Hazus) ≈ structure RCN (ours) | TCRE-C004 |
| Calibration to observed losses | Component validation only (roof cover, sheathing, whole-roof failures in Andrew, Erin, Fran; §5.5); **no loss-claims calibration verified for these three variants** | TCRE-S001 §5.5 |

No load-bearing link is missing. The chain is complete at **screening grade**: a published engineering simulation
for a reference building, not calibrated to observed losses for that building.

## 2. How much the unknowns move the answer

From the [variant sensitivity table](VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv)
(building loss, % of replacement cost):

| Change from the reference building | House 120 mph open | House 140 mph open | Commercial 140 mph open | Warehouse 120 mph open |
|---|---:|---:|---:|---:|
| **Reference (most common)** | **31.3** | **77.9** | **31.3** | **39.5** |
| Suburban terrain instead of open | 9.3 | 51.2 | 25.9 | 12.7 |
| Hip roof | 22.0 | 67.8 | — | — |
| Weak garage door | 55.7 | 91.0 | — | — |
| Single-ply membrane instead of BUR | — | — | 35.6 | — |
| Medium window area | — | — | 39.5 | — |
| New roof deck | — | — | — | 23.5 |
| Other type: MLRM1 strip mall / SPMBM medium | — | — | 62.7 (MLRM1) | 30.5 (SPMBM) |

What this means:

1. **Terrain is the biggest single driver for the house and the warehouse** (about 3× at 120 mph). This is why
   JL made it a required input rather than an assumption (TCRE-C018).
2. **The unknown building details move the house by roughly ± 10–25 points** at 120–140 mph. The most-common
   rule picks a middle-to-weak house (6d nails, toe-nails, no SWR) — which is what most of the stock is
   (Table C-2), not a worst case.
3. **The commercial type choice matters more than its details.** A masonry strip mall (MLRM1) loses about twice
   what the engineered building (SECBL) does at 140 mph. The reference "small low-rise retail or office, masonry or
   steel frame" matches the engineered type better; strip-mall retail stays a recorded alternative (TCRE-C009).

## 3. Source anomalies and how they are contained

| Finding | Effect on this cell | Containment |
|---|---|---|
| SPMB superior-deck rows are copies of other size classes (TCRE-C016) | None on the selected record (standard deck). Blocks "superior deck attachment" as a warehouse measure. | Rows excluded; flag `HAZUS_SPMB_FAMILY_ANOMALY_NOT_IN_SELECTED_ROW`; revisit when FEMA explains |
| SPMBS standard rows above medium and large, against the manual's direction (TCRE-C017) | None (SPMBS not used) | Recorded |
| Dips ≤ 0.2 points in 5 of the 15 selected records, 205–235 mph (TCRE-C014) | Negligible; published values kept | Flag `HAZUS_SIMULATION_NOISE_SMALL_DIPS`; validator bounds the dip size |
| Extract mapping sheets use 12 old regions (TCRE-C013) | None (defaults read from the 7.0 manual) | Recorded |
| Commercial: light-suburban terrain above open terrain at 90–250 mph (27.7% vs 18.6% at 130 mph); open levels off at 88.3% (TCRE-C024) | Open terrain is **not** the worst case for the commercial building | Published values kept; flag `HAZUS_COMMERCIAL_TERRAIN_ORDER_NOT_MONOTONE`; terrain must still be supplied, never defaulted to open as a "conservative" choice |

## 4. Proposed selections

| Item | Proposal | Decision row |
|---|---|---|
| House | WSF1 CONUS, most-common characteristics, wbID 6 | D-TCRE-14 (JL accepted type) |
| Commercial | SECBL (= MECBL), BUR, low windows, debris B, standard deck, wbID 1812 | D-TCRE-15 (JL accepted type) |
| Warehouse | SPMBL, old deck, standard deck, wbID 1729; reference floor area > 50,000 ft² | D-TCRE-16 (JL accepted type) |
| Terrain | Required selector, five Hazus classes, no default, no interpolation | D-TCRE-06 (JL decided) |
| Characteristics | Most common (Table C-2 all-region average), fixed and named | D-TCRE-07 (JL decided) |
| Tree fall (house) | Deferred additive term; withheld, not zero | D-TCRE-13 |

## 5. What stays withheld

```text
contents, loss of use                  deferred failure unit / disruption stage (D-TCRE-08)
tree fall on the house                 deferred additive term (D-TCRE-13)
other characteristic variants          withheld until published as records (D-TCRE-19)
scenario dollars                       per-area replacement cost not selected (D-TCRE-09)
annual and tail metrics                consumer-owned
gusts above 250 mph                    outside the published range (D-TCRE-18)
```

## 6. Grade

```text
model_grade: screening_source_native_adopted_tables
ordinates:   T2 (published FEMA engineering simulation, two identical independent copies)
reference-building characteristics: T2 frequencies, applied as T4 assumptions about one building
warehouse record: T2 with a source-family anomaly flag
calibration: none verified for these variants
```
