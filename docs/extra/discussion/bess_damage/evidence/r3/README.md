---
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: done
scope: Reproducible source allocation and unadmitted repair-policy arithmetic
---

# Grouped-value audit r3

Read [the decision and evidence](../../04_grouped_repair_and_value.md) first.
This is a research checkpoint, not a runtime artifact or an average-loss curve.

| File | Contents |
|---|---|
| [Source captures](source_captures.json) | Exact raw inputs, URLs, bytes, hashes, review scope and visual checks |
| [Parameter register](parameter_register.csv) | Source allocations versus open engineering assumptions |
| [Value allocations](value_allocations.csv) | Four groups; market-input allocation plus undistorted-input sensitivity; both preserve $84M |
| [Repair examples](repair_policy_examples.csv) | Three explicit replacement policies, without probabilities or complete-loss claims |
| [Entry examples](entry_policy_examples.csv) | Two hypothetical entry levels; neither is an adopted runtime default |
| [Checks](known_answer_checks.csv) | 31 source, arithmetic, unknown-input and unit-grain checks |
| [Receipt](audit_receipt.json) | Source, reference, helper and output hashes; runtime admission false |

From the Damage root, after obtaining the pinned originals in the ignored cache:

```bash
.venv/bin/python scripts/reference_helpers/bess_flood_value_audit.py \
  --hazard-repo ../Hazard_modeling \
  --output-dir docs/extra/discussion/bess_damage/evidence/r3
```

The helper reads source text inputs and reference CSVs. It does not execute the
Excel workbook/macros, fit a depth curve, infer affected fraction, emit annual
metrics, change a profile or publish anything. The source workbook is an unloaded
template: its blank input cells are not zero-cost observations. Downloaded full
text and rendered source pages stay in the ignored cache; only extracted
numerical inputs, transformations and provenance travel with this review.
