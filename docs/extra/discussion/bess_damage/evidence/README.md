<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Reproducible BESS Flood source audits and explicitly unqualified hypothesis tests
-->

# Evidence and audit files

The latest [r3 grouped-value audit](r3/README.md) adds original cost inputs,
same-budget allocations and 31 checks. The [r2 hypothesis tests](r2/README.md)
retain 52 checks and four primary sources. The root-level r1 audit remains the
original source-reproduction record.

- [Sources](sources.csv): primary sources and pinned repository evidence, exact
  locators, permitted and prohibited inferences.
- [Claims](claims.csv): decisions/inferences and their support; no BESS numerical
  parameter is admitted by a source's authority alone.
- [Reuse matrix](reuse_matrix.csv): source-native curve units and BESS transfer
  dispositions.
- [Value crosswalk](value_crosswalk.csv): all ten reference rows reconciled;
  $109.8M included, $23.4M excluded from the rounded source buckets.
- [Source evaluations](source_curve_audit.csv): 95 source-only checks; all BESS
  result fields remain empty. Values outside the source domain only expose the
  helper's clamping behavior.
- [Audit receipt](audit_receipt.json): exact profile, curve, helper and registry
  hashes; checks and explicit non-admission.
- [Source captures](source_captures.json): original-PDF URLs, local cache paths,
  retrieval status and SHA-256; no source full text is republished here.
- [Validation](validation.json): rectangular CSVs, source references, local links,
  metadata and current input hashes checked; no BESS scientific admission.

Reproduce from the Damage repository root:

```bash
.venv/bin/python scripts/reference_helpers/audit_bess_flood_evidence.py \
  --hazard-repo ../Hazard_modeling \
  --output-dir docs/extra/discussion/bess_damage/evidence
```

The helper is a research utility, not a runtime BESS evaluator. It imports the
existing reference evaluator, checks source inputs and writes audit evidence.
Production M2/M3/M4 will remain in Hazard's responsibility-specific packages;
no notebook or review utility becomes a production dependency.
