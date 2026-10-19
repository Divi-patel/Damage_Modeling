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

## Open BF-Q01 — common-entry active-hardware replacement policy

**No owner ruling recorded.** The [review](../../extra/discussion/bess_damage/04_grouped_repair_and_value.md)
recommends a conservative candidate, explicitly T4 for entry/affected-group and
replacement assumptions. Costing and testing that candidate is not adoption.
