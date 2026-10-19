---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: active
scope: BESS wind enclosure/PCS cost-policy comparison; research only, no selected runtime default
---

# Enclosure and PCS candidate comparison

Read [the review and BW-Q01](../../../07_hurricane_enclosure_candidate.md).
`experiment_spec.json` declares this comparison, rather than a runtime Damage
artifact. `compare_candidates.py` reads the exact existing source response and
cost allocation; it writes state costs, response probes, value/axis controls,
input identities and a plot. No current cell or index is modified. BW-Q01 now
selects replacement for local testing; the comparison retains both policies.

Reproduce from Damage root:

```bash
../Hazard_modeling/.venv/bin/python \
  docs/extra/discussion/bess_damage/evidence/hurricane/r2/compare_candidates.py
```

- `state_costs.csv`: one enclosure's explicit cost hypotheses.
- `response_probes.csv`: two repair policies, three unweighted resistance
  scenarios and a common normalized demand grid; no annual frequency.
- `example_summary.json`: exact one-unit/state and uniform-plant event examples.
- `axis_controls.csv`: invalid, zero, in-domain, pressure/speed and domain tests.
- `source_captures.json`: retrieved primary drawing and reused source pins.
- `audit_receipt.json`: exact experiment/source/asset/value identities and checks.
- `candidate_comparison.png`: conditional response and uniform-event cost on
  common axes; no confidence bands or calibrated uncertainty claim.

Raw PDFs and visually inspected page renders stay in gitignored
`data/bess/raw_hurricane_review_r2/` and the prior caches. A recipient must fetch
and hash-check those inputs to rerun. This research helper is never a Hazard
production dependency. The owner ruling is recorded in `experiment_spec.json`;
subsequent Hazard source-coupling and annual qualification remain separate from
these conditional candidate numbers. The
[proposed package](../../../../../../cells/tropical_cyclone_wind_bess/proposed/local_candidate_v0_1/README.md)
contains its exact local reader and validation. Its builder is
`build_local_candidate.py` in this evidence directory.
