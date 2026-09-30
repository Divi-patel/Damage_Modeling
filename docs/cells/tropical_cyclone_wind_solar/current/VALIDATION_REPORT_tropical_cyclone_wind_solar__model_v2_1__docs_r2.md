# Validation report — tropical-cyclone wind × solar model v2.1 / docs r2

## Result

```text
PASS_AS_CANONICAL_COVERAGE_COMPLETE_SCREENING_RELEASE
release_checks=220
proposal_regression_checks=25663
dual_read_comparisons=171
curve_records=10
runtime_kats=5
rejection_kats=5
sources=71
claims=92
parameters=93
value_rows=18
old_vs_new_rows=10
full_plant_curve_table_rows=246
workbook_sheets=10
workbook_qa_passes=8
```

## Usability gates

| Gate | Result |
|---|---|
| fixed and tracker full-plant calls return numeric DR | PASS |
| foundation/power/GSU/SCADA/civil return numeric same-unit DR | PASS |
| named physical replacement-value coverage | 100% |
| replacement support allocation | once, reconciled |
| scenario physical dollars with capacity | PASS |
| 0.00–2.00 full-plant curve table, 0.05 step | PASS — 246 architecture/scenario rows |
| zero demand | zero DR/loss |
| monotonicity over both axes `[0,2]` | PASS |
| lower/central/upper resistance ordering | PASS |
| legacy ~48% artificial cap absent | PASS; fixed central DR at ratio 2.0 = 0.8034375623 |
| exact artifact pin | PASS |
| obsolete v2.0 scenario-loss/unit-withholding runtime labels removed | PASS |
| annual-metric promotion field distinguished from event-output availability | PASS |
| v2.0 bytes preserved | PASS |
| canonical identity and current paths | PASS |
| proposal bytes preserved | PASS — `4dd951495a9f…` |
| proposal/current numerical parity | PASS — 171 fixed, tracker and GSU comparisons |
| docs-r2 status correction | PASS — `CANONICAL_SCREENING_RELEASE`; no stale noncanonical output label |
| KAT promotion diff | PASS — canonical identity/status metadata only; numerical payload unchanged |
| canonical artifact index pin | PASS |

## Regression matrix

| Check | Result |
|---|---|
| canonical release validator | PASS — 220 checks, 171 dual reads |
| preserved model v2.1 proposal validator | PASS — 25,663 checks |
| preserved model v2.0 validator | PASS — 36,425 checks |
| preserved model v1/docs-r2 validator | PASS — runtime hashes unchanged |
| preserved model v0.1 validator | PASS — machine hashes unchanged |
| strong-wind-solar v2 proposal | PASS |
| repository runtime contracts | PASS — nine indexed canonical artifacts |
| damage-curve skill validation/self-tests | PASS |

## Legacy-defect regression

- State probability remains distinct from economic DR; recomposition is checked numerically.
- Unsupported physical value is not zeroed. All direct/civil value has a numeric screening proxy.
- Tracker response still requires attained and qualified state.
- No anchored-logistic intercept subtraction is used.

## Machine hashes

| File | SHA-256 |
|---|---|
| curve artifact | `2fbc34fbf8f91df408fe1b3c8d01d260d013119cbcba594b6a9a60044cd2113e` |
| capability | `ad9075d09decef9089b03a9da2e34e1cbed92ba162f4b95d0d4afca5e459204f` |
| known-answer tests | `4df723816bc751a92b412ea9c6dafe91f25ee6c645133921867541aea88c1293` |
| workbook | `f7bedd7ad614158095330da9258373e47d276c8c513e289baa92fa89de9d4cc7` |

## Interpretation

PASS means the release is canonical and executable for its declared screening purpose, with its numerical
physics proven identical to the immutable proposal. It does not mean the Tier-4 common-unit parameters are
calibrated, probabilistic, claims-validated or bankable.
