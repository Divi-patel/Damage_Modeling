---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Proposed categorical BESS Wildfire response v0.1; explicit T4 transfers and selected consequence policy
---

# Derivation: categorical response and economic consequence

The target is the selected outdoor liquid-cooled LFP battery plant, with separate
PCS, no collector station/export, and direct physical hardware loss only.
BWF-Q01 selects **$1.05M integrated replacement after battery compromise**, with
repair sensitivities, for local tests. It does not approve a measured fragility,
class threshold, thermal propagation rate or annual result.

## One class axis; two different kinds of statement

The axis is the existing source-native FSim class, with exact states 1–6 and a
no-event control 0. A class is landscape severity, not measured equipment dose.
No flame midpoint, Byram-to-flux equation, duration assumption, operating-rating
threshold or interpolation between classes is introduced.

**Known compromised battery:** the selected economic consequence is $1.05M,
or100% of the same enclosure's hardware budget. This is not a forecast of how
frequently that state occurs.

**Class-conditioned forecast:** for a local screening hypothesis, use a
provisional ordinal mean-response weight `w_s` and a costed end-state `C_h`:

```text
enclosure conditional mean loss(s,h,k) = w_k(s) × C_h
enclosure DR(s,h,k) = w_k(s) × C_h / $1,050,000
PCS conditional mean loss(s) = d_PCS(s) × $520,000
```

These weights are economic mean-response proxies. **They are not measured
ignition or battery-compromise probabilities**, and no Bernoulli Damage-state
draws, intrinsic spread or propagation frequency is inferred. A lower repair
cost is a different economic interpretation that requires serviceable retained
hardware, not permission to repair known compromised cells.

## Source spine and transfer judgment

Use the pinned `wildfire_solar` v1.0/docs r3 electrical tables as ordinal templates:

| Exact state | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Electronics reference / PCS donor | 0 | .002 | .01 | .05 | .18 | .45 | .80 |
| Heavy-electrical enclosure sensitivity | 0 | .001 | .006 | .03 | .12 | .35 | .70 |

The donor's **absolute ordinates are already T4**, not observed failure rates.
Their BESS transfer is a **new analyst T4 hypothesis**, recorded as BWF-C13 and
BWF-P07/P09. The owner ruling supplies the consequence policy, not those weights.

Why this reference: an integrated battery enclosure contains enclosed electronic,
cooling, cable and polymer-bearing hardware that can suffer consequential thermal
damage. Reviewed OEM guidance supports external-flame initiation; the electrical
table provides a simple increasing screening template without a new fabricated
continuous dose axis. It does not establish equivalent construction or thermal
resistance. The heavier-equipment table tests a materially different, lower-response
interpretation for a more protected assembly, without claiming a measured protection
factor. Neither shape is selected because it produces a desired national number.

The manufacturer target-survival example constrains our reasoning: nearby fire
does not automatically destroy every enclosure. It supplies no class ordinate or
generic immunity. The observed spread counterexample likewise supplies no fitted
conditional probability. Those sources therefore remain **mechanism/endpoint
constraints**, not numeric calibration. See BWF-S03–S08 and the r1 source review.

Why not new detailed fragilities: the reviewed evidence does not support separate
cell/rack thermal thresholds or an external-fire-to-compromise distribution. Adding
those parameters would create precision without evidence. Keep one transparent
ordinal assembly hypothesis, a related PCS response and named alternatives. The
shape comparison is **not** a confidence interval or proven risk bound; actual
uncertainty can exceed it. A practical local hypothesis does not authorize a
calibrated, bankable or complete-property claim.

## Economic hypotheses

| Hypothesis | End-state cost | Required interpretation |
|---|---:|---|
| `approved_replacement` | $1,050,000 | Compromised battery contents require replacement of the integrated enclosure under BWF-Q01. |
| `noncell_repair_sensitivity` | About $334,395 | Cells are serviceable; replace all related non-cell groups. |
| `limited_repair_sensitivity` | About $204,352 | Cells and BMS are serviceable; replace cooling and the enclosure/rack/safety group. |

The latter costs come from the earlier related MMP benchmark allocation projected
onto the same $84M enclosure budget. They are not an OEM quote, verified repair
method, salvage allowance or detailed wildfire repair BOM. Runtime must request
the serviceability **counterfactual** explicitly for either repair sensitivity.
The baseline and sensitivities share the same class weight only to isolate the
cost-policy effect; this does not establish equal true damage-state likelihood.
No probabilities are assigned across shape or cost hypotheses; do not average them.

All seven numerical records are exact-state tables. The existing v3 schema's
`piecewise_linear` container carries those knots, as in the current Wildfire Wind
cell. The admitted domain contains only exact integers0..6: the evaluator never
executes interpolation. A generic continuous evaluator is not an eligible consumer.
No schema field or existing cell is changed to accommodate this candidate.

## Seven-step and value audit

| Step | Current result | Limit |
|---|---|---|
| 1. Boundary | Selected100MW/400MWh usable-AC outdoor LFP, 450MWh DC, $109.8M fixed 2024 physical value | Engineering reference, not an observed fleet or appraisal. Autonomous failures, BI/performance and external collector/export are outside. |
| 2. Failure units | Integrated enclosure and separate PCS | Cell/rack independence and unit-MV/civil curves are not invented. |
| 3. Y-axis | Same-unit conditional mean physical repair/replacement cost divided by same-unit hardware value | Safety isolation, ignition, availability and revenue are different endpoints. |
| 4. Value rows | Ten rows reconcile:$109.8M retained and $23.4M outside | Mixed physical rows stay explicit. |
| 5. Allocation | 80×$1.05M enclosure +20×$520k PCS =$94.4M candidate hardware | $15.4M residual stays unbound; no renormalization to full TIV or repeated internals. |
| 6. Site exposure | Declared local FSim class; no blanket mitigation or exposed-share default | Yard transfer, unit footprint/dependence, source gaps and original placement weights belong to the later consumer proof. |
| 7. Conditional response | Proposed opt-in scalar means with independent source/cost controls | Unreleased; annual metrics and full-property loss remain withheld. |

The $13.2M unit-MV/shared electrical row, $1.6M civil and $0.6M fieldwork are retained
in the denominator but not damaged by these two curves. Fieldwork is a once-only
repair allocation, not another vulnerability curve. A support row cannot receive
its own DR and also be charged in hardware replacement. Exposed cable shares and
component values are not silently assigned one or copied from a full GSU.

## Site-condition and double-counting controls

The r1 intake's site matrix remains applicable. No clearance/fence/gravel/barrier,
enclosure rating, suppression, detection or response credit is quantified here.
Do not combine a protected archetype and another discount for the same mechanism.
Source BP stays in Hazard; passing it to this Damage reader is rejected. Unknown
class is unavailable, never the no-event control. Internal thermal consequence is
included in the selected unit-replacement endpoint where hypothesized; additional
cross-unit spread is unquantified and cannot be added again for the same hardware.
Autonomous fire needs its own excluded initiating population.

## Consumer capability and next evidence

Explicit local-test opt-in, exact SHA pins, native state, reference selector,
policy, shape and same-unit value are mandatory. Repair requires its explicit
serviceability counterfactual. Unsupported units/pathways emit null, not a curve
borrowed from a neighboring hazard. No default shape/policy or uncertainty percentile
is selected. Conditional means carry no intrinsic Damage uncertainty distribution.

Annual EAL/PML/VaR/TVaR, canonical runtime admission, national risk and complete-property
metrics are withheld. Hazard must separately prove source/footprint coupling,
joint screening dependence, original unknown mass, per-unit annual caps and tails.
The candidate comparison cannot be reported as annual loss or burn probability.

Actionable improvements are retained under Hazard BR-24–BR-26: matched external
exposure/duration and inspected repair costs; full manufacturer test reports and
configuration; yard/fuel transfer and actual fire footprints; propagation; mixed
electrical values and once-only support. Reopen the relevant hypothesis when that
evidence changes its endpoint or class response. No unlimited repeat search is
required for this bounded local test, and no complete/calibrated claim can bypass
its missing proof by calling that proof future work.
