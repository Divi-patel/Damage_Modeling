# docs/extra/guides/

Practical walkthroughs for common repo operations and user questions.

These are not canonical curve artifacts, contracts, or source drops. They are operating guides that point to
the canonical files and explain the normal process.

## Guides

| Guide | Use when |
|---|---|
| [`hail_solar_curve_request_guide.md`](hail_solar_curve_request_guide.md) | Someone asks for the current solar hail curve or how Hazard should consume it. |
| [`flood_solar_curve_request_guide.md`](flood_solar_curve_request_guide.md) | Someone needs to bridge event water level and component datum into the current flood × solar failure-unit curves. |
| [`wildfire_solar_curve_request_guide.md`](wildfire_solar_curve_request_guide.md) | Someone asks for a wildfire x solar curve, multi-subsystem damage treatment, or why the current scaffold must withhold numerical outputs. |
| [`wind_tornado_wind_curve_request_guide.md`](wind_tornado_wind_curve_request_guide.md) | Someone asks for an onshore-wind curve for convective wind, tornado, generic “strong wind,” or hurricane and needs the correct pathway, lifecycle version, inputs, limits, and fail-closed rule. |
| [`strong_wind_solar_curve_request_guide.md`](strong_wind_solar_curve_request_guide.md) | Someone asks for convective/strong wind × solar, fixed-tilt versus tracker treatment, stow/Ucrit, a derecho/hurricane/tornado boundary, value linkage, or how to request and interpret the proposed v2 screening curves. |
| [`flood_wind_curve_request_guide.md`](flood_wind_curve_request_guide.md) | Someone needs the exact legacy-source whole-substation flood × wind request and same-substation value rule. |
| [`wildfire_wind_curve_request_guide.md`](wildfire_wind_curve_request_guide.md) | Someone needs either of the two canonical Tier-4 wildfire × wind electrical-unit requests. |
| [`tropical_cyclone_wind_wind_curve_request_guide.md`](tropical_cyclone_wind_wind_curve_request_guide.md) | Someone needs the canonical hurricane × wind source-native request, exact Jaimes selector, axis/range behavior, or partial-coverage boundary. |
| [`tropical_cyclone_wind_solar_v2_curve_request_guide.md`](tropical_cyclone_wind_solar_v2_curve_request_guide.md) | Someone needs to evaluate the noncanonical tropical-cyclone wind × solar model-v2 candidate, choose its Perry/fixed/tracker route, supply qualified architecture-specific inputs and an exact pin, or interpret its five bounded records and withheld outputs. |
| [`tropical_cyclone_wind_solar_v2_1_curve_request_guide.md`](tropical_cyclone_wind_solar_v2_1_curve_request_guide.md) | Someone needs the coverage-complete screening call: seven numeric direct/civil unit DRs, named-value plant physical DR, loss per kWdc, optional scenario dollars, and a direct GSU route. |
| [`flood_substation_curve_request_guide.md`](flood_substation_curve_request_guide.md) | Exact current flood substation inputs, pin, response/value grain and conditional-use limits. |
| [`flood_bess_curve_request_guide.md`](flood_bess_curve_request_guide.md) | Exact current flood bess inputs, pin, response/value grain and conditional-use limits. |
| [`tropical_cyclone_wind_bess_curve_request_guide.md`](tropical_cyclone_wind_bess_curve_request_guide.md) | Exact current tropical cyclone wind bess inputs, pin, response/value grain and conditional-use limits. |
| [`wildfire_bess_curve_request_guide.md`](wildfire_bess_curve_request_guide.md) | Exact current wildfire bess inputs, pin, response/value grain and conditional-use limits. |
| [`source_drop_ingestion_guide.md`](source_drop_ingestion_guide.md) | A new ZIP/source drop arrives and needs inventory, classification, promotion, or staging. |
| [`damage_curve_skill_usage_guide.md`](damage_curve_skill_usage_guide.md) | Deciding whether `damage_curve_skill` should operate directly in-repo or through an outside package/ZIP flow. |

## Rule

Guides explain how to navigate the repo. They should not become a second source of truth. When guide content
names a curve, contract, manifest, or artifact, it should link back to the canonical file.

Every repository-current artifact-index cell must have one canonical request guide. Proposal-only guides may
also exist, but they do not satisfy or alter that current-cell mapping.
