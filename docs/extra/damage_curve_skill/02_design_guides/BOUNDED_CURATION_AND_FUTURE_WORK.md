# Bounded damage-curve curation and future research

Use when adding a cell or materially reconsidering its evidence, assumptions or
coverage. The output has two linked parts: the best justified response for the
agreed scope now, and enough retained research to make later improvement efficient.
Use the existing dossier and registers; a new document is not mandatory.

## 1. Set the deliverable before searching

State the target asset/configuration, initiating hazard, affected physical units,
loss denominator, intended consumer use and material excluded mechanisms. Identify
which facts could change the result and set a bounded search/checkpoint around
those facts. Do not expand into every possible failure mode merely because the
twin contains it.

Separate the initiating event from its consequences. A natural hazard may trigger
an internal short or fire; those can belong to that event's damage response.
An autonomous defect-induced fire needs its own initiation/frequency treatment
outside a natural-hazard-only assignment. The same mechanism name does not make
the two event populations interchangeable. Follow the consumer's declared scope;
this is not a blanket prohibition on research for autonomous failures.

## 2. Choose the simplest justified current response

Inspect qualified reuse before deriving new behavior. Use the existing source and
claim registers to compare configuration, demand axis, endpoint, exposure and value
membership. Adopt a fit-for-purpose baseline with evidence, reasoning, uncertainty
and explicit capability. Engineering assumptions are acceptable only under the
applicable tier and admission rules, with their basis and intended use stated.

“Reasonable” does not mean taking the midpoint of incompatible estimates, assuming
optimism and pessimism cancel, or inventing numbers to fill missing coverage.
Distinguish a central estimate from a conservative bound and a sensitivity case.
Where a parameter is material and weakly known, compare a small number of meaningful
alternatives; do not require an elaborate probabilistic model without evidence.

At the agreed checkpoint, conclude with a qualified baseline, a qualified partial
response, or `NO_RUNTIME_CURVE`. Explain what can be delivered now and the specific
missing evidence that would change it. A research gap is not automatically a blocker
for unaffected units or pathways; a required unsupported capability stays withheld.
Do not restart a broad search when only one denominator or transfer assumption is
unresolved.

## 3. Preserve discoveries while curating

Update a future-research register during the search, not from memory at closeout.
Link exact source/claim IDs, pages/tables, files, calculations, failed access
attempts and rejected alternatives already recorded in the authoritative evidence
store. Do not duplicate source registers or fill the backlog with generic wishes.

Use or adapt these fields in the existing register:

| Field | What makes the entry actionable |
|---|---|
| Stable ID and affected scope | Pathway, failure unit, configuration and consumer metric |
| Current treatment | Adopted assumption/response, partial coverage, excluded scope or withheld capability |
| Discovery and evidence | What was learned; source IDs/locators and calculations; what remains unverified |
| Why deferred | Outside agreed scope, low materiality, missing data, or excessive complexity relative to current benefit |
| Expected benefit | Which bias, coverage gap, decision or intervention becomes testable; magnitude if measured |
| Reopening trigger | Specific new dataset, configuration, material sensitivity, user need or admission prerequisite |
| Next action and acceptance check | First concrete research/implementation step and what would qualify the change |
| Owner/priority/state | Named role, relative priority and deferred/blocked/adopted/superseded state |

Distinguish a **future enhancement** from **missing evidence needed for a requested
current claim**. Deferring an enhancement does not delay a qualified baseline;
deferring a required proof does not authorize that claim. Preserve the current
reference and version, and link a later promotion back to the entry.

## 4. Close with two clear outputs

Report the current response, assumptions, source support, boundaries and tests;
then the actionable deferred items. State which cell/model/docs/schema versions
changed and which capabilities did not change. Keep numerical admission under the
existing cell workflow; this curation practice grants no new release permission.

Examples of the distinction:

- A source matches the current enclosure and flood endpoint; detailed rack-level
  replacement would only support a future intervention. Use the qualified current
  response and retain that refinement with its evidence and trigger.
- An enclosure fire test measures propagation but has no annual initiation rate.
  Keep it as conditional-mechanism evidence; do not derive an annual fire loss by
  borrowing a landscape-wildfire frequency. Record the exact missing rate basis.
- A related transformer curve is usable, while the battery units remain unsupported.
  A labeled partial capability can progress if allowed; the battery gap stays
  explicit and cannot be hidden by renormalizing covered value to the full plant.
