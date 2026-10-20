# Curve derivation dossier — tropical_cyclone_wind_wind model v1.1

## Answer first

No new damage curve was fitted. Model v1.1 preserves the released Jaimes model-v1.0 evidence and equation,
then adds a governed target-use decision: the 3.3 MW / 100 m curve may screen the canonical 5 MW / 100 m
turbine under exact opt-in. The scientific uncertainty is therefore the target transfer, not a hidden
parameter refit.

## Source and target

| Dimension | Source evidence | Target use |
|---|---|---|
| rated power | 3.3 MW | 5 MW |
| hub height | 100 m | 100 m |
| rotor diameter | 114 m | canonical profile does not use rotor diameter as a selector; source value stays visible |
| wind input | 3-second peak gust at 10 m, km/h | exact same field |
| output | expected source-defined turbine/tower damage ratio | screening DR for the declared rotor+nacelle+tower value scope |
| evidence grade | source-derived engineering proxy | owner-approved target-mismatch screening proxy |

The full evidence review, equation provenance and source limitations remain in the preserved
[model-v1.0 rollback snapshot](../model_v1_0__docs_r1/README.md).

## Numerical derivation

The v1.1 proxy record is a parameter-identical copy of `TCWW_JAIMES_3P3MW_100M_SCREENING`:

```text
DR = 0                                           when V <= 90 km/h
DR = 1 - exp[-ln(2) ((V - 90) / 73.3)^4.99]     otherwise
```

Exact source-native selectors keep the released rules: `90 < V < 108 km/h` is withheld,
`108–252 km/h` is evaluated, and `V > 252 km/h` is withheld. The named 5 MW proxy adds two explicit screening
completion branches:

| Proxy input | Runtime treatment | Why |
|---|---|---|
| `V <= 90 km/h` | source-assumed zero with the existing flag | unchanged source equation branch |
| `90 < V < 108 km/h` | zero with `SCREENING_TRANSITION_BAND_ASSIGNED_ZERO` | conservative completion; not source evidence |
| `108 <= V <= 252 km/h` | unchanged Jaimes equation | source-supported simulation range |
| `V > 252 km/h` | `max_dr = 1` with `SCREENING_ABOVE_SOURCE_RANGE_CAPPED_AT_MAX_DR` | bounded cap; no tail extrapolation |

The full-population Hazard comparison evaluated 113,526 governed M1 events in all 1,773 active cells at 20
turbine nodes. The transition-zero branch has a `$10,564.85` upper bound on summed placement EAL—about
`0.00037%` of the `$2.8527B` centroid screening-EAL sum across those placements. The cap keeps extreme events
in scope without claiming response beyond the model's bounded maximum. Neither rule changes the wind axis or
the source-native records.

## Why the proxy is useful now

- it lets Hazard exercise and review the real canonical Wind Farm rather than changing the asset to fit a
  source curve;
- it unlocks the M2 field-coupling and M4 aggregation tests that are independent of future curve quality;
- it gives the dashboard a transparent screening result instead of a hidden legacy fallback; and
- its exact IDs provide a clean replacement point when target-matched 5 MW evidence arrives.

## Why the proxy is limited

Turbine size, rotor diameter, controls, drivetrain and structural design can change vulnerability. This
package does not prove those changes are immaterial. It states only that the owner accepts the source curve as
a bounded screening proxy for this one canonical target.

The value crosswalk is also partial. Foundation, collection/electrical, substation and civil units do not
receive a zero DR; they receive no result from this model.

## Replacement trigger

Revisit when target-matched modern 5 MW evidence, a reviewed physical transfer model, component-specific
curves or better value data becomes available. Replacement requires a new governed Damage model version and
a Hurricane rerun; it cannot be applied as silent cleanup.
