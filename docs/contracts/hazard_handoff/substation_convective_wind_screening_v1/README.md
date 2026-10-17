---
author: "owner-directed (Divy) · agent-qualified"
created: 2026-10-17
updated: 2026-10-17
status: active
scope: Explicit cross-hazard direct-wind screening proxy; no intrinsic source curve change or complete Tornado claim.
---

# Substation Strong Wind and Tornado — direct-wind consumer binding

[binding.json](binding.json) separately qualifies the unchanged canonical `tropical_cyclone_wind_solar`
model v2.1 / docs r2 response `TCWS21_GSU_SUBSTATION_SCREENING_T4_ORDERED_STATES` for the canonical
station's **direct wind-loading contribution**. This is a T4 cross-hazard proxy with exact source identity,
not a renamed Hurricane permission or a new calibrated Tornado damage model. The [value crosswalk](value_crosswalk.csv)
retains the same fenced $27,353,236.37 assembly. No new component fragilities are introduced.

Change classification: inside-repo, target consumer binding under the illustrative-asset reuse guide.
The source response parameters, canonical artifact, existing cell outputs and capability remain unchanged.
This new binding owns its target applicability and value/exposure choices. The source's conditional annual
permission is necessary but does not itself establish applicability; the following qualification does.
No shared Damage runtime registry or intrinsic cell release is introduced. Hazard shares only the numerical
ordered-state evaluator between two real consumers, with exact equality tests.

## Seven-step qualification and evidence

| Dimension | Source → target reasoning | Disposition and limit |
|---|---|---|
| Asset | GSU/substation assembly → same selected 345/138 kV AIS yard, two 336 MVA transformers | Retain prior GSU-to-transmission T4 transfer; not equipment-specific calibration |
| Failure unit | One site-facility direct-wind assembly | No sum of assembly and child damage; Tornado partial contact is Hazard coupling |
| Mechanism | Aerodynamic demand increases with squared gust; compatible three-second event/design ratio | Strong Wind adopted as T4 direct loading. Tornado adopted only for direct loading; debris, pressure change, rotation, duration and cascading electrical failures are unmodeled |
| Input | Source site-facility pressure ratio, domain 0–2 | Strong Wind ASCE gusts already three-second. EF midpoint is a damage-inferred gust proxy, not a measured Exposure-C observation; its use on this axis is an explicit T4 bridge. No Hurricane duration conversion |
| Consequence | Same physical repair/replacement ordinate, same whole-unit denominator | Fenced TIV once, external road/support $3,061,823.44 outside; prior civil-membership T4 assumption retained |
| Numerical response | Same medians, beta 0.35, costs 0/0.08/0.35/1 and three unweighted resistance cases | No tornado uplift multiplier, extrapolation, scenario probability or new ordinate |
| Annual use | Hazard supplies frequency, finite-footprint contact, severity probabilities, count law and cap | Screening contribution after consumer proof. Unknown event mass retained at zero contribution with tags; complete risk remains unavailable |

Primary evidence inspected 2026-10-17:

- [NIST tornado design guide](https://www.nist.gov/publications/design-guide-new-tornado-load-requirements-asce-7-22)
  treats tornado forces separately from ordinary wind design. It supports distinguishing mechanisms, not
  these curve ordinates or a station-specific numerical multiplier.
- [NIST explanation of tornado loading](https://www.nist.gov/news-events/news/2024/07/tornadoes-are-deadly-these-new-building-codes-will-save-lives)
  explains distinct tornado effects and documents substation damage at Joplin. It does not calibrate repair ratios.
- [NWS EF scale](https://www.weather.gov/tae/ef_scale) gives damage-inferred wind bands. EF5 has no official
  finite upper band; 253 mph is the existing Hazard model's bounded convention, not an NWS limit.
- Exact existing source curve and prior station/value qualification:
  [Hurricane binding](../substation_hurricane_screening_v1/README.md). These ordinates remain expert
  assumptions, not claims-calibrated evidence. Equal source and target numbers prove numerical reuse only.

## Consumer scope and future replacement

The initial map uses existing 0.25° Strong Wind profiles and 150 km pooled Tornado rates/EF mixtures.
Tornado contact uses the actual footprint area as an equivalent square and a consistent rectangular path
intersection. Uniform spatial value and parallel path geometry are T4 approximations; no equipment
locations or resilience credit are asserted. Source national **median** path dimensions are reused.
The existing regional Fano factor remains after contact thinning, as in the current model; this is not
an exact derivation of spatially thinned outbreak clustering.

Unresolved response tails are not clipped into the source's domain and do not become safe locations.
The result is a modeled direct-wind contribution, not a proven bound on true loss: curve transfer and
contact approximations have model error of unknown sign. Numerical omitted-response contribution is zero.
A complete Tornado response requires the deferred component/pathway research; this work does not reopen it.

Combined Strong Wind + Tornado uses independent annual streams, then one station cap. It is not a common
storm catalog and cannot be added to Hurricane as a deduplicated all-wind Total. ASCE wind overlap with
Hurricane remains a downstream Total decision. No BI, service interruption or portfolio risk is modeled.

[Hazard plan and proof](https://github.com/aamani-ai/Hazard_Modeling/blob/codex/substation-conus/docs/plans/_cross_cutting/substation_conus/22_convective_wind_grid.md)
records the consumer implementation and measured checks. Replace this proxy when an admitted station-specific
response materially improves the current screening scope; preserve this exact binding for reproduction.
