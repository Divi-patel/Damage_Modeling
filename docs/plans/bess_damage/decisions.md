<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS Damage process and research decisions; owner scope versus analyst findings distinguished
-->

# Decisions

## BD-D01 — Approved reference and natural-hazard boundary

**Decision (owner):** use the Hazard r1 battery plant, unit transformers included,
collector station/export line excluded. Natural-hazard physical damage includes
supported triggered consequences; autonomous internal events remain outside scope.

**Reason:** compare a canonical asset geographically, preserving modules and
ownership rather than combining unrelated operational event rates.

## BD-D02 — Enclosure and PCS first

**Decision (analyst implementation):** concentrate the first numerical candidate
on the $84M enclosure group and $10.4M PCS group. Preserve the remaining budget
and unsupported mechanisms visibly.

**Reason:** the two independently valued groups comprise 85.97% of the reference
budget. This is research prioritization, not admitted damage coverage or a reason
to renormalize the other value away.

## BD-D03 — Reject two automatic transfers

**Decision (evidence review):** do not bind the whole-substation Hazus curve to
BESS or treat Chen et al.'s storage availability equation as a physical DR.

**Reason:** the former has a different inventory/denominator; the latter lacks the
required replacement endpoint and a complete target-applicable calibration.
Retain supporting mechanisms and form ideas. See BF-C03 and the reuse matrix.

## BD-D04 — Preserve electrical candidates without changing current cells

**Decision (analyst implementation):** pin and audit existing curves, then qualify
each target transfer separately. Do not modify Solar/Wind curves for this task.

**Reason:** common labels do not establish common failure units. The audit is
reproducible while existing consumers retain their results.

## BD-D05 — Scaling is a later required delivery item

**Decision (owner, 2026-10-18):** document how the production team can use the work
for other asset sizes after the reference model works.

**Reason:** power, energy, integer units, shared property and layout can change
differently. Damage supplies compatibility rules; Hazard/recipient code supplies
any qualified resizing or screening projection. Current research proceeds.


## BD-D06 — Preserve candidate status after the second pressure test

**Decision (analyst evidence review):** keep exact `FS_INV` as a conditional T3
PCS candidate; do not select the full-enclosure step, uniform-height curve or
an average of those interpretations as the battery mean.

**Reason:** the OEM and immersion evidence establishes distinct repair/entry
questions. The sensitivity comparison materially changes loss, and neither
shape resolves the missing link. Continue with a grouped repair rule and
same-unit cost allocation; no cell simulation or hazard rebuild is required.
See [the candidate review](../../extra/discussion/bess_damage/03_flood_candidate_pressure_test.md).

## BD-D07 — Use source-derived shares without changing the reference budget

**Decision (analyst evidence implementation):** retain the original $84M
enclosure total and record a T3 internal allocation using the historical PVSCM
market-case direct inputs. Keep its undistorted-input allocation as sensitivity.

**Reason:** dimensionless related-benchmark shares are a reproducible starting
point; cost categories are not repair units. No new value, current tariff claim
or runtime damage ratio follows. See
[BF-C17–BF-C18](../../extra/discussion/bess_damage/evidence/claims.csv).

## BD-D08 / BF-Q01 — common-entry policy approved for local testing

**Owner ruling, 2026-10-18:** “Use the conservative candidate for local testing (Recommended)”.
The [review](../../extra/discussion/bess_damage/04_grouped_repair_and_value.md)
defines the 0.30 m common-entry assumption and active-hardware replacement
policy. Both remain T4; approval permits a local candidate, not calibration,
complete-plant loss, annual metrics or national publication. The next task is
to package and test this exact policy, retaining the separate PCS candidate and
unresolved property.

## BD-D09 / BF-Q02 — saline-entry replacement approved for local testing

**Owner ruling, 2026-10-18:** “Use replacement after saltwater entry (Recommended)”.
The [r4 comparison](../../extra/discussion/bess_damage/05_remaining_property_and_flood_domain.md)
defines the rule: saline depth strictly above the assumed 0.30 m entry triggers
replacement of covered active enclosure and PCS hardware. At 0.45 m one PCS is
$520,000, versus $390,000 under the unchanged freshwater proxy. This is an
explicit T4 local policy, not a measured mean or annual-use approval.

Package local model v0.2 separately. Preserve the v0.1 bytes and all supported
freshwater outputs; carry the existing hardware ceiling into deeper freshwater
as the documented engineering continuation. Keep the $27.2896M residual value,
source missingness and source-bin uncertainty visible. No new hazard model or
global schema change is authorized or required for this bounded local test.

## BD-D10 — conditional annual admission after the owner-directed proof

**Owner direction:** proceed after the Coastal local proof, document carefully,
and raise material blockers. **Analyst qualification:** preserve every v0.2
response ordinate and value; create canonical model v1.0 under
`NEW_CELL_MODEL_RELEASE` after the bounded annual consumer passes.

Existing annual clocks, a shared inland rank/Coastal event, per-physical-unit
no-restoration caps, original probability mass and explicit coverage are required.
The [consumer proof](../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/07_annual_flood_proof.md)
passes 29 cases × 100,000 years plus independent mean and tail checks.
This is an engineering admission under the continuing work authorization; the
original BF-Q01/BF-Q02 rulings remain local-policy approvals, not claims of
calibration. Conservative entry/consequence assumptions remain T4.

The current cell is indexed in this repository; portable packaging, national
spatial qualification, complete-property coverage and delivery remain separate.
Old local pins and existing other-cell outputs are unchanged. Retain the
material Coastal first-bin sensitivity for the spatial pilot.

## BD-D11 — conditional Hurricane annual admission

Owner direction, 2026-10-19: continue the annual-loss qualification after the local
source/reference proof. Analyst qualification: preserve v0.1 conditional records
and unit values, and admit first repository-canonical v1.0/docs r1 after 90 local
configurations × 100,000 years, independent unit-PGF means, analytic OEP, annual
array/tail replay and controlled unit-cap tests pass.

[Qualification and scope](../../extra/discussion/bess_damage/08_hurricane_annual_qualification.md).
This is a conditional screening admission under continued authorization, not
owner certification of empirical fragility. Common-rank spatial dependence,
mean-severity projection, source gaps, no restoration and $15.4M unbound property
remain explicit. National support and portable/recipient publication remain
separate. Existing v3 schemas, other cells and old proposal bytes are unchanged.
