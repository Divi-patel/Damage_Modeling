---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Same-response first canonical BESS Hurricane screening release and consumer qualification
---

# Derivation and applicability

Read the [original conditional derivation](../proposed/local_candidate_v0_1/derivation.md)
for all source/claim locators, T4 state probabilities, NREL-based cost allocation
and the BW-Q01 major-compromise replacement policy. The [annual qualification](../../../extra/discussion/bess_damage/08_hurricane_annual_qualification.md)
changes downstream admission after validation, without recalibrating those
conditional curve records or unit values. Record IDs retain their provenance
identifiers; the exact cell model is v1.0/docs r1.

Explicit response hypotheses are required: `approved_replacement` or
`repair_sensitivity`; explicit resistance scenarios remain lower, central and
upper. These are unweighted alternatives, not a probability distribution or
confidence interval. The comparable pressure axis remains 0–2; unsupported
values are withheld. No construction, height, storm-kit or autonomous-fire credit
is inferred. Surge/rain flood, Strong Wind/Tornado and internal autonomous failure
remain separate scopes.

A supported consumer declares its comparable reference, storm frequency and
spatial coupling. The tested Hazard case uses a regional MRI1700 reference with
MRI700/3000 sensitivities and a common Poisson exceedance-rank across native unit
curves. It uses each unit's conditional mean response, applies a no-restoration
annual value cap to each physical unit before plant summation, retains unknown
source/domain mass and recomputes annual tails from the same capped distribution.
The consumer's reference/coupling is an assumption, not a measured joint storm.
Missing clocks and source tails remain unknown. No national coverage claim,
intrinsic Damage spread or complete-property result follows.

The [validation receipt](validation.json) states the exact finite proof and
limits. This is same-author validation with independent numerical methods, not
external scientific review. Matched failure/service evidence and residual value
remain deferred targets in the original dossier and Hazard future-work register.
