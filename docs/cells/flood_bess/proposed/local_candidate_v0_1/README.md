---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Owner-authorized freshwater BESS local candidate v0.1 / docs r1
---

# Candidate package and permitted use

The [JSON artifact](curve_artifact.json) and [binding](value_binding.json) are
the proposed response and same-unit values. [Consumption pins](consumption_pin.json)
identify exact bytes. The [capability](capability.json) withholds normal runtime
and all annual metrics; explicit local testing is authorized separately by BF-Q01.
Read [derivation](derivation.md) and [input/output rules](metadata.md) before use.

| Property / role | Candidate treatment | Value |
|---|---|---:|
| Battery, management and cooling / primary | Binary replacement after assumed entry; T4 policy | $72.1104M across 80 units |
| Separate PCS / primary | Unchanged nine-knot FS_INV proxy; T3 shape, T4 entry | $10.4M across 20 units |
| Enclosure/racks/fire safety | Unmodeled; not DR≈0 | $11.8896M |
| Internal electrical balance | Unmodeled mixed bucket | $13.2M |
| Civil and fieldwork | Unmodeled; fieldwork never an independent damage curve | $2.2M |
| Collector station/export, BI, autonomous internal failures | Outside agreed property/event scope | Excluded from this reference |

No conditioner-only hardware gets a numerical protection benefit. No residual
bucket has been declared immune or negligible. Salinity, duration corrections,
wave/debris/scour, conduit bypass and inter-enclosure spread are not modeled.
The active replacement amount already covers its damaged hardware; do not add
another overlapping thermal-damage charge.

**Axis:** freshwater external depth above the same local grade as the selected
0.30 m entry. The battery adapter creates a binary state. PCS subtracts entry
once. The 0–2.3 m external range is the local test envelope, not a physical flood
limit. The y-axis is same-unit hardware policy cost divided by same-unit hardware
value; it is not outage probability or a claims-calibrated mean.

**Selectors / conditioners / exposure:** selected outdoor LFP separate-PCS
reference; explicit policy acknowledgment; freshwater scenario; local unit
depth and availability. Geometry is provided by the pinned Hazard profile.
No default affected share, IP protection, extra height or MW multiplier applies.

**Audit-view map (workbook deviation):** use [known answers](known_answers.json),
[value crosswalk](value_crosswalk.csv) and the existing
[r3 allocation table](../../../../extra/discussion/bess_damage/evidence/r3/value_allocations.csv).
The small candidate uses these inspectable JSON/CSV views instead of a duplicate
Excel workbook (`source_workbook: null`). This follows the add-cell workflow's
audit-view option. A future release can add a workbook if it improves review.

Run the Damage validator from the repo root:

```bash
.venv/bin/python scripts/reference_helpers/validate_bess_flood_candidate.py
```

The local Hazard adapter is `flood.bess_candidate`; the conductor is
`python -m conus_grid.flood.bess_candidate_review`. Neither imports research
helpers or a notebook. See Hazard's
[local proof](../../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/04_local_flood_proof.md)
for exact invocation and results. Matched service/entry evidence, residual-value
coverage, annual use and later size scaling remain explicit next work.
