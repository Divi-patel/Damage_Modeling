# Hazard_modeling handoff notes

These notes are the implementation-side contract for external M2/M3 notebooks. They are included here because the separate `Hazard_modeling` repository was not part of the uploaded package.

| File | External action |
|---|---|
| `hail_solar_m3_canonicalization.md` | Replace any legacy capex-weighted hail asset curve in M3 with the canonical failure-unit JSON artifact. |
| `wind_tornado_wind_m2_height_bridge.md` | Convert 10m gusts to hub-height gusts before evaluating the wind/tornado wind-farm damage curve. |
| `wind_tornado_wind_model_v2_0_hazard_migration_proposal.md` | Shadow-test the proposed pathway-aware model v2 contract; repair event, height/profile, turbine exposure, value, frequency, hardcoded-curve, and rollback seams before any cutover. Model v1 remains canonical. |
| `strong_wind_solar_model_v2_0_convective_migration_proposal.md` | Shadow-test the proposed convective solar v2 contract with fixed-pressure versus tracker-Ucrit routing, local event/zone exposure, state-aware module/structure cascade, explicit value basis, negative tests, and v1 rollback. |
| `tropical_cyclone_wind_wind_model_v0_1_boundary.md` | Preserve the new TC-wind pathway boundary and fail closed with `NO_RUNTIME_CURVE`; do not load the noncanonical scaffold, reuse convective/tornado curves, or create an ungoverned coastal overlap. |
| `tropical_cyclone_wind_wind_model_v1_0_proposal.md` | Shadow-test the three exact Jaimes expected-DR curves on their source-native axis and atom while withholding value conversion, standard wind-farm units, and scenario/annual/tail loss. No cutover is authorized. |
| `tropical_cyclone_wind_wind_model_v1_0_hazard_migration.md` | Load the canonical bundle-v3 Jaimes source-native turbine/tower pin with exact selector/axis controls; preserve all standard-unit, value, whole-farm, and annual/tail withholding. |
| `tropical_cyclone_wind_wind_model_v1_2_hazard_migration.md` | Load the canonical tower-only proxy with exact v1.2 SHA and identities; bind only 16% tower value, withhold 84%, and reject the archived v1.1 63% route. |
| `tropical_cyclone_wind_solar_model_v0_1_boundary.md` | Preserve architecture-specific solar demand, separate GSU/substation binding, compound-event routing, and fail-closed `NO_RUNTIME_CURVE`; do not load the scaffold or reuse strong-wind/legacy curves. |
| `tropical_cyclone_wind_solar_model_v1_0_proposal.md` | Shadow-test the one Perry source-cohort visible-module-hardware screening proxy with exact axis, selector, range, limitation-flag, and withholding rules. Strict evidence review still favors v0.1; no cutover is authorized. |
| `tropical_cyclone_wind_solar_model_v1_0_docs_r2_no_cutover.md` | Apply the deep-curation no-cutover result: Visual Crossing is known only at study level; ordinary Hazard 3-second gust, trackers, severe tail, generic arrays, value binding, and scenario/annual/tail use remain prohibited. |
| `tropical_cyclone_wind_solar_model_v2_0_synthetic_proposal.md` | Develop only against the noncanonical five-record research contract: preserve the Perry compatibility route, route fixed tilt and exact-system-qualified trackers to four cell-local synthetic Tier-4 records, and keep unsupported units plus value/full-plant and annual/tail outputs withheld. No cutover is authorized. |
| `tropical_cyclone_wind_solar_model_v2_1_screening_proposal.md` | Integrate the coverage-complete screening contract: seven numeric direct/civil unit DRs plus a named-value `physical_damage_assembly.v1` with plant DR, loss per kWdc, and optional scenario dollars. Annual/tail metrics remain consumer-owned; no canonical cutover is authorized. |
| `flood_wind_model_v0_1_boundary.md` | Preserve component-local flood exposure, ownership/value separation, and fail-closed `NO_RUNTIME_CURVE`; do not load the scaffold, reuse flood-solar/legacy curves, or leave the independent M4 bypass out of a future migration. |
| `flood_wind_model_v1_0_proposal.md` | Shadow-test the exact legacy FEMA whole-substation screening table on its source-native grade-depth axis while keeping component/wind-unit coverage, value binding, annual/tail outputs, and consumer cutover withheld. |
| `hail_wind_model_v0_1_boundary.md` | Apply the docs-r2 strict NO-GO decision while preserving the unchanged docs-r1 machine scaffold, source-hail versus blade-contact-demand semantics, per-turbine/BOP/GSU spatial grains, and fail-closed `NO_RUNTIME_CURVE`; do not load the scaffold or reuse solar, chronic-erosion, or legacy real-estate curves. |
| `wildfire_wind_model_v0_1_boundary.md` | Preserve regional-wildfire versus delivered thermal/firebrand/residue demand, one shared event across per-turbine and separately located BOP/GSU subjects, and fail-closed `NO_RUNTIME_CURVE`; do not load the scaffold or reuse solar, building, internal-fire, or legacy wind curves. |
| `wildfire_wind_model_v1_0_partial_screening_proposal.md` | Review or shadow-test two cell-local Tier-4 electrical-unit records on the exact FSim categorical state, with no whole-farm/value/annual output and no canonical cutover. |
| `flood_wind_model_v1_0_hazard_migration.md` | Load the canonical bundle-v3 legacy-FEMA whole-substation partial-screening pin; preserve water/range/unit withholding and exact same-substation value rules. |
| `wildfire_wind_model_v1_0_hazard_migration.md` | Load the canonical bundle-v3 two-unit Tier-4 electrical screening pin; preserve exact FSim/source/assumption guards, nulls, and same-unit value rules. |
| `m3_to_m4_distribution_ready_emit.md` | Ensure the parquet/schema seam can carry scalar and distribution emit objects. |
| `wildfire_solar_research_to_runtime_handoff__model_v0_1__docs_r2.md` | Keep FSim wildfire screening separate from physical solar loss; isolate the current legacy proxy and fail closed until a canonical wildfire_solar model is released. |
| `wildfire_solar_model_v1_0_hazard_migration.md` | Replace the legacy midpoint/Byram/logistic proxy with the canonical exact-FSim-state screening model, explicit value linkage, KATs, SHA pin, and limitation flags. |
| 01 | 2026-10-16 | owner-directed (Divy) · agent-drafted | Hazard | [Substation Flood conditional binding](substation_flood_screening_v1/README.md) | Unchanged canonical assembly response, 31-row value/exposure binding and conditional point-proxy guards; annual withholding retained |

The canonical `wildfire_solar_model_v1_0_hazard_migration.md` supersedes that cell's v0.1 no-runtime
instruction for execution; its v0.1 file remains the research and promotion audit. For every explicitly
noncanonical v1 proposal listed above, the corresponding v0.1 boundary remains the operational execution
rule until a separate canonical promotion and cutover decision.
