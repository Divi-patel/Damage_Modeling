---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Read-only Wildfire source reproduction and BESS consequence arithmetic
---

# BESS Wildfire evidence

Start with [intake and BWF-Q01](../../09_wildfire_damage_intake.md), then
[sources](sources.csv), [claims](claims.csv), [parameters](parameters.csv),
[reuse](reuse_matrix.csv), [values](value_crosswalk.csv) and [search](search_log.md).

[Source probes](source_curve_probes.csv) reproduce **Solar** records.
[PCS arithmetic](pcs_transfer_pressure_test.csv) is a hypothetical transfer audit,
not an admitted BESS curve. [Cost cases](consequence_cost_probes.csv) carry no
hazard states or probabilities. No runtime artifact or schema changes.

From Hazard, reproduce:

```bash
.venv/bin/python ../damage_modeling/docs/extra/discussion/bess_damage/evidence/wildfire/audit_reuse.py
.venv/bin/python docs/plans/_cross_cutting/bess_conus/verification/check_wildfire_source_support.py
```

The second command is an unsited source-support diagnostic owned by Hazard,
not a Damage evaluator. [Validation](validation.json), [pins](input_receipt.json)
and [captures](source_captures.json) separate identity, numerical reproduction,
scientific inference and open choices. This is same-author review with independent
table/equation checks, not external scientific certification.

Tesla bytes stay in the prior Flood cache. New HTML captures, PDF extractions
and three inspected page renders are under gitignored
`data/bess/raw_wildfire_review_r1/`. USFS/Sungrow PDFs were fetched/hashed/parsed in
memory because storage was full; full PDFs were not retained. URLs/hashes allow
retrieval. Full source texts/images are not redistributed in committed evidence.
These helpers are research utilities; production must never import them.
