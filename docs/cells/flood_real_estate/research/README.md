---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-15
updated: 2026-10-15
status: active
scope: Source checks after intake of Junga's proposed Flood package; research evidence only, separate from the unchanged v0.1 artifact.
---

# Flood Real Estate research after branch intake

The [v0.1 proposal](../README.md) remains unchanged. This folder holds follow-up evidence needed for the
owner's selected three-story office and other qualification questions. The
[intake review](../../../extra/discussion/real_estate_conus/03_junga_research_intake_and_next_work.md)
owns the research disposition and next work.

| # | Date | Created by | Related to | Doc | What it is |
|---|---|---|---|---|---|
| 01 | 2026-10-15 | owner-directed (Divy) · agent-drafted | Office candidate | [Office source receipt](office_source_check.json) and [comparison table](office_df431_vs_retail_df217.csv) | Exact source pins and 29 floor-relative depth knots comparing COM4/DF431 office with COM1/DF217 retail |

## Office source check

The source carrier is the Hazus table preserved in the Plymouth trial at Hazard commit
`09b95acbe39b4981e446a5b4dc3ab7d7d07f8911`. Office DF431/COM4 was compared against the pinned primary
[USACE go-consequences occupancy implementation](https://github.com/USACE/go-consequences/blob/dff647cabbc1abae3f084e80b7f6a166651d05d8/structures/occtypes.json).
All **29 office knots match exactly**, before dividing source percentages by 100. The receipt records
both input hashes, the exact JSON locator, carrier row filters and the comparison CSV hash.

At 4 ft above first floor, the compared retail table gives DR 0.18 and the office table gives 0.28.
That 0.10 difference is evidence against silently relabeling the retail response. It is not a calibrated
loss prediction for our particular three-story design. The COM defaults are class-average responses and
do not describe separate damage to each floor.

To reproduce: fetch the exact USACE raw URL in the receipt, extract the carrier with `git show` at its
recorded commit/path, verify both hashes, select `DmgFnId=431`/`Occupancy=COM4`, and compare its 29 depth
columns (−4 through 24 ft) with the JSON locator. Extract DF217/COM1 only for the comparison. Convert
percent to fraction once. Do not interpolate or round to manufacture the exact-match result.

## Limits and next qualification

- The FEMA default-selection manual was checked in Junga's source review; this pass did not independently
  download and verify those manual bytes. Agreement between two table carriers is not independent claims
  calibration or proof of applicability to every office.
- Office is not a record in the imported v0.1 artifact. Adding it requires explicit selector identity,
  source/claim/value reconciliation, capability review and tests through the existing change workflow.
- Freshwater evidence does not select a coastal prototype. Construction, story scope, source geography
  and wave/velocity exclusions need separate review.
- Building replacement values and coverage of fixed services/interiors are not resolved by this curve
  comparison. Dollar losses remain unavailable.
- The NFIP claims comparison mentioned in Slack was not located in the inspected branch. No claim of
  field calibration, coastal rejection or source superiority is made from that unavailable analysis.
