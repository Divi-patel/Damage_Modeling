# Tropical-cyclone wind × solar

## Current release

```yaml
cell_id: tropical_cyclone_wind_solar
pathway_id: tropical_cyclone_wind
documentation_lead: current model v2.1 / docs r2
damage_code_id: TROPICAL_CYCLONE_WIND_SOLAR_SCREENING_COMPLETE_V2_1
semantic_damage_model_version: model v2.1
documentation_revision: docs r2
lifecycle_state: released_v2_1
promotion_status: released
model_grade: screening_engineering_proxy_T4_coverage_complete
canonical_runtime_artifact: true
package_release: repository_current_not_in_portable_package
artifact_index_entry: model_v2_1_docs_r2_bundle_v3_exact_sha
current_pointer: current/
full_plant_physical_dr: supported_in_screening_mode
scenario_physical_loss: supported_with_named_value_profile
annual_and_tail_metrics: downstream_consumer_owned
```

Model v2.1 is current because it produces the requested end-to-end screening result. It retains the v2.0
array curves, adds numeric foundation, power/collection, GSU, SCADA, and civil curves, and assembles 100% of
a named physical replacement-value profile into plant physical DR and scenario loss.

It remains explicit Tier 4 where calibration is unavailable. The limitation is output grade—not output
absence. Promotion followed the owner-accepted Everglades M0→M4 experiment and exact dual-read parity.

## Delivered calculation

```text
qualified array demand ──> module + structure DR
qualified site demand  ──> foundation + power + GSU + SCADA + civil DR
named value profile    ──> same-unit losses
support-once rule      ──> total physical loss
                       └─> physical replacement DR
                           installed-capex physical loss fraction
                           scenario dollars when capacity is supplied
```

The primary runtime atom remains failure-unit DR. `physical_damage_assembly.v1` is an explicit convenience
view with a named denominator; it is not an untraceable whole-asset curve.

## Why this avoids the legacy defects

1. State probability and damage ratio remain separate; DR is `Σ P(state) × same-unit cost ratio`.
2. No physical value is silently treated as wind-immune. Every direct/civil value row has a numeric proxy.
3. Tracker calls require attained state and exact-system qualification; commanded stow is insufficient.
4. No anchored-logistic intercept subtraction is used.
5. GSU uses its own site-facility axis and value, not the array curve.

## Use it

Start with the [v2.1 request guide](../../extra/guides/tropical_cyclone_wind_solar_v2_1_curve_request_guide.md).
The runnable evaluator is
[`tropical_cyclone_wind_solar_v2_1_curve_eval.py`](../../../scripts/reference_helpers/tropical_cyclone_wind_solar_v2_1_curve_eval.py).

Key package files:

- [current package](current/README.md)
- [overview](current/README_tropical_cyclone_wind_solar__model_v2_1__docs_r2.md)
- [derivation dossier](current/tropical_cyclone_wind_solar_curve_derivation_dossier__model_v2_1__docs_r2.md)
- [metadata contract](current/tropical_cyclone_wind_solar_damage_code_metadata_spec__model_v2_1__docs_r2.md)
- [curve artifact](current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__curve_artifact.json)
- [capability](current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__capability.json)
- [known-answer tests](current/known_answer_tests_tropical_cyclone_wind_solar__model_v2_1__docs_r2.json)
- [full-plant curve table](current/FULL_PLANT_SCREENING_CURVE_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r2.csv)
- [workbook](current/damage_curve_records_tropical_cyclone_wind_solar__model_v2_1__docs_r2.xlsx)
- [validation report](current/VALIDATION_REPORT_tropical_cyclone_wind_solar__model_v2_1__docs_r2.md)
- [release decision](current/RELEASE_DECISION_tropical_cyclone_wind_solar__model_v2_1__docs_r2.md)
- [Hazard handoff](../../contracts/hazard_handoff/tropical_cyclone_wind_solar_model_v2_1_screening_proposal.md)

## Scope boundary

V2.1 delivers tropical-cyclone **wind-only physical damage**. Rain ingress, debris, surge/flood, and tornado
loss remain separately governed pathways. Frequency, EAL, PML, VaR, and TVaR remain Hazard-tier calculations;
BI and downtime remain a separate disruption stage.

## Version ladder

| Version | Role | Plant screening output | Status |
|---|---|---|---|
| model v2.1/docs r2 | coverage-complete screening release | numeric failure-unit DR, plant DR, loss per kWdc, optional dollars | current; canonical screening |
| model v2.1/docs r1 | first immutable promotion | same numerical output; stale noncanonical KAT status label | superseded by docs r2 |
| model v2.0/docs r1 | partial component research baseline | array component DR only; plant/value outputs withheld | preserved audit baseline |
| model v1.0/docs r2 human, r1 runtime | narrow Perry source-cohort alternative | one visible-module material proxy | noncanonical |
| model v0.1/docs r1 | strict evidence-only alternative | no runtime curve | fail closed |

V2.1 is canonical at screening grade after explicit owner acceptance, Hazard exact-pin integration checks,
and proposal-to-current dual-read/rollback coverage. These gates do not turn Tier-4 proxies into calibrated
physics or expand the wind-only scope.

## Historical and basics

- [model-v2.0 package](proposed/README_tropical_cyclone_wind_solar__model_v2_0__docs_r1.md)
- [model-v1 deep-curation record](proposed/README_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md)
- [strict model-v0.1 package](proposed/README_tropical_cyclone_wind_solar__model_v0_1__docs_r1.md)
- [physical idea](basics/README.md)
- [how the model is built](basics/HOW_THE_MODEL_IS_BUILT.md)
- [model reference](basics/MODEL_REFERENCE.md)
