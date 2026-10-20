# Capability declaration

Every cell must machine-declare which metrics it can support.

## Required block

```yaml
capability_declaration:
  schema_version: <governed_capability_schema_after_review>
  cell_id:
  spread_carried: true | false
  emit_modes_populated_by_cell:
    - scalar_mean
  pathway_unit_support:
    - pathway_id:
      failure_unit_id:
      status: supported | conditional | withheld
      reason_codes: []
      curve_ids: []
  metrics_supportable:
    failure_unit_scalar_dr: supported | conditional | withheld
    scenario_loss_given_value_basis: supported | conditional | withheld
    scalar_eal: supported | conditional | withheld
    pml: supported | conditional | withheld
    var: supported | conditional | withheld
    tvar: supported | conditional | withheld
  metric_reason_codes:
    failure_unit_scalar_dr: []
    scenario_loss_given_value_basis: []
    scalar_eal: []
    pml: []
    var: []
    tvar: []
  cap_binding:
    policy: pass_required | fail_closed | not_applicable
    preflight_status: pass | fail | not_executed_no_distribution | not_executed_no_value_basis
    required_before_scalar_eal: true | false
    tolerance_pct:
    action_if_fail:
```

## Support rules

| Metric | Rule |
|---|---|
| Failure-unit scalar DR | Supported when deterministic failure-unit curves exist for the requested inputs |
| Scenario loss | Supported only with explicit value and exposure basis |
| Scalar EAL | Conditional unless frequency layer, value basis, and cap-binding preflight pass |
| PML/VaR/TVaR | Withheld unless a qualified downstream annual loss distribution or equivalent tail-supporting object exists and the applicable capability permits that use |

Distinguish **curve-intrinsic spread** from the **annual loss distribution**. Deterministic damage ratios
can feed a stochastic hazard-event/year model; missing curve spread alone does not make downstream tail
metrics mathematically impossible. Damage declares response support and uncertainty; the consumer owns
frequency, coupling, annual composition and metric validation. Existing explicit annual withholding remains
binding until its governed promotion gates pass. Do not fabricate spread or unlock metrics through prose.

This guide describes the support concepts. The cell's released schema and capability are the runtime
authority; this illustrative block does not migrate existing capability versions.

Keep the support state machine-readable and finite: `supported`, `conditional`, or `withheld`. Put the condition or withholding explanation in `metric_reason_codes`, for example `MISSING_VALUE_BASIS`, `MISSING_HAZARD_FREQUENCY`, `CAP_BINDING_PREFLIGHT_NOT_EXECUTED`, `NO_TAIL_DISTRIBUTION`, or `NO_RUNTIME_CURVE`. Do not encode prose conditions into new status strings.

## Default v1 stance

```text
failure-unit DR: supported if curve exists
scenario loss: conditional, reason MISSING_VALUE_BASIS until explicit basis exists
scalar EAL: conditional, reason CAP_BINDING_PREFLIGHT_NOT_EXECUTED until gate passes
PML/VaR/TVaR: withheld, reason NO_TAIL_DISTRIBUTION
```

For a scaffold with no runtime curve, every metric is `withheld` with `NO_RUNTIME_CURVE` taking precedence for DR and dependent loss metrics.

## Multi-pathway rule

Cell-level metric support is insufficient when coverage differs by mechanism. Add a rectangular pathway × failure-unit support matrix. Every declared pair must be present exactly once, including immune/near-zero units when they are intentionally modeled.

```text
supported   -> one or more governed curve IDs resolve for the pair;
conditional -> the named gate is machine-checkable and no number appears until it passes;
withheld    -> no numeric DR and a stable reason code;
```

Do not report the cell as globally supported if the requested pair is withheld. Use `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` for a missing pair in an otherwise partly supported cell. Unknown or missing `pathway_id` fails closed and never selects the first/supported pathway.
