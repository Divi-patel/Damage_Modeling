---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Bounded BESS Hurricane-wind evidence intake; source-only reproduction, no BESS runtime response
---

# Hurricane wind evidence: first bounded pass

Read [the intake verdict](../../06_hurricane_wind_intake.md), then the
[sources](sources.csv), [claims](claims.csv), [reuse matrix](reuse_matrix.csv)
and [bounded search log](search_log.md). These extend the BESS research history;
they do not replace the Flood registers or create a current wind cell.

`source_curve_probes.csv` contains **Solar source-only** evaluations. Its BESS
admission flag is false. The audit helper reproduces the ordered-state equation
independently, checks pressure/speed semantics, reconciles the ten reference
budget rows, checks evidence references and records exact input hashes.
`validation.json` reports actual checks; `skill_check.json` records the current
local skill validation and its working-tree provenance. These are not scientific
qualification or calibrated uncertainty results.

Run from the Damage repository root:

```bash
.venv/bin/python docs/extra/discussion/bess_damage/evidence/hurricane/audit_reuse.py
```

Source PDFs/HTML and three inspected page renders remain in gitignored
`data/bess/raw_hurricane_review_r1/`; earlier OEM manuals remain in their original
Flood research cache and retain their original hashes. The receipt records URLs,
byte identities and exact reviewed pages. A recipient without those caches can
inspect the committed source/claim records, but must retrieve and verify the
inputs to rerun the complete audit. No full source texts are republished.

This helper is a research utility. Hazard production code must never import it.
