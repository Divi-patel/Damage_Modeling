---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Evidence and seven-step audit for BESS local candidate v0.2
---

# Derivation and evidence limits

The [bounded r4 review](../../../../extra/discussion/bess_damage/05_remaining_property_and_flood_domain.md)
and its BF-C23–C30 claims are the authoritative research trail. The selected
coastal rule follows the owner's BF-Q02 reply, not new measured loss data.
Schneider/NEMA recovery guidance and adjacent immersion evidence constrain
interpretation but do not fit a BESS depth-to-cost curve.

The active enclosure value remains
`$1,050,000 × (96.3 + 17.5 + 7.5) / 141.3 = $901,380.0424628449`.
For the binary policy `DR = int(d > 0.30)`; only states 0 and 1 are accepted.
One separate PCS retains its own $520,000 denominator. Saline water uses the
same binary policy; freshwater retains `FS_INV(max(0,d−0.30))` and explicitly
continues DR=1 beyond its last native knot. No extra capex or duplicated cooling
cost is introduced by the new saline curve record.

| Seven-step audit | v0.2 disposition |
|---|---|
| Asset and event | Same standalone outdoor LFP reference; direct natural inundation, explicit freshwater/saline condition |
| Failure units | 80 active enclosure groups and 20 separate PCS; source-grain and value membership retained |
| Endpoint | Conditional hardware policy cost / same-unit hardware value; not outage or empirical mean |
| Split rows | Unchanged r3 allocation and four unresolved property buckets |
| Allocate values | Candidate $82.5104M + unmodeled $27.2896M = $109.8M; no new coverage |
| Site adapter | Unit-local grade depth; one entry subtraction or binary test; finite/nonnegative inputs; unknown condition withheld |
| Apply and restrict | Explicit local opt-in; matching policy/pin; annual and complete-plant metrics withheld |

Saturation is a T4 continuation of a replacement endpoint. It does not claim
that high-water cleanup, soil contamination or other property costs are capped
by the covered equipment alone. The saline policy can overstate shallow-entry
damage; the first-source-bin sensitivity must stay visible when class depths
straddle 0.30 m. Source-censored deep water remains censored even when the
covered replacement amount is invariant to further depth.

Future work: target-matched ingress/service evidence, consistent MV/control and
composite cost splits, additional physical pathways, then separately qualified
annual use and size scaling. These are retained in the r4 review and Hazard plan.
