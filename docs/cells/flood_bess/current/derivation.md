---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Source-linked seven-step audit and conditional annual semantics
---

# Evidence, value and annual qualification

## Seven-step audit

| Step | Qualified disposition |
|---|---|
| Asset / boundary | One outdoor liquid-cooled LFP plant; unit transformers included in the physical boundary but currently in unmodeled value; collector/export excluded |
| Failure units | 80 active enclosure groups and 20 separate PCS, unique IDs; no overlapping cell/rack/cabinet charges |
| Endpoint | Conditional hardware replacement/repair fraction of that same hardware value; conservative screening policy, not an empirically calibrated mean |
| Split rows | Preserve original reference budget and r3 cost allocation; no new electrical-balance subdivision |
| Allocate value | $1.05M × 121.3/141.3 = $901,380.0424628449 active hardware per enclosure; $520,000 per PCS; full partition reconciles to $109.8M |
| Site adapter | Unit-local grade depth, one strict entry test or one PCS entry subtraction; explicit water condition; source missingness retained |
| Apply / restrict | Original PCS knots; binary strict-entry response; deep replacement plateau; conditional annual capability subject to verified event dependence, caps and missing mass |

The [v0.2 derivation](../proposed/local_candidate_v0_2/derivation.md) and
[claim/source registers](../../../extra/discussion/bess_damage/evidence/README.md)
remain the evidence trail. BF-C18/20/26/27/30 explain value, entry, saturation and
saline policy. Those source strengths do not increase because the artifact is
now canonical. The ordinary value mapping and every conditional DR are unchanged.

## Annual interpretation and limits

Hazard owns frequency and annual composition. Inland uses the existing
log-AEP **depth** interpolation and common annual rank across equipment.
It evaluates Damage afterwards; interpolating losses would smooth away entry
thresholds. Pluvial uses the actual per-pixel capacity, at most 0.30 m; therefore
this direct-entry mechanism remains zero on supported Pluvial locations.
That is not a claim of zero all-mechanism BESS Pluvial damage.

Coastal uses the existing observed rate and direct-event catalog. Event category
selects the matching MOM severity field. All units share that event and the
plant remains fixed through the year. This is an existing screening surrogate,
not event-resolved hydraulics. Source categories absent from the catalog do not
receive invented probability. Missing clocks are not measured zero rates.

No within-year restoration is modeled. A unit's annual accumulated cost cannot
exceed that unit's replacement value. Two repeated hits on one enclosure do
not consume another dry enclosure's value. OEP is the maximum **whole-event**
loss; AEP sums each unit's capped annual cost. Summing component OEPs would be
wrong when different events affect different components.

For the binary saline response the exact modeled annual mean is
`sum_i V_i * (1 - exp(-lambda * p_i))`, where `p_i` is the catalog share of events
that produce a known positive response at that unit. This checks Monte Carlo;
unknown responses retain their own probability flags, not a zero-risk claim.
The positive-response probability is not supplied by a safety certification.

The first 0–1 ft SLOSH bin straddles 0.30 m. Keep the native midpoint response
and an upper-bin sensitivity; do not mistake the latter for a calibrated mean
or a full-risk upper bound. Tails require the consumer's annual distribution
and exact tail-mass accounting; no additional vulnerability spread is assumed.

## Double-counting and future work

| Potential overlap | Current control |
|---|---|
| Battery, BMS, cooling versus enclosure | One source-derived active-hardware value; residual enclosure/fire/racks separate and unmodeled |
| PCS versus unit transformer / cables | Separate PCS value only; no allocated transformer proxy |
| Repeated hazards/events | Annual cap per physical unit; no within-year repairs or reinstatement |
| Sub-perils or other hazards | No combined annual result admitted by this proof; later composition must state overlap |
| Protection and entry | Apply entry once; no IP/UL effectiveness multiplier |

Refinements remain in the [future-work register](../../../../../Hazard_modeling/docs/discussion/_cross_cutting/bess_conus/03_future_research.md): matched service evidence, residual value/response, additional mechanisms, restoration, source-bin sensitivity, and size/duration scaling. No complete-property or portfolio claim is supported here.
