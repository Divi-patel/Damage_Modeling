---
author: "owner-directed (Divy) · agent-researched"
created: 2026-10-16
updated: 2026-10-16
status: settled
scope: Repository-grounded inventory of existing substation-related Damage across the five Hazard families; research evidence, not standalone admission.
---

# Which hazards already have substation Damage work?

**Flood, Hurricane wind and Wildfire have numeric substation-related candidates.** Older Hazard Wind
calculations also included coarse substation assumptions for Strong Wind and Tornado, but the current
governed models do not provide a qualified standalone station response for those pathways. Hail's
current Solar response is for modules. None of these findings establishes a standalone station grid.

This answers the owner's October 16 request to plan beyond a single Flood layer. It distinguishes
physical relevance, numeric availability, actual consumer use and admission for our new target. The
[file receipt](verification/cross_hazard_inventory.json) captures inspected artifact IDs, unit treatments,
paths and exact hashes, plus the Hazard consumer files. The receipt is research metadata, not a runtime registry.

## Inventory at the reviewed checkout

| Family / source | What is actually present | Consumer/reuse conclusion |
|---|---|---|
| Flood / Solar v1.0 docs r4 | `FS_SWG` switchgear and `FS_XFMR` main-transformer-labelled numeric responses | Hazard's Solar adapter maps both to the existing Solar substation value row. Component datum/value assumptions require transfer review; a solar-plant value share is not the station budget |
| Flood / Wind v1.0 docs r1 | `FW_HAZUS_GSU_SUBSTATION_ASSEMBLY`, a source-native whole-substation depth-damage function | Strong assembly reuse candidate; component records remain withheld. Freshwater, grade-depth, source range and same-assembly denominator restrictions apply. Current capability withholds annual metrics |
| Hurricane wind / Solar v2.1 docs r2 | `PV_GSU_SUBSTATION` and `TCWS21_GSU_SUBSTATION_SCREENING_T4_ORDERED_STATES` | Numeric GSU/switchyard/protection/control screening response. Hazard's v2.1 consumer includes it and the Solar value adapter assigns `Solar_Map:8`. Its ordered-state parameters are Tier-4 expert judgment, not observed station loss calibration |
| Hurricane wind / Wind v1.2 docs r2 | `WT_GSU_SUBSTATION` is explicitly `withheld_not_zero` | The Wind tower response is not another station candidate. Do not infer coverage from a named unit |
| Wildfire / Solar v1.0 docs r3 | `WSV1_MV_EQUIPMENT_THERMAL` covers transformer/switchgear as an engineering screening proxy | Hazard's Solar value adapter maps it to `Solar_Map:8`. It uses source flame-length classes; it is neither a detailed station heat-transfer model nor automatically transferable to the full station value |
| Wildfire / Wind v1.0 docs r1 | Numeric `WT_GSU_PROTECTION_CONTROL_DC` response; main transformer, switchgear/bus and cable-termination responses withheld | Reusable lead for that specific package only. The separate numeric pad-electrical unit is not a main-station assembly. Annual metrics are currently withheld |
| Strong Wind / Solar v1.0 docs r3 | Tracker/racking/module attachment/foundation plus exposed SCADA units | No dedicated GSU/substation response. Proposed Solar v2.0 also withholds the broader electrical/substation package |
| Strong Wind and Tornado / Wind v1.0 docs r4 | Turbine structural response and an unresolved turbine power-electronics seam | Hazard's current `convective_wind/damage.py` evaluates the structural aggregate, not a station curve. Proposed v2.0 explicitly withholds the mixed collection/substation electrical unit |
| Historical Strong Wind and Tornado / Wind consumer | A prior hardcoded model allocated 9% of whole-plant TIV to a substation bucket and evaluated gust-space logistics | Prior work exists, but its exposure/value semantics were rejected as a basis for v2 calibration. Preserve as a comparison fixture; do not restore it as an admitted station response |
| Hail / Solar v1.0 docs r7; Wind v0.1 proposal | Solar has `PV_MODULE_GLASS_CELL`; Wind is a noncanonical scaffold without runtime ordinates | No station response found in this reviewed current/proposed inventory. Missing evidence is not proof of zero station damage |

The legacy Wind finding is documented in the
[numerical audit](../../../cells/wind_tornado_wind/proposed/LEGACY_NUMERICAL_AUDIT_wind_tornado_wind__model_v2_0__docs_r1.md).
It is historical evidence, not a claim about the current production response. The existing
[Flood review](01_assembly_reuse_review.md) remains authoritative for its 93-case reproduction, source
limitations and 31-row station-value accounting.

## What reuse does and does not save

Reuse can save curve derivation, source discovery, evaluator work and known-answer tests. It does not
automatically carry over the parent plant's value fraction, turbine/PV spatial exposure, annual permission,
or exact design assumptions. A curve can be applicable to a component in several assets without making
their complete assets interchangeable. A whole-assembly response can also be reused when its scope fits;
component responses are not mandatory if direct assembly evidence is the defensible source grain.

For the new generic canonical station, retain the exact physical reference and map each selected response
to compatible value and exposure. The same physical substation is counted once. Do not add a whole-yard
response to overlapping transformer, switchgear or control responses for the same event. Conversely, do
not label a protection/control-only result as full-station damage.

Annual capability must be qualified for each adopted record. Solar Hurricane/Wildfire consumer machinery
is useful evidence of an integration pattern, not permission to remove Flood/Wind or Wildfire/Wind's
explicit annual withholding. A deterministic conditional damage ratio can participate in a stochastic
annual Hazard model, subject to that admission and to validated frequency, exposure, value and caps.

## Verdict and next work

The reuse-first direction is justified, but readiness differs by hazard. Recommend **Flood → Hurricane
wind → Wildfire → Strong Wind → Tornado → Hail** as the work queue. Strong Wind/Tornado are the two
branches of one Convective Wind family. This is a readiness-based recommendation, not a loss ranking.
Flood coastal/salinity and other within-family gaps remain explicit follow-on work.

The [Hazard roadmap](../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/04_multi_hazard_roadmap.md)
owns sequence, M0–M4/CONUS milestones, Total and dashboard integration. Damage's
[execution plan](../../../plans/substation_damage/README.md) owns response qualification and release.
Record a new decision if evidence changes the sequence; do not silently promote a current plant response
to a standalone station curve. This inventory is settled as an October 16 checkpoint; scientific transfer
and all new station releases remain open.

No curve ordinates, capabilities, scientific versions, canonical indices or consumer pins changed in this
review. Numerical responses outside the existing Flood reproduction were inspected, not re-executed or
newly validated. Current/proposed files and production source were reviewed; the search is not a claim
that every archived notebook, remote branch or unpublished analysis has been exhaustively inspected.

## October 17 follow-through

The preceding inventory remains the October 16 source-discovery checkpoint. Subsequent target qualification
is recorded separately: [Hurricane station binding](../../../contracts/hazard_handoff/substation_hurricane_screening_v1/README.md),
[Wildfire electrical binding](../../../contracts/hazard_handoff/substation_wildfire_screening_v1/README.md), and
[Strong Wind / Tornado direct-wind binding](../../../contracts/hazard_handoff/substation_convective_wind_screening_v1/README.md).
The last is an explicit T4 cross-hazard mechanism transfer with Tornado-only mechanisms withheld; it does
not revive rejected legacy logistics or create intrinsic source calibration. Existing canonical curves
remain unchanged. The owner excluded Hail from the first delivery; missing station Hail evidence is not zero risk.
