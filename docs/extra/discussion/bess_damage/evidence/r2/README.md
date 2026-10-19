---
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS Flood candidate pressure tests; research only, no admitted response
---

# Candidate pressure-test evidence

Read [the interpretation](../../03_flood_candidate_pressure_test.md) before using
these files. **No file here supplies a BESS runtime curve or site-risk result.**

| File | What it establishes |
|---|---|
| [Source captures](source_captures.json) | Four original primary PDFs, versions, exact bytes and review scope; cache is local and ignored |
| [Parameter register](parameter_register.csv) | Source versus assumption, canonical tier, disposition and reopening trigger |
| [Repair-unit matrix](repair_unit_matrix.csv) | The specific entry, repair and cost questions to close next |
| [Experiment specification](experiment_spec.json) | Fixed probe inputs and unqualified hypotheses; not a runtime schema |
| [Battery probes](battery_hypothesis_probes.csv) | Alternative assumption arithmetic, never an interval or a selected mean |
| [PCS probes](pcs_probes.csv) | Exact FS_INV under hypothetical entry, with incompatible/out-of-domain conditions excluded |
| [Known-answer checks](known_answer_checks.csv) | 52 passed numerical, missing/invalid, condition, value and support checks |
| [Audit receipt](audit_receipt.json) | Exact input/output hashes, reference pins, candidate status and no-runtime declaration |
| [Comparison figure](candidate_comparison.png) | Visual explanation of hypotheses versus conditional PCS reuse |
| [Validation](validation.json) | Reproduction, registry integrity and documentation checks; not scientific admission |

From the Damage repository root:

```bash
.venv/bin/python scripts/reference_helpers/bess_flood_candidate_audit.py \
  --hazard-repo ../Hazard_modeling \
  --output-dir docs/extra/discussion/bess_damage/evidence/r2
```

The helper reads the pinned reference, layout, budget and existing source
evaluator. It does not change Hazard physics or call a runtime publisher. Do not
place these formulas in a notebook and use that notebook as a production model.
Further numerical qualification belongs in the governed new-cell workflow.
