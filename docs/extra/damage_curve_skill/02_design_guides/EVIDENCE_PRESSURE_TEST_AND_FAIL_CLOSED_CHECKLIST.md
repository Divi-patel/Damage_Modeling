# Evidence pressure test and fail-closed cell checklist

Use this guide for every new hazard × asset cell and whenever legacy research, a proposed converter, or a numerical curve is being reconsidered. It turns the main lessons from the controlled `wildfire_solar` scaffold into a hazard-neutral workflow.

The goal is not to force a curve into existence. The goal is to determine whether a curve is supportable at the declared failure-unit, exposure, and value grain. A fully governed `NO_RUNTIME_CURVE` result is a valid and often preferable research outcome.

## The seven-step audit

Complete all seven steps in order. Record a status and blocking seam for each step.

### 1. Define the asset and boundary

```text
[ ] asset archetype and reference capacity/configuration are named;
[ ] value vintage and geography are named;
[ ] included physical boundary is explicit;
[ ] BI, revenue, insurance terms, land, soft/sunk value, and deferred hazards are explicit;
[ ] the archetype is not presented as a site appraisal.
```

### 2. Decompose into failure units

```text
[ ] each materially different failure mechanism has its own candidate failure unit;
[ ] protected/exposed and materially different BOM states are split or flagged;
[ ] pathway controls are not mislabeled as vulnerable components;
[ ] every material value row has a candidate treatment;
[ ] the curve count is not precommitted before coverage reconciliation.
```

### 3. Choose the y-axis and value basis

Define the numerator, denominator, conditioning state, and exclusions in one equation. Prefer same-unit direct replacement cost for a physical failure-unit curve unless a different basis is intentionally governed.

```text
DR_u(s) = E[direct replacement cost of failure unit u
            / pre-event direct replacement value of the same failure unit u
            | delivered local exposure state s, construction/protection state]
```

Do not silently substitute whole-site installed TIV, insured value, gross claims, net claims, or BI.

### 4. Split the value basis row by row

```text
[ ] direct vulnerable hardware is separated from civil/support/logistics;
[ ] mixed rows are split or remain unresolved;
[ ] excluded soft/sunk/nonphysical rows are named;
[ ] every workbook row reconciles to one treatment;
[ ] support costs do not receive an independent component DR.
```

### 5. Allocate physical value

Allocation must preserve failure-unit and spatial grain.

```text
[ ] failure-unit value reconciles to the source value rows;
[ ] exposed/protected or at-risk shares have a measured basis;
[ ] spatial zones and burned/attacked shares are separately defined;
[ ] unknown at-risk or attack fractions do not default to one;
[ ] support/logistics are allocated once after direct damage is known.
```

### 6. Build the site-condition exposure adapter

Separate fixed asset selectors, event/maintenance conditioners, site-transfer inputs, derived exposure, and value allocation. A coarse hazard intensity or probability product is not automatically component demand.

For any fence, wall, firebreak, berm, vegetation treatment, enclosure, burial, suppression system, or access provision:

```text
[ ] construction/material, geometry, continuity, condition, and maintenance date are captured;
[ ] bypass pathways are considered;
[ ] a control can be harmful, neutral, or protective depending on conditions;
[ ] guidance or code language is not converted into an efficacy coefficient;
[ ] unknown mitigation receives no credit;
[ ] the same mechanism is not applied in both exposure and vulnerability/value allocation.
```

A fence or wall never receives blanket credit. Examples of required questions include whether a combustible fence is a fuel path, whether an open fence provides no meaningful radiant shielding, whether a solid barrier has gaps or line-of-sight bypass, whether accumulated fuel defeats it, and whether embers or floodwater/debris/wind can bypass it for the hazard under review.

### 7. Apply curves and reconcile loss—or withhold

Activate a numerical curve only after the full chain is supported:

```text
source-native hazard state
  -> local delivered exposure at the failure unit
  -> construction-specific failure/inspection/replacement state
  -> same-unit direct replacement-cost ratio
  -> support-cost allocation once, outside the curve ordinate
```

If any load-bearing link is absent, use the cell capability declaration to withhold the output. Do not lower an unsupported curve merely to make it look conservative.

## Mandatory evidence controls

### Source register

Every source receives a stable ID, exact citation/URL, exact locator, role, canonical evidence tier, applicability statement, permitted inference, prohibited inference, and adoption decision. A bibliography without these fields is not a source register.

### Claim-level provenance

Every load-bearing scientific, engineering, numerical, regulatory, and governance claim receives a claim ID. Link it to one or more source IDs and exact locators. Distinguish:

```text
direct observation
source interpretation
engineering inference
governance decision
unresolved hypothesis
```

Do not cite a document as support for a stronger endpoint than it measured. Ignition is not functional failure; functional failure is not replacement; component replacement is not whole-site economic DR.

### Bounded negative-evidence claims

If a decision depends on “no dataset/source was located,” create a bounded evidence-search log. Record the review cutoff, search surfaces, query families and variants, target endpoint chain, inclusion/exclusion rules, results by missing link, scope limitations, and update triggers. Link the claim register to that exact log section. A search log supports only absence within its recorded scope, never universal nonexistence.

### Parameter tiers

Use only the canonical labels:

```text
T1_claims_or_field_calibrated
T2_public_lab_standard_or_physics
T3_engineering_proxy_or_adjacent_empirical
T4_placeholder_or_expert_judgment
```

Each load-bearing parameter, default, disabled-credit rule, and open placeholder must have source IDs, reasoning, status, and an update trigger.

### Legacy numerical audit

Legacy material is input, not authority. Before reusing any number or formula:

```text
[ ] retrieve and pin the exact source/version/blob where possible;
[ ] reproduce every displayed equation at boundary and table points;
[ ] check units, inverse conversions, signs, intercepts, asymptotes, and zero-input behavior;
[ ] compare formula output with every displayed table/chart;
[ ] identify the measured endpoint and target population;
[ ] verify the citation identity and exact locator;
[ ] distinguish source-derived values from analyst assumptions;
[ ] record retain, re-source, demote, reject, or defer for each item.
```

A formula that contradicts its own table is rejected even before external calibration is considered. A plausible mechanism does not rescue an uncalibrated economic curve.

### Tests, interventions and the economic endpoint

When laboratory tests or equipment safety reports support a proposed response,
reconstruct the timeline before treating a result as a curve anchor:

- Separate the specified test protocol, actual exposure, observed response and
  economic repair decision. A protection rating or prescribed two-hour test is
  not an observed survival result, and survival of a fire criterion is not zero
  physical damage.
- Record post-test soaking, discharge, disassembly or other treatment before
  inspection. Damage photographed after extended treatment cannot be attributed
  quantitatively to a shorter initial challenge without additional evidence.
- Record interventions and stopping rules. Re-immersion at first smoke censors
  later thermal severity; it cannot establish either inevitable escalation or
  absence of escalation without that intervention.
- Do not fit a failure probability from a small set of heterogeneous units,
  salinities, exposure times and stopping rules as though they were repeated
  trials of one target configuration.
- Preserve the tested unit and endpoint. An automotive pack can inform utility
  battery mechanisms without establishing a utility enclosure repair ratio.

Use the existing source/claim/parameter registers for these checks; no extra
folder or mandatory document is needed. If a sensitivity experiment compares
unqualified repair interpretations, label them as hypotheses, not a confidence
interval or a mean to be obtained by averaging. The BESS Flood immersion review
is a worked application in `docs/extra/discussion/bess_damage/` when operating
inside this repository; the rules above also apply to standalone skill packages.

### Pressure testing and overestimation controls

Pressure tests must use explicit denominators and must be labeled as audit arithmetic when inputs are withdrawn or synthetic.

```text
[ ] convert proposed DRs to dollars on same-unit, direct-hardware, and broader physical bases where informative;
[ ] show how whole-site exposure or a default exposure fraction changes the result;
[ ] isolate support/civil/logistics so they are not scaled twice;
[ ] test zero hazard, lower/upper valid bounds, and asymptotic behavior;
[ ] test alternative source interpretations and unit conversions;
[ ] prohibit synthetic probability vectors from becoming reportable scenarios;
[ ] reject unsupported uncertainty bands rather than calling them conservative.
```

Conservatism is not always a lower damage number. The defensible action is to withhold when the calibration chain is missing.

## Site-condition double-counting matrix

Every adapter must include a matrix with at least these columns:

| Related fields or controls | Single governed treatment | Prohibited double count | Missing/default behavior |
|---|---|---|---|
| fuel/terrain/geometry inputs and derived exposure | Inputs feed one transfer model; the result feeds vulnerability. | Reapply input discounts after using the derived exposure. | Withhold if load-bearing. |
| barrier construction/geometry and attenuation result | Either derive delivered exposure or select a qualified protected archetype. | Apply both a barrier discount and the derived/protected response for the same effect. | No credit without a qualified model. |
| protected/exposed installation and at-risk allocation | Partition value first; apply the relevant pathway to that partition. | Reduce the same share again in vulnerability. | Unknown share does not default to fully exposed. |
| response/access/suppression controls | One event-response model determines any duration/spread change. | Stack independent credits for one intervention chain. | No credit without event availability and response evidence. |
| direct damage and support/logistics | Apply direct same-unit DR; allocate support once afterward. | Give support rows their own DR and also scale them with direct loss. | Withhold total physical loss if allocation is unresolved. |

Add hazard-specific rows; this is a minimum, not a complete matrix.

## Required machine/reportability outcome

A scaffold with no qualified runtime curve must be internally and externally consistent:

```yaml
curve_records: []
canonical_runtime_artifact: false
failure_unit_scalar_dr: withheld
scenario_loss: withheld
scalar_eal: withheld
pml: withheld
var: withheld
tvar: withheld
standard_reason: NO_RUNTIME_CURVE
```

Remove rejected numeric arrays from runtime-shaped artifacts. Preserve them only in a clearly labeled audit memo or workbook. Known-answer tests for a scaffold must assert that valid inputs still produce no numeric DR or loss.

## Minimum evidence package

```text
[ ] seven-step audit;
[ ] source register;
[ ] claim/parameter provenance register;
[ ] every governed CSV register is rectangular, with no missing or extra row fields;
[ ] bounded evidence-search log when a negative-evidence claim is load-bearing;
[ ] parameter-tier table;
[ ] legacy evidence ingestion/audit memo when legacy material exists;
[ ] site-condition adapter and double-counting matrix;
[ ] row-level value crosswalk;
[ ] pressure-test memo;
[ ] capability declaration identical wherever embedded or standalone;
[ ] no-curve known-answer tests when curve_records is empty;
[ ] validation report recording every withheld gate.
```

Use the templates in `../templates/` and the controlled example in `../06_examples/EXAMPLE_FAIL_CLOSED_WILDFIRE_SOLAR_SCAFFOLD.md`.

For a multi-pathway cell, complete the evidence package at pathway grain. Populate `pathway_ids` / `pathway_id` in source, claim, parameter-tier, and value-crosswalk registers; do not let a source or parameter adopted for one mechanism silently qualify another. A row may use `all_shared` only when the same asset/value fact genuinely applies to every declared pathway. Apply `NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT` when the evidence chain fails for one pathway × failure-unit pair while other pairs remain supportable.
