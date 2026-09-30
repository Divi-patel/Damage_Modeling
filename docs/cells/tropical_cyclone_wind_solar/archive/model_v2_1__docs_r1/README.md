# Tropical-cyclone wind × Solar current — model v2.1/docs r1

> **Canonical coverage-complete screening release · 2026-08-30.** The exact proposed curve/value physics
> passed the Everglades M0→M4 experiment and proposal-to-current dual-read tests before promotion.

```text
qualified fixed/tracker array demand
                  +
qualified site-facility wind demand
                  +
named physical replacement-value profile
                  ↓
ten failure-unit screening DRs
                  ↓
plant physical replacement DR + loss per kWdc
                  ↓
Hazard-owned frequency, EAL and PML
```

This is a screening release, not a claims-calibrated or bankable model. The additional site-facility curves
remain explicit Tier-4 engineering proxies; the central scenario is the headline, while the lower/upper
resistance scenarios are a nonprobabilistic epistemic envelope. Rain, debris, surge/flood and tornado are
outside this wind-only cell.

## Package

- [curve artifact](tropical_cyclone_wind_solar__model_v2_1__docs_r1__curve_artifact.json)
- [capability declaration](tropical_cyclone_wind_solar__model_v2_1__docs_r1__capability.json)
- [known-answer tests](known_answer_tests_tropical_cyclone_wind_solar__model_v2_1__docs_r1.json)
- [full-plant curve table](FULL_PLANT_SCREENING_CURVE_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv)
- [value crosswalk](VALUE_CROSSWALK_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv)
- [workbook](damage_curve_records_tropical_cyclone_wind_solar__model_v2_1__docs_r1.xlsx)
- [derivation dossier](tropical_cyclone_wind_solar_curve_derivation_dossier__model_v2_1__docs_r1.md)
- [validation report](VALIDATION_REPORT_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md)
- [release decision](RELEASE_DECISION_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md)

The immutable `proposed/` v2.1 artifact remains the rollback and numerical-parity reference. Consumers must
pin this current artifact by model, docs revision, schema and SHA; the portable library remains v2.5.
