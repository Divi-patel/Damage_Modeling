<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
scope: Step 5 (derive the response) for tropical-cyclone wind × real estate — the fifteen proposed curve records, how values between published speeds are computed, behaviour outside the published range, and why no smooth form is fitted.
-->

# Curve records and form — tropical_cyclone_wind_real_estate model v0.1 / docs r1

Exact ordinates: [CURVE_ORDINATES](CURVE_ORDINATES_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv)
(615 rows = 15 records × 41 speeds). Chart: [candidate curves](../previews/tropical_cyclone_wind_real_estate_v0_1_candidate_curves.png).
Reproduce: `scripts/reference_helpers/extract_tropical_cyclone_wind_real_estate_hazus_ordinates.py` (source verification §4).

## 1. The fifteen proposed curve records

One record per reference building × Hazus terrain class. All are Hazus building-loss rows
(`huDamLossFun`, `DamLossDescID` 5) at 50, 55, …, 250 mph peak gust (10 m, open terrain).

| curve_id pattern | Reference building | Hazus type, wbID | Characteristics |
|---|---|---|---|
| `TCRE_RES_HAZUS_WSF1_<TERRAIN>` | `RE_RES_SFD_1S_SLAB` | WSF1 (CONUS), 6 | gable · no SWR · 6d @ 6"/12" · toe-nail · no garage · no shutters · shingle |
| `TCRE_COM_HAZUS_SECBL_<TERRAIN>` | `RE_COM_LOWRISE` | SECBL, 1812 | BUR · low windows · debris B · standard metal deck · no shutters |
| `TCRE_IND_HAZUS_SPMBL_<TERRAIN>` | `RE_IND_WAREHOUSE` | SPMBL, 1729 | old roof deck · standard metal deck · no shutters |

`<TERRAIN>` ∈ `OPEN` (z0 0.03 m), `LIGHT_SUBURBAN` (0.15), `SUBURBAN` (0.35), `LIGHT_TREES` (0.70), `TREES` (1.00).

Selected values (building loss, % of replacement cost):

| Record | 100 mph | 120 mph | 140 mph | 160 mph |
|---|---:|---:|---:|---:|
| House, open | 5.2 | 31.3 | 77.9 | 97.9 |
| House, suburban | 1.4 | 9.3 | 51.2 | 89.1 |
| Commercial, open | 1.0 | 8.8 | 31.3 | 61.6 |
| Commercial, suburban | 0.4 | 5.7 | 25.9 | 55.4 |
| Warehouse, open | 6.8 | 39.5 | 88.2 | 99.9 |
| Warehouse, suburban | 1.6 | 12.7 | 56.1 | 94.7 |

## 2. Between published speeds: straight lines

**Proposed (D-TCRE-17): straight lines between the published 5-mph points**, keeping every published value as is.

```text
- the table is dense (41 points); a 5-mph step is finer than the uncertainty of a screening gust field;
- reproduces every published value exactly and adds no shape the source did not publish;
- the cells built on published tables (flood_real_estate, flood_wind, wildfire_*) use straight lines; smooth
  forms are used where curves are derived (hail, wind);
- a smooth fit could only move published values; with 41 points and no gaps there is nothing to fill.
```

No form comparison is run: unlike the flood tables (1-ft steps with a few knots for NACCS), nothing here is sparse.

**Small dips are kept, not repaired.** Five of the fifteen records dip by at most 0.2 points at 205–235 mph
(TCRE-C014), which is Hazus simulation noise. Repairing them (for example a running maximum) would change
published values for no material gain. The validator bounds every dip at 0.005 and requires them to sit above
200 mph; a larger dip in a future record stops the build.

**The commercial terrain curves cross** (TCRE-C024): light-suburban sits above open from 90 mph. This is the
source's behaviour and is kept; the record set carries a flag so nobody reads open terrain as the commercial worst
case.

## 3. Outside the published range

| Region | Behaviour | Reason |
|---|---|---|
| gust < 0 or not a number | error `AXIS_VALUE_INVALID` | malformed input |
| 0 ≤ gust < 50 mph | **0**, flag `BELOW_SOURCE_RANGE_ZERO` | every selected record is exactly 0 at 50 mph (D-TCRE-18) |
| 50 ≤ gust ≤ 250 mph | straight line between published points | — |
| gust > 250 mph | **withheld**, `ABOVE_SOURCE_VALID_RANGE` | nothing published above; no clamp, no extrapolation |

Hazard's delivered range (about 61–229 mph) sits wholly inside the published range, so the two edge rules only
protect against other callers.

All fifteen records share one range (50–250 mph). That lets the current Hazard generic loader, which checks one
pathway-level `valid_range` and routes by selectors only, use the records unchanged (TCRE-C020).
