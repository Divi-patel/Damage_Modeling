# Version registry — portable package v2.5 + repository-current contracts

This registry separates **package release labels** from **semantic damage-model versions**.

The latest portable package remains the v2.5 implementation-hardening release. Repository-current runtime
state has advanced to `2026-08-30.hurricane-solar-screening-v2-1-docs-r2-v3`: the five existing bundle-v2 pins remain
unchanged, while bundle v3/capability v3/emit v2 also serve canonical `flood_wind`, `wildfire_wind`,
`tropical_cyclone_wind_wind`, and `tropical_cyclone_wind_solar` screening packages.

On 2026-08-30 tropical-cyclone wind × solar model v2.1 moved into `current/` after the exact proposal passed
the Everglades Hazard M0→M4 experiment and proposal-to-current numerical parity. Docs r2 is current: it fixes
forward docs r1's inherited `NONCANONICAL_MODEL_V2_1` KAT label without changing any curve, value or numerical
output. Ten failure-unit curves and the named physical-value assembly remain canonical at screening grade.
Tier-4 response assumptions, the nonprobabilistic scenario envelope and wind-only exclusions remain explicit;
annual/tail metrics remain Hazard-owned.

On 2026-08-09 tropical-cyclone wind × wind moved from its pressure-tested v1 proposal into `current/` without
broadening the science. It contributes three exact Jaimes selectors for one quarantined source-native
turbine/tower atom. Generic turbine transfer, remaining wind-farm units, value binding, whole-farm loss, and
annual/tail metrics remain withheld.

On 2026-08-08 the two wind missing pieces moved from review proposals into `current/`. Flood contributes one
legacy FEMA whole-substation source atom; wildfire contributes two Tier-4 electrical units. All unsupported
units remain withheld, same-unit value/exposure is mandatory for scenario dollars, and annual/tail metrics
remain consumer-owned.

On 2026-07-20, all five cells gained the complete cell-owned basics set. Human documentation advanced to
hail r8, flood r5, wind/tornado r5, strong-wind solar r4, and wildfire r4. No runtime artifact or contract was
published for these docs-only changes; consumers remain pinned to the artifact-index versions below.

On 2026-07-29, `tropical_cyclone_wind_solar` advanced from the partial model-v2.0 proposal to a noncanonical
model-v2.1/docs-r1 coverage-complete screening proposal. It preserves the five v2.0 records, adds five
site-facility Tier-4 records, and publishes a fully reconciled named-value plant physical DR/scenario-loss
view. Annual/tail metrics remain consumer-owned. Model v0.1, v1.0, and v2.0 remain preserved; `current/`, the
artifact index, the cell changelog, package releases, and Hazard runtime remain unchanged.

> Some source dossiers and workbooks still carry earlier labels (`v1_3`, `v1_0`, or `docs_r1`) for continuity.
> The artifact index is the authoritative repository-current runtime pointer. Package v2.5 remains the portable
> baseline and must not be used by itself as a cell-runtime pin.


---

## Current cells

| Cell folder | Current semantic damage-model version | Human / runtime docs revision | Current status | Repository-current contract note |
|---|---:|---:|---|---|
| `hail_solar` | **model v1.0** | human docs r8; runtime docs r7 | Current; source docs retain `v1_3` labels | Docs r8 adds the three-file basics set. Runtime docs r7 still own the denominator/value profiles, strict logistic payload validation, KATs, and consumer-scoped tail capability. |
| `flood_solar` | **model v1.0** | human docs r5; runtime docs r4 | Current | Docs r5 adds the three-file flood/elevation basics set; runtime docs r4 remain canonical. |
| `wind_tornado_wind` | **model v1.0** | human docs r5; runtime docs r4 | Current | Docs r5 adds the three-file basics set and keeps the noncanonical v2 proposal separate; runtime docs r4 remain canonical. |
| `strong_wind_solar` | **model v1.0** | human docs r4; runtime docs r3 | Current derived cell | Docs r4 adds the three-file basics set and documents validation gaps/proposal boundaries; runtime docs r3 remain canonical. |
| `wildfire_solar` | **model v1.0** | human docs r4; runtime docs r3 | Current screening engineering proxy | Docs r4 adds the three-file basics set; runtime docs r3 retain exact FSim-class tables, value linkage, KATs, and screening flags. |
| `flood_wind` | **model v1.0** | docs r1 | Current partial screening | One exact FEMA Hazus-MH 2.1 facility-substation atom; all component/wind units withheld; bundle v3 pin and KATs. |
| `wildfire_wind` | **model v1.0** | docs r1 | Current Tier-4 partial screening | Two exact FSim-state electrical-unit curves; all other units withheld; bundle v3 pin and KATs. |
| `tropical_cyclone_wind_wind` | **model v1.2** | docs r2 | Current owner-approved tower-only screening | Jaimes parameters and source selectors reproduce; the canonical-5-MW proxy covers tower value only (16% of TIV); remaining 84% withheld; old 63% route superseded. |
| `tropical_cyclone_wind_solar` | **model v2.1** | docs r2 | Current owner-approved coverage-complete screening | Docs r2 corrects the result-status label only; ten failure-unit curves and a named physical replacement-value assembly produce plant DR, loss per kWdc and optional event dollars; Tier-4 assumptions and wind-only scope remain explicit. |

---

## Active noncanonical proposals

| Cell folder | Proposed semantic model | Proposed documentation | Status | Current-runtime effect |
|---|---:|---:|---|---|
| `wind_tornado_wind` | model v2.0 | docs r1 | Pressure-tested pathway-aware screening proposal; promotion gates remain blocked | None. Model v1.0/docs r4 remains canonical and is still the artifact-index pin. |
| `strong_wind_solar` | model v2.0 | docs r1 | Convective pathway/architecture-aware screening proposal; T4 numerical envelopes and promotion gates remain blocked | None. Model v1.0/docs r3 remains canonical and is still the artifact-index pin. |
| `hail_wind` | model v0.1 | docs r2 | Independently deep-curated, zero-curve research scaffold; seven-source and nine-claim evidence addenda strengthen mechanism, field-observation, inspection, migration, and acquisition controls, but the strict model-v1 gate remains NO-GO | None. The docs-r1 machine-shaped scaffold is unchanged; no canonical cell, artifact-index entry, package release, schema change, or consumer cutover exists. |

The wind proposal introduces separate `straight_line_convective` and `tornado_direct_hit` pathways, proposed
bundle v3 / emit v2 / capability v3 contracts, an equipment-only ordered-state curve, and explicit withheld
external units. It is not a portable package release, current changelog event, or hurricane curve. See
[`wind_tornado_wind/proposed/README_wind_tornado_wind__model_v2_0__docs_r1.md`](wind_tornado_wind/proposed/README_wind_tornado_wind__model_v2_0__docs_r1.md).

The solar-wind proposal routes one `straight_line_convective` pathway through separate rigid fixed-tilt
pressure and qualified-tracker instability axes; it adds dependency-controlled module/structure records and
explicitly excludes hurricane, tornado and nonconvective wind. See
[`strong_wind_solar/proposed/README_strong_wind_solar__model_v2_0__docs_r1.md`](strong_wind_solar/proposed/README_strong_wind_solar__model_v2_0__docs_r1.md).

The tropical-cyclone wind release reuses the wind-asset anatomy while keeping TC wind distinct. Model v1.2
preserves the source-derived Jaimes curves and binds the named canonical proxy only to
`WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT` and 16% tower value. Standard equipment assembly, foundation,
electrical/GSU/control, civil, support, and the other 84% remain withheld. See
[`tropical_cyclone_wind_wind/current/`](tropical_cyclone_wind_wind/current/README.md).

The flood-wind release keeps the hazard × asset release unit and the asset-neutral flood-electrical method
substrate. Model v1.0 uses the exact legacy FEMA Hazus-MH 2.1 whole-substation response as one quarantined,
mutually exclusive screening atom; component-local disposition/cost remains unsupported, and current Hazus
7.0 disables electric-power loss results. See [`flood_wind/current/`](flood_wind/current/README.md).

The tropical-cyclone wind × solar current release reuses solar anatomy and TC event/pathway semantics while
keeping every parameter decision cell-owned. Model v2.1/docs r2 preserves v2.0's Perry and four array records,
adds five site-facility screening records, and assembles all 877.7957023626668 USD/kWdc of the named physical
replacement profile. The result includes plant physical DR, installed-capex physical loss fraction, loss per
kWdc, and optional scenario dollars. Replacement support is allocated once. The additional records remain
explicit Tier-4 assumptions; annual/tail and BI outputs remain outside the damage layer. Model v0.1 remains
the strict fail-closed alternative, v1.0 the narrow source-derived alternative, and v2.0 the preserved partial
baseline. The immutable proposal remains the rollback and parity reference. See
[`tropical_cyclone_wind_solar/`](tropical_cyclone_wind_solar/README.md) and the
[`model-v2.1 current package`](tropical_cyclone_wind_solar/current/README.md).

The hail × wind proposal separates observed/radar hail descriptors from the future blade-contact demand
bridge and keeps blades, exposed nacelle subjects, towers, turbine-pad electrical, collection, GSU, controls,
civil subjects, and support at their own physical/spatial grains. Public coupon, simulation, degradation, and
repair-cost evidence does not close an occurrence demand → inspected disposition → same-unit cost chain, so
every candidate remains audit-only. Docs r2 also records the developing ISO test route, FM post-hail
inspection workflow, bounded field non-damage observation, active wrong-asset legacy mappings, and exact
consumer migration guardrails. See [`hail_wind/`](hail_wind/README.md).

The wildfire × wind release preserves FSim as source-native screening context without calling it unit heat
flux or firebrand dose. Two explicitly Tier-4 BOP/GSU electrical curves are current; all other units remain
withheld. See [`wildfire_wind/current/`](wildfire_wind/current/README.md).

---

## Package release history summary

| Package release | Main change | Cell model changes? |
|---|---|---:|
| v1.3 | Hail × solar derivation audit package | Hail model already at v1.0 behavior; docs improved. |
| v1.6 | Flood × solar v1.0 derived cell | Yes: flood_solar model v1.0 introduced. |
| v2.0 | Wind/tornado × wind v1.0 derived cell | Yes: wind_tornado_wind model v1.0 introduced. |
| v2.1 | Evidence-ingestion and versioning governance | No. |
| v2.2 | Legacy evidence co-curation ingestion; validation/caveat/model-change distinction added to standard 16 | No. |
| v2.3 | Hazard-pathway scope splitting standard + strong_wind_solar v0.1 scaffold | New scaffold only; no DR curve parameters. |
| v2.4 | Strong wind × solar model v1.0 derived curve package | Yes: strong_wind_solar model v1.0 introduced. |
| v2.5 | Implementation hardening: JSON runtime artifacts, capability declarations, cap-binding gates, field-name alignment, handoff notes | No semantic DR changes. |

Post-package repository contract history is pollable from each cell's `CHANGELOG.json` and the v2 artifact
index. It is not assigned a new package number until a portable release is deliberately assembled.

---

## Repository-current cells outside portable package v2.5

| Cell folder | Semantic model version | Documentation revision | Lifecycle / promotion / review state | Canonical runtime artifact? |
|---|---:|---:|---|---:|
| `wildfire_solar` | model v1.0 | human docs r4; runtime docs r3 | released repository-current screening proxy; model v0.1 scaffold retained as research/rejection audit | Yes, repository-current |
| `flood_wind` | model v1.0 | docs r1 | released repository-current partial screening; legacy FEMA source and all limits retained | Yes, repository-current |
| `wildfire_wind` | model v1.0 | docs r1 | released repository-current Tier-4 partial screening; v0.1 strict scaffold retained | Yes, repository-current |
| `tropical_cyclone_wind_wind` | model v1.2 | docs r2 | released repository-current canonical-Wind-Farm tower-only screening; v1.1 and v1.0 exact archives retained | Yes, repository-current |

The portable v2.5 package does not contain these four later repository-current cells. The artifact index does.
Model v1.0 is deliberately a Tier 4 absolute engineering proxy constrained by Tier 2/3 evidence; it uses exact
source-native categorical states and does not claim a physical FSim-to-heat-flux converter. A future
site-calibrated model remains dependent on local-attack, inspected-disposition, cost, and coverage evidence.

---

## Practical rule

```text
Package version changed ≠ damage curve changed.
Cell damage-model version changed = damage-code behavior changed.
Documentation revision changed = proof trail / contract / implementation wrapper changed, but same inputs produce the same DRs.
v0.1 scaffold = structure accepted but runtime DR not yet parameterized.
v1.0 = first derived runtime curve package for the cell.
```
