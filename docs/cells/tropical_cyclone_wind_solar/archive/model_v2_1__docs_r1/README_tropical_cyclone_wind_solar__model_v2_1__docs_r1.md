# Tropical-cyclone wind × solar — model v2.1 / docs r1

> **Outcome:** owner-approved, coverage-complete canonical screening release.
> Numeric plant physical DR and scenario loss are delivered. The model remains
> explicitly Tier-4 where calibration is absent.

## What changed from v2.0

V2.0 was a partial component experiment. V2.1 keeps its defensible array records and adds what the requested
use case needs:

- numeric foundation, power/collection, GSU, SCADA, and civil screening curves;
- 100% coverage of a named 877.7957023626668 USD/kWdc physical replacement profile;
- support cost allocated exactly once;
- plant physical DR, installed-capex physical loss fraction, loss per kWdc, and optional scenario dollars;
- a runnable full-plant request and machine schema.

V2.1 does **not** resurrect the legacy defects: probability and DR remain different quantities, absent evidence
does not become zero, tracker state must be attained and qualified, and no intercept-shifted logistic is used.

## Use it

Start with the [v2.1 request guide](../../../../extra/guides/tropical_cyclone_wind_solar_v2_1_curve_request_guide.md).
Machine truth is the
[curve artifact](tropical_cyclone_wind_solar__model_v2_1__docs_r1__curve_artifact.json), accompanied by the
[capability declaration](tropical_cyclone_wind_solar__model_v2_1__docs_r1__capability.json),
[known-answer tests](known_answer_tests_tropical_cyclone_wind_solar__model_v2_1__docs_r1.json), and
[workbook](damage_curve_records_tropical_cyclone_wind_solar__model_v2_1__docs_r1.xlsx). The
[full-plant curve table](FULL_PLANT_SCREENING_CURVE_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv)
provides all 246 fixed/tracker × resistance-scenario points from demand ratio 0.00 through 2.00.

## Governance

- [change classification](CHANGE_CLASSIFICATION_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md)
- [decision log](DECISION_LOG_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md)
- [derivation dossier](tropical_cyclone_wind_solar_curve_derivation_dossier__model_v2_1__docs_r1.md)
- [metadata contract](tropical_cyclone_wind_solar_damage_code_metadata_spec__model_v2_1__docs_r1.md)
- [old-vs-new table](OLD_VS_NEW_COMPARISON_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv)
- [validation report](VALIDATION_REPORT_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md)
- [release decision](RELEASE_DECISION_tropical_cyclone_wind_solar__model_v2_1__docs_r1.md)
