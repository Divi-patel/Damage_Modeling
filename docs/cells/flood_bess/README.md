---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Canonical partial-property BESS Flood screening response
---

# Flood × BESS

**Current: canonical conditional model v1.0 / docs r1.** The response and values
are identical to the tested local v0.2 package. Annual screening is permitted
only when the declared frequency, coupling, unit-cap and support checks pass.

Start with [the plain-language explanation](basics/README.md),
[the current package](current/README.md) and [validation](current/validation.json).
The [Hazard annual proof](../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/07_annual_flood_proof.md)
passes 29 diagnostic cases. It is not a national result or empirical calibration.

Covered scope is active battery/management/cooling hardware and separate PCS:
$82.5104M of $109.8M. $27.2896M remains unmodeled. Other physical pathways,
autonomous failures and external collector/export property are not included.

The [version register](VERSION_REGISTRY.md) preserves the distinction between
current canonical use and local-only [v0.2](proposed/local_candidate_v0_2/README.md)
and [v0.1](proposed/local_candidate_v0_1/README.md). The current tuple is indexed;
no portable package or national publication has been issued. Source evidence
and reasoning remain in the [BESS research record](../../extra/discussion/bess_damage/README.md).
