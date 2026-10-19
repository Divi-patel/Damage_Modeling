# docs/plans/

Planning home for `damage_modeling` workstreams that have graduated from discussion into a build shape.

The convention mirrors `Hazard_modeling`: exploratory reasoning stays under `docs/extra/discussion/`; when a
direction is stable enough to execute carefully, it gets a folder here with a plan-of-record, decisions log,
and assumptions register.

| Plan | Status | What |
|---|---|---|
| [`bess_damage/`](bess_damage/README.md) | active; owner-directed (Divy), 2026-10-18 | Flood-first BESS curation: first evidence/reuse audit complete; enclosure/PCS candidate next; later size-scaling handoff tracked. |
| [`tropical_cyclone_wind_wind_v1_1_proxy/`](tropical_cyclone_wind_wind_v1_1_proxy/README.md) | owner-approved model-behavior change planned; v1.0 remains current | Build and validate the explicit canonical-5-MW screening proxy, 0.63 covered-value crosswalk and Hazard migration gates. |
| [`hazard_asset_coverage/`](hazard_asset_coverage/README.md) | breadth complete: 10/10 structural, 8/10 repository-current canonical runtime after partial-screening flood_wind, wildfire_wind, and tropical_cyclone_wind_wind v1 releases; TC-wind-solar also has a noncanonical model-v2.1 candidate | Continue depth work one cell at a time; partial canonical status is not complete calibration, and the out-of-queue TC-solar work does not change current pins. |
| [`repo_information_architecture/`](repo_information_architecture/README.md) | initial plan-of-record | Normalize the repo from deliverable-shaped navigation into a shallow, durable documentation architecture without losing provenance. |
| [`flood_wind_shared_electrical/`](flood_wind_shared_electrical/README.md) | phase 2 complete; local v1 proposal noncanonical; shared runtime deferred | Govern the flood-wind cell and asset-neutral flood-electrical substrate while preserving an explicit future migration path. |
| [`strong_wind_solar_completion/`](strong_wind_solar_completion/README.md) | step 1 audit complete; promotion blocked | Harden the existing convective-wind × solar v2 proposal without rebuilding it, close scientific and consumer gates in order, and preserve v1 as canonical until an explicit release decision. |
| [`tropical_cyclone_wind_solar_completion/`](tropical_cyclone_wind_solar_completion/README.md) | owner-authorized noncanonical model-v2/docs-r1 candidate built; promotion blocked | Govern five records—one Perry compatibility record plus four cell-local synthetic-T4 records—while preserving v0.1/v1 and acquiring the evidence required for any promotion. |
| [`solar_wind_normalized_response/`](solar_wind_normalized_response/README.md) | comparison-only candidate v0.1; no runtime authority | Govern the hazard-label-neutral, solar-specific audit fingerprint without treating strong-wind numerical identity as tropical-cyclone evidence or a shared runtime dependency. |

## Workflow

```text
discussion note
  -> plan folder
  -> staged execution
  -> verification
  -> task history / handoff
```

Planning docs are not raw research and are not runtime artifacts. They are the build-facing record of what we
intend to change, why, and how we will verify it.

| **2026-10-16** | [`substation_damage/`](substation_damage/README.md) | owner-directed (Divy) · agent-researched | Divy / Hazard | active | Qualify existing Flood substation response, repair-value scope, governed standalone candidate and conditional/annual consumer proofs; numerical review complete, proxy and denominator unresolved. |
