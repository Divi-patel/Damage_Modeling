---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: settled
scope: First BESS Wildfire conditional annual screening admission; numerical response and values unchanged
---

# BESS Wildfire: conditional annual admission

**Local annual proof passed; model v1.0/docs r1 is repository-canonical for
conditional screening.** This is `NEW_CELL_MODEL_RELEASE` under the existing
new-cell workflow, not a change to the original seven conditional records.
Bundle v3 and capability v3 schemas remain unchanged. No portable package is
issued. Same-author review uses independent numerical methods; external
scientific review and empirical BESS calibration are not claimed.

The [qualification receipt](evidence/wildfire/r3/annual_qualification.json)
pins 72 configurations × 100,000 years from the twelve saved high-BP source
stress probes, three consequence hypotheses and two ordinal shapes. Rate/class
marginals agree within 1.39e-17 per year. Independent AEP/OEP array replay is
exact. Bounded per-unit Poisson enumeration limits the whole-hardware mean
truncation error to $0.000001624. Source-law sampling checks pass; the minimum
analytic OEP family p-value is 0.1047. Independent financial-metric replay differs
by at most $0.000006974, inside the existing $0.00001 gate.

The common occurrence-rate and severity ranks are an explicit screening spatial
law, not measured fire footprints. Per-unit annual caps prevent repeated losses
to one unit from borrowing dry hardware value. Conditional mean Damage carries
no intrinsic stochastic spread. An unavailable clock or source-policy exclusion
remains explicit; 100% unknown support is not an annual fire probability.

## Release and consumer boundary

[Current package](../../../cells/wildfire_bess/current/README.md) supplies
conditional severity only. The new canonical reference selector is
`BESS_LFP_R1_WILDFIRE_ORDINAL_V1`; named failure units, pathway, cost/shape choices,
repair serviceability counterfactual and exact integer-state domain remain
mandatory. Every conditional table and same-unit dollar value matches v0.1.
The original proposal/evaluator remains historical local-test evidence and cannot
emit annual financial metrics. Hazard never imports that authoring utility.

Hardware scope remains $94.4M of $109.8M full fixed-2024 TIV. The $15.4M mixed
MV/shared electrical, civil and fieldwork scope stays unbound. Autonomous events,
BI, performance, external collector/export and a new propagation model are not
added. T4 transfer, no blanket protection credit and unweighted sensitivities
remain explicit. Matched-test, repair-BOM, site-transfer, footprint and residual
work remains under BR-24–BR-26; stronger claims still require their own proof.

Consumers must pin the exact current artifact/capability/value tuple and qualify
source exposure, event dependence, original support, separate physical-unit caps
and annual distributions before reporting EAL/PML/VaR/TVaR. Local admission does
not imply national execution, canonical Hazard publication or recipient selection.
[Hazard plan/proof](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/20_wildfire_annual_proof.md)
owns the executable consumer. [Completed readback](evidence/wildfire/r3/consumer_readback.json)
now verifies all 84 NPZ packages / 588 arrays byte for byte before/after
admission, 28 new annual controls, 64 current BESS tests and an executed
notebook with two inspected figures. The selected Hazard suite has 229 passes
and the same inherited Convective Wind architecture failure. National support
and publication remain separate.

## Change record

- Classification: `NEW_CELL_MODEL_RELEASE`; new model v1.0/docs r1.
- One `wildfire_bess` row added to the runtime index; other cells unchanged.
- Existing source/claim/value CSVs and 84 known answers preserved exactly.
- Capability changes from withheld proposal to conditional downstream annual use.
- No schema, portable package, curve ordinate, economic hypothesis or value change.
- [Author/validator](evidence/wildfire/r3/release.py) verifies schemas, parity,
  content pins, provenance paths and the once-only runtime index entry.

The broad runtime validator still fails on the pre-existing Flood BESS v2
vulnerability-spread flag. That artifact is byte-identical to HEAD; the old
index reproduces the failure. The new Wildfire cell separately passes the
validator's seven-record v3 checks, existing v3 schemas and exact pin/value
checks. [Scope receipt](evidence/wildfire/r3/runtime_validation_scope.json)
records this inherited debt; a global validator pass is not claimed.
