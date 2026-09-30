# Derivation dossier — tropical-cyclone wind × solar model v2.1

## Purpose

Deliver a coverage-complete, screening-grade physical damage curve that Hazard can actually call. Model v2.1
is a behavior-changing successor to the partial v2.0 proposal. It is canonical
at labeled screening grade after the Everglades exact-pin experiment and owner
acceptance; it is not calibrated, claims-calibrated or bankable.

## Curve architecture

```text
array architecture axis
  fixed tilt: qualified event/design net-pressure ratio
  tracker:    attained-state Vnormal / exact-system Ucrit

site-facility axis
  preferred: qualified event/design wind-pressure ratio
  proxy:     (10 m event 3-s gust / qualified design 3-s gust)^2

failure-unit response
  DR_u(x) = sum_s P(exact state s | x) × same-unit cost_ratio_s

plant assembly
  direct/civil loss = sum_u value_u × DR_u
  support DR        = direct/civil loss / direct/civil value
  physical loss     = direct/civil loss + support value × support DR
  physical DR       = physical loss / 877.7957023626668
```

State probability is never relabeled as damage ratio. Every cost ratio is separately explicit.

## Failure-unit coverage

| Failure unit | V2.1 treatment | Axis |
|---|---|---|
| fixed/tracker module field | retained v2.0 Tier-4 ordered states | architecture-specific |
| fixed structure/tracker SBOS | retained v2.0 Tier-4 ordered states | architecture-specific |
| foundation | new Tier-4 screening ordered states | site facility |
| power conversion and collection | new Tier-4 screening ordered states | site facility |
| GSU and substation | new Tier-4 screening ordered states | site facility |
| SCADA and communications | new Tier-4 screening ordered states | site facility |
| civil infrastructure | new Tier-4 screening ordered states | site facility |
| replacement support | derived once in assembly; no intrinsic curve | assembled direct/civil DR |

The five new records use `beta_ln=0.35`, four exact states, and unweighted lower/central/upper resistance
scenarios. Their full parameters are machine truth in the curve artifact and parameter-tier CSV.

## Value basis

| Bucket | 2024 USD/kWdc |
|---|---:|
| modules | 291.21485143992487 |
| mounting | 109.98972602739727 |
| foundation | 31.12448715327472 |
| power conversion and collection | 116.83772835067089 |
| GSU/substation | 106.50466417910448 |
| SCADA | 1.31 |
| civil | 31.223744292237445 |
| replacement support | 189.59050092005714 |
| **physical replacement total** | **877.7957023626668** |
| installed CAPEX reporting denominator | 1120.0 |

The 242.20429763733296 USD/kWdc difference between installed CAPEX and physical replacement value is labeled
soft/sunk/nonphysical for this physical-destruction calculation. It is not called wind-immune and does not
cap the physical replacement DR.

## Representative outputs

For fixed tilt with both array and site-facility ratios equal to 1.0:

| Scenario | Physical DR | Physical loss (2024 USD/kWdc) |
|---|---:|---:|
| lower resistance / higher damage | 0.3335660993 | 292.8028884 |
| central screening | 0.1441695907 | 126.5514471 |
| upper resistance / lower damage | 0.0562454851 | 49.3720451 |

At ratio 2.0 the central physical DR is 0.8034375623. V2.1 therefore has no legacy 48% ceiling.

The [full-plant screening curve table](FULL_PLANT_SCREENING_CURVE_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv)
contains 246 evaluated points: fixed and tracker architectures, all three resistance scenarios, and demand
ratios from 0.00 through 2.00 in 0.05 increments. The same table is included as `Plant_Curve_Table` in the
governed workbook.

## Honest limitations

- The common-unit medians and costs are Tier-4 screening assumptions, not TC claims calibration.
- One representative array-zone curve is applied to the full array value in the reference convenience view.
- The reference value profile is not a substitute for site-specific replacement values.
- The three resistance scenarios are not probabilities, percentiles, or a frequency distribution.
- Wind-only output excludes rain, debris, surge/flood, and tornado loss.
