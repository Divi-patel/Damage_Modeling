<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Exact inputs, review-only numerical cases and full value accounting.
-->

# Substation reuse — research receipts

The [candidate-binding review](../06_flood_binding_candidate_and_proof.md) is reproduced with
`scripts/reference_helpers/review_substation_flood_binding.py` and checked with
`scripts/reference_helpers/validate_substation_flood_binding.py`. Its
[results](flood_binding_review.json), [31-row crosswalk](flood_binding_value_crosswalk.csv),
[validation](flood_binding_validation.json) and [native-input preflight](flood_native_input_preflight.json)
are separate from the earlier source-table reproduction below. Candidate arithmetic is not an admitted loss.

[cross_hazard_inventory.json](cross_hazard_inventory.json) records the October 16 current/proposed curve
inventory and inspected Hazard consumer/Total/dashboard files by SHA-256. It supports the
[cross-hazard audit](../05_cross_hazard_reuse_inventory.md); it is not a numerical test result or runtime
registry. The Flood reproduction below remains a separate measured receipt.

Run from Damage:

```bash
.venv/bin/python scripts/reference_helpers/review_substation_flood_reuse.py \
  --hazard-repo ../Hazard_modeling
```

This reads exact Git blobs, verifies the local reference evaluator equals its pinned version, and writes
only this review directory. Use `--output-dir /tmp/substation-reuse-review` for a separate reproduction.
The two repositories must contain commits named in the script; no network or current-branch assumption is needed.

- [review_receipt.json](review_receipt.json): 93 passed curve cases, wrong-SHA rejection, exact source/profile
  pins, current annual withholding and research status.
- [value_review.csv](value_review.csv): all 28 installed rows plus three support rows, exactly once;
  $30,415,059.81 total. Every row remains unadmitted and no allocation fraction is chosen.

**What passed:** retained-table reproduction, supported-input handling, explicit withholding/rejection,
source-pin checks and complete cost accounting. **What did not become approved:** new-profile applicability,
repair denominator, annual risk, publication or a new cell. See the [review](../01_assembly_reuse_review.md).

The numerical reference helper retains historical proposal-only scenario metadata. This receipt tests its
DR behavior and separately reads the canonical capability. It is not a production-runtime certification.
