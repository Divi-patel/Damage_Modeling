# Change classification — tropical-cyclone wind × solar model v2.1

```yaml
change_class: MODEL_BEHAVIOR_CHANGE
cell_id: tropical_cyclone_wind_solar
operating_mode: inside_repo
outputs_can_change_for_same_inputs: true
prior_proposal: model v2.0 / docs r1
new_release: model v2.1 / docs r1
primary_workflow: 01_workflows/UPDATE_EXISTING_CELL_WORKFLOW.md
schema_events:
  curve_bundle: damage_curve_record_bundle.v3 unchanged
  damage_emit: damage_emit.v2 unchanged
  companion_assembly: physical_damage_assembly.v1 added
version_impacts:
  package_release: unchanged_unreleased
  cell_model_version: minor_bump_v2_0_to_v2_1
  docs_revision: new_docs_r1_for_v2_1
  canonical_index: add_model_v2_1_docs_r1
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

The behavior change is deliberate: v2.0 returned only array-component DRs and prohibited plant physical DR
and scenario loss. v2.1 preserves those array curves, adds explicitly synthetic common-unit screening curves,
and assembles the complete named physical replacement-value profile.
