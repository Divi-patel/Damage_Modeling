# Change classification — tropical-cyclone wind × solar model v2.1

```yaml
change_class: CONTRACT_STATUS_METADATA_FIX
cell_id: tropical_cyclone_wind_solar
operating_mode: inside_repo
outputs_can_change_for_same_inputs: false
prior_current: model v2.1 / docs r1
new_release: model v2.1 / docs r2
primary_workflow: 01_workflows/UPDATE_EXISTING_CELL_WORKFLOW.md
schema_events:
  curve_bundle: damage_curve_record_bundle.v3 unchanged
  damage_emit: damage_emit.v2 unchanged
  companion_assembly: physical_damage_assembly.v1 unchanged
version_impacts:
  package_release: unchanged_unreleased
  cell_model_version: unchanged_model_v2_1
  docs_revision: docs_r1_to_docs_r2
  canonical_index: replace_model_v2_1_docs_r1_with_docs_r2
required_gates:
  - old_vs_new_behavior_comparison
  - complete_failure_unit_and_value_coverage
  - scenario_loss_reconciliation
  - JSON_and_companion_schema_QA
  - known_answer_and_rejection_tests
  - exact_pin_verification
  - proposal_to_canonical_dual_read_parity
  - owner_screening_acceptance
```

The v2.1 model behavior was introduced in docs r1: v2.0 returned only array-component DRs and prohibited
plant physical DR and scenario loss, while v2.1 added explicitly synthetic common-unit screening curves and
the complete named physical replacement-value assembly. Docs r2 does not change that behavior. It replaces
the inherited `NONCANONICAL_MODEL_V2_1` KAT/output label with `CANONICAL_SCREENING_RELEASE` and updates the
exact canonical pin; all numerical results remain identical.
