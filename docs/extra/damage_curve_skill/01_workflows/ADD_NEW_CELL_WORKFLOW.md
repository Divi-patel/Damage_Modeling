# Add new cell workflow

Use for a new hazard × asset pair. A new physical profile alone does not automatically create a new cell.

## Before Phase 0 — new-asset intake when needed

For a new asset family or detailed twin, use
[illustrative asset intake and reuse](../02_design_guides/ILLUSTRATIVE_ASSET_INTAKE_AND_REUSE.md).
Resolve scope, response grain, existing reuse candidates and the Hazard–Damage interface before choosing
cell identity. Link its worksheet from the scope dossier; do not duplicate established cell registers.

## Phase 0 — classify and name

```text
[ ] cell_id chosen: <hazard>_<asset>
[ ] hazard scope defined
[ ] asset scope defined
[ ] related hazards that should split are listed
[ ] initial cell state chosen: scaffold, draft, or release candidate
```

Do not call the cell `model v1.0` unless the runtime curve artifact is ready.

For a proposed artifact stored in the repository but not released in a package, record:

```yaml
package_release: unreleased
package_baseline: library vX.Y
package_inclusion_status: not_included
canonical_runtime_artifact: false
```

Repository presence supports review; it does not promote runtime/package status.

## Phase 1 — scope dossier

Apply [bounded curation and future research](../02_design_guides/BOUNDED_CURATION_AND_FUTURE_WORK.md).
Set the current deliverable and a materiality-based search checkpoint. Preserve
useful deferred discoveries as they arise, with exact evidence, current treatment,
reopening trigger and next acceptance check; link the existing registers.

Create a cell README and scope note that answer:

```text
What damage mechanisms are in v1?
What mechanisms are explicitly deferred?
What is the hazard axis candidate?
What asset metadata matters?
Which failure units are plausible?
Which value buckets are implicated?
```

## Phase 2 — failure-unit selection

Use `02_design_guides/FAILURE_UNIT_SELECTION.md`.

Output table:

| Failure unit | Subsystem | Component | Role | Reason | Value bucket | v1 treatment |
|---|---|---|---|---|---|---|

Roles:

```text
primary_nonzero
secondary_nonzero
conditioner_only
exposure_only
reviewed_DR_near_zero
out_of_scope_deferred
```

## Phase 3 — axis and curve form

Use:

```text
02_design_guides/X_AXIS_SELECTION.md
02_design_guides/CURVE_FORM_SELECTION.md
02_design_guides/HAZARD_PATHWAY_SPLITTING.md
```

Record alternatives and rejected options.

## Phase 4 — evidence and parameter tiers

Use:

```text
01_workflows/EVIDENCE_INGESTION_WORKFLOW.md
02_design_guides/PARAMETER_TIER_AND_RATIONALE.md
```

Create:

```text
source register with exact locators and transfer limits
claim-level provenance register
source-to-parameter map
parameter tier table
derivation rationale
evidence pressure test
legacy numerical audit, when legacy material exists
open seams/update triggers
```

Use `02_design_guides/EVIDENCE_PRESSURE_TEST_AND_FAIL_CLOSED_CHECKLIST.md`. Reproduce proposed equations and tables before adopting them. A source can support a mechanism without supporting a converter, threshold, curve ordinate, economic endpoint, or whole-asset transfer.

## Phase 5 — value crosswalk

Use `02_design_guides/VALUE_CROSSWALK_GUIDE.md`.

Map each failure unit to engineering substrate and value workbook buckets. If no value bucket exists, create an explicit placeholder and update trigger.

The crosswalk must reconcile every material row and distinguish direct vulnerable value, mixed rows, support/logistics allocated once, and excluded soft/sunk/nonphysical value. Unknown at-risk or exposure shares do not default to one.

## Phase 5A — seven-step and site-condition audit

Complete `templates/TEMPLATE_SEVEN_STEP_AUDIT.md`:

```text
1. define the asset and boundary;
2. decompose into failure units;
3. choose the y-axis and value basis;
4. split the value basis row by row;
5. allocate physical value by failure unit and zone;
6. specify site-condition exposure logic;
7. apply qualified curves and reconcile loss, or withhold.
```

When site conditions can materially change delivered demand or affected value, also complete `templates/TEMPLATE_SITE_CONDITION_ADAPTER.md`. Include fences, walls, barriers, vegetation/fuels, protection, access/response, and bypass pathways when applicable. Include a double-counting matrix and assign no blanket mitigation credit.

## Phase 6 — artifact creation

Create or populate:

```text
README_<cell>__model_<...>__docs_<...>.md
<cell>_curve_derivation_dossier__model_<...>__docs_<...>.md
<cell>_damage_code_metadata_spec__model_<...>__docs_<...>.md
<cell>__model_<...>__docs_<...>__curve_artifact.json
workbook or derivation/audit view, if useful
previews, if workbook/dashboard exists
```

If no curve passes the evidence chain, a proposed non-canonical artifact may preserve scope, inputs, evidence, and `curve_records: []`. Rejected or withdrawn numeric arrays belong only in a labeled audit memo/workbook, not in runtime-shaped curve records.

## Phase 7 — capability declaration

Every new cell, even a scaffold, needs a capability stance.

For scaffold/draft:

```text
failure_unit_scalar_dr: withheld
scenario_loss: withheld
scalar_eal: withheld
pml/var/tvar: withheld
standard_reason: NO_RUNTIME_CURVE
```

For released v1.0:

```text
failure_unit_scalar_dr: supported if deterministic curves are complete
scenario_loss: supported only with explicit value/exposure basis
scalar_eal: conditional unless distribution and cap-binding gates pass
scalar_eal reason while conditional: CAP_BINDING_PREFLIGHT_NOT_EXECUTED
pml/var/tvar: withheld unless the downstream annual loss distribution and metric-specific gates are qualified
```

Curve-intrinsic spread and an annual loss distribution are different objects. A deterministic
DR(intensity) can feed a stochastic hazard-event/year calculation. Damage must state whether it carries
intrinsic spread; Hazard owns frequency, spatial coupling, annual composition and tail calculation.
Do not fabricate curve spread to unlock tails, and do not override an existing cell's explicit annual
withholding merely because a downstream distribution can be constructed. Follow
[the capability rules](../03_contracts/CAPABILITY_DECLARATION.md).

## Phase 8 — validation and release

Use `04_validation_qc/VALIDATION_QC_GUIDE.md` and `05_release/PACKAGE_ASSEMBLY_GUIDE.md`.

Minimum release outputs:

The closeout also identifies the supported baseline and its actionable future-work
entries. An unresolved required proof remains a capability restriction, even if
it is recorded for later work; an optional refinement does not block the baseline.

```text
VERSION_REGISTRY updated
machine_readable_artifact_index updated if runtime artifact exists
MANIFEST updated
CHANGED_FILES updated
VALIDATION_REPORT added
release note added
```

For a no-curve scaffold, known-answer tests must assert that valid inputs emit no numeric DR or loss and return `NO_RUNTIME_CURVE`. A smooth provisional curve is not a required scaffold output.
