<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
-->

# Decision log — flood_real_estate model v0.1 / docs r1

All entries are **proposed** on 2026-10-11 by JL for this scaffold. None is owner-accepted yet. Items marked
*owner* need the reviewer (or the platform) before they can be settled.

| ID | Decision | Reason | Alternatives considered | Revisit trigger |
|---|---|---|---|---|
| D-FRE-01 | One cell, `flood_real_estate`, for all three asset types. The reference building is a selector on one failure unit. | Same mechanism, axis, source libraries and denominator across the three types. Real estate is one asset category (doc 06). Mirrors `hail_solar` archetype selectors. | Three cells (`flood_residential`, `flood_commercial`, `flood_industrial`). | A type needs a different mechanism, axis, or value boundary. |
| D-FRE-02 | Model the structure only, as a fraction of **replacement cost new**. Land, contents, depreciation and market value are excluded. | The Hazus and NACCS ordinates are % of structure replacement value; the denominator must match. | Market or assessed value; depreciated value. | Owner chooses a different reporting basis (then convert explicitly, never silently). |
| D-FRE-03 | One whole-building curve per reference building for flood v0.1/v1. | The sourced curves are whole-building. Doc 06 accepts this as a deliberate v1 exception. Precedent: `flood_wind` whole-substation atom. | Component split (structure / roof / walls / services). | A component-level flood source is curated. |
| D-FRE-04 | One still-water pathway, `flood_inundation_contact`, for riverine, pluvial and coastal water. | Same physical mechanism. `flood_solar` and `flood_wind` do not split by flood source; the pathway-splitting guide separates mechanisms, not peril names. | Separate coastal pathway. | Coastal water needs a different axis or mechanism (see D-FRE-06). |
| D-FRE-05 | Water type is an event-time conditioner: freshwater → Hazus default (Table 5-2); coastal surge → NACCS 2015; unknown → withhold. | The two libraries were built for different water and settings. Unknown withholds rather than guessing, as `flood_wind` does for salt or unknown water. | One library for all water; default unknown to Hazus. | Hazard cannot supply water type; or a single national library is adopted. |
| D-FRE-06 | Declare `flood_wave_velocity` (waves, fast flow, scour) as a separate, deferred pathway. | Different mechanism and axis. Mirrors the `flood_solar` scour proxy and `flood_wind` D-FW-07. | Fold waves into coastal curves. | Coastal V-zone or velocity curves are curated. |
| D-FRE-07 | Axis = depth above first finished floor, in ft; outside the published range withholds. | This is the native axis of both libraries. It makes first-floor height an explicit input, so elevation measures later become a parameter change (the reviewer's ask, 2026-10-05). | Depth above grade with a baked-in floor height. | — |
| D-FRE-08 | Choose candidate curves by the **Hazus default per occupancy (Table 5-2)**, not by picking among class-specific curves. | Class curves for one occupancy disagree widely (warehouse structure curves range 1%–62% at 4 ft). The defaults are Hazus's own averages across classes, which makes the choice defensible. | Hand-pick class curves; New Orleans salt/fresh-water curves. | Validation (e.g. NFIP claims) shows a default is biased for our reference building. |
| D-FRE-09 | Building subsystem and component names (`BUILDING`, `BUILDING_STRUCTURE_ASSEMBLY`, `CONTENTS`) are proposals. *Owner: platform / reviewer.* | The platform vocabulary has no building subsystem. Standard 24 requires an exact code join. | Reuse `CIVIL_INFRA`. | Platform codes are issued. |
| D-FRE-10 | Platform type labels (Hotel → Commercial, Warehouse → Industrial) do not affect the curve; the curve keys on the recorded Hazus occupancy. *Owner: reviewer with stakeholders (doc 06 check 4).* | The labels decide routing on the platform, not vulnerability. | — | Labels change. |
| D-FRE-11 | The legacy `Real Estate_Hail` array is not evidence for this or any future real-estate cell. | It was rejected in `hail_wind` as a mislabelled, unit-inconsistent array. | — | — |
| D-FRE-12 | Contents are deferred as a separate failure unit, not folded into the structure ratio. | A different value bucket and different Hazus curves; folding them in would mix denominators. | Include contents in v1. | Owner asks for contents. |
