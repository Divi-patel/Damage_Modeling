<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-26
updated: 2026-08-26
status: proposed
scope: One work package per cell — lead artifact, bundle shape, what the curation and runtime notebooks must show for that cell specifically, the Hazard consumer to name, and the gate that closes the package. Facts measured 2026-08-26 from docs/cells and docs/contracts.
-->

# Per-cell work packages

Order follows plan decision NB-D02. A package closes when its `00` and `01` execute headlessly, its two
READMEs exist, the cell README links the pair, the coverage matrix is updated and the structure test passes.
Each package is one bounded unit of work; do not open the next before the gate.

Legend — **bundle**: `damage_curve_record_bundle.v1|v2|v3` · **KAT**: known-answer file in the evaluated
artifact's folder · **consumer**: the Hazard code that pins this artifact (referenced, never imported).

---

## WP-0a · `hail_solar` — repair

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/hail_solar/current/hail_solar__model_v1_0__docs_r7__curve_artifact.json` (`HAIL_SOLAR_PV_MODULE_V1`, v2) |
| Records / units | 3 archetype records (`HAIL_SOLAR_FRAGILE_THIN_GG`, `HAIL_SOLAR_DEFAULT_3P2_GBS`, `HAIL_SOLAR_HARDENED_THICKER`) / 1 failure unit `PV_MODULE_GLASS_CELL` |
| Axis | `HAIL_DIAMETER_MESH_EQUIV`, mm, valid 0–100, clamp-or-warn |
| KAT | `current/known_answer_tests_hail_solar__model_v1_0__docs_r7.json` |
| Consumer | `Hazard_modeling/perils/hail/src/hail/solar/damage.py` (selects `default_3_2mm_glass_backsheet`, value bucket 0.3554); driver `drivers/conus_grid/src/conus_grid/hail/solar_damage.py` pins `HAIL_SOLAR_DEFAULT_3P2_GBS` |
| Repair | re-point loader (r5 → r7); reconcile prose to r7 (denominator / value profiles, strict logistic payload validation, KATs, consumer-scoped tail capability per registry); regenerate 9 figures; update README paths |
| Gate | executes; KATs pass in-notebook; README "Source artifacts" point at `docs/cells/hail_solar/current/` |

## WP-0b · `flood_solar` — repair

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json` (`FLOOD_SOLAR_ELECTRICAL_INUNDATION_V1`, v2) |
| Records / units | 8 piecewise-linear records / 8 units (`FS_INV`, `FS_SWG`, `FS_XFMR`, `FS_COMB`, `FS_SCADA`, `FS_CABLE`, `FS_PVMOD`, `FS_FOUND`) |
| Axis | `FLOOD_LOCAL_DEPTH_COMPONENT_DATUM`: `h_i = max(0, WSE − z_i_crit)`, m, 0–2 m clamp |
| KAT | none published in `current/` (owner gate G4) — the notebook says so |
| Consumer | `Hazard_modeling/perils/flood/src/flood/damage.py`: 7 included units on installed-TIV shares, `FS_FOUND` excluded (velocity axis), computed cap 0.4314 |
| Repair | re-point loader (r3 → r4); reconcile prose to r4; note that the consumer's 7-unit inclusion / exclusion is a **consumer decision**, not the artifact's; regenerate 11 figures |
| Gate | executes; identity block shows r4; README paths current |

---

## WP-1 · Shared scaffolding

`notebooks/_shared/repo_paths.py` · `notebooks/_templates/{00,01}_*.ipynb` + README ·
`tests/test_notebook_coverage.py` · `scripts/reference_helpers/execute_notebooks.py`. Gate: test and runner
pass over the two repaired pairs. Details: [`notebook_contract.md`](notebook_contract.md).

---

## WP-2 · `tropical_cyclone_wind_wind`

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/tropical_cyclone_wind_wind/current/tropical_cyclone_wind_wind__model_v1_2__docs_r2__curve_artifact.json` (`TROPICAL_CYCLONE_WIND_WIND_JAIMES_TOWER_SCREENING_V1_2`, v3, 1 pathway) |
| Records / units | Jaimes source selectors + one canonical-5-MW tower proxy route (`TCWW_JAIMES_3P3MW_AS_CANONICAL_5MW_TOWER_PROXY_V1`, unit `WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT`) / 10 units; tower = 16 % of TIV covered, 84 % withheld |
| History to narrate in `00` | `CHANGELOG.json` + `archive/model_v1_0__docs_r1/`, `archive/model_v1_1__docs_r1/`: v1.0 three Jaimes selectors → v1.1 rotor+nacelle+tower "63 % covered" → v1.2 tower-only 16 %; why the 63 % route was superseded |
| KAT | `current/known_answer_tests_tropical_cyclone_wind_wind__model_v1_2__docs_r2.json` |
| Consumer | `Hazard_modeling/perils/hurricane/src/hurricane/damage_wind.py` (expects the v1.2 code, curve and failure unit above); `drivers/conus_grid/src/conus_grid/hurricane/wind_farm*.py` |
| `01` specifics | `pathways[0]` resolver; evaluate the tower record on its pathway axis; withheld table (9 units) with reason codes; same-unit value rule; KATs |
| Gate | executes; banner-free (canonical); cell README links |

## WP-3 · `tropical_cyclone_wind_solar` *(owner gate G3)*

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/tropical_cyclone_wind_solar/proposed/tropical_cyclone_wind_solar__model_v2_1__docs_r1__curve_artifact.json` (`TROPICAL_CYCLONE_WIND_SOLAR_SCREENING_COMPLETE_V2_1_PROPOSED`, v3, 1 pathway + `site_facility_hazard_axis`) — **NONCANONICAL**; no `current/`, no index entry |
| Records / units | 10 records / 11 units: Perry compatibility record, fixed / tracker array records, five Tier-4 site-facility records (foundation, power/collection, GSU, SCADA, civil) |
| Preserved alternatives to link, not evaluate | v0.1 scaffold, v1.0 Perry module screening, v2.0 synthetic-T4 (all under `proposed/`) |
| KAT | `proposed/known_answer_tests_tropical_cyclone_wind_solar__model_v2_1__docs_r1.json` |
| Consumer | Hazard hurricane × solar CONUS served **below crown**: `drivers/conus_grid/src/conus_grid/hurricane/solar_recipient_release.py` (`…_V2_1_PROPOSED@model_v2_1__docs_r1`), `perils/hurricane/src/hurricane/damage_v21.py` |
| `00` specifics | why the strict evidence gate stayed NO-GO; what the owner-authorized synthetic-T4 candidate adds (named 100 %-physical-value assembly) and does not prove (calibration) |
| `01` specifics | NONCANONICAL banner in Markdown and output; plant DR and loss per kWdc assembly; Tier-4 labelling on every generic parameter; KATs |
| Gate | executes; banner present; cell README links it under a "Proposal notebooks" heading, not "Companion notebooks (current)" |

## WP-4 · `wildfire_solar`

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/wildfire_solar/current/wildfire_solar__model_v1_0__docs_r3__curve_artifact.json` (`WILDFIRE_SOLAR_FSIM_SCREENING_V1`, v2) |
| Records / units | 10 exact FSim-class state tables / 10 units; `screening_engineering_proxy`; no interpolation |
| Axis | `FSIM_CONDITIONAL_FLAME_LENGTH_CLASS_STATE` (source-native categorical class; alternate probability-by-bin field) |
| KAT | `current/known_answer_tests_wildfire_solar__model_v1_0__docs_r3.json` (validator: `validate_wildfire_known_answers`) |
| Consumer | `Hazard_modeling/perils/wildfire/src/wildfire/damage.py`; driver `drivers/conus_grid/src/conus_grid/wildfire/` |
| `00` specifics | why a categorical axis; source registers and claim registers carried in the artifact; legacy / deprecated artifacts listed and why they are not the curve |
| `01` specifics | step plots per unit; **exact-state lookup, not interpolation** — the records are stored as `piecewise_linear` points but the artifact forbids interpolating between FSim classes, so the notebook mirrors `validate_runtime_contracts.exact_state_value` under a Rule-3 "local helper" title and logs the evaluator gap; `wildfire_reference_loss` reproduction; mandatory not-field-calibrated flags |
| Gate | executes; KATs pass |

## WP-5 · `strong_wind_solar`

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/strong_wind_solar/current/strong_wind_solar__model_v1_0__docs_r3__curve_artifact.json` (`STRONG_WIND_SOLAR_V1`, v2) |
| Records / units | 5 `thresholded_logistic_demand` records / 5 units |
| Axis | `SWS_GUST_3S_ARRAY_HEIGHT`: `gust_3s_mph` → `R_eff = (V_3s / V_design)² × demand_multipliers`, valid 0–200 mph |
| KAT | none in `current/` (v2.0 proposal carries one) — say so |
| Consumer | `Hazard_modeling/perils/convective_wind/src/convective_wind/solar_damage.py` (`CURVE_DAMAGE_CODE_ID = "STRONG_WIND_SOLAR_V1"`) |
| `00` specifics | design-gust demand derivation; fixed-tilt vs tracker selectors; the v2.0 convective proposal appears **only** as a "what's next" link (NB-D06) |
| `01` specifics | use `strong_wind_solar_r_eff` and `evaluate_curve_record` (`thresholded_logistic_demand` is a supported form: DR = 0 below `R0`, logistic above) from the evaluator; gust → ratio → DR shown as before/after numbers; exposure contract |
| Gate | executes |

## WP-6 · `wind_tornado_wind`

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/wind_tornado_wind/current/wind_tornado_wind__model_v1_0__docs_r4__curve_artifact.json` (`WIND_TORNADO_WIND_V1`, v2) |
| Records / units | 5 `wind_tornado_logistic_ratio` records / 5 units; `include_in_default_structural_aggregate` per record; `iec_speed_table` (3 classes) |
| Axis | `X_SPEED_RATIO_TO_IEC`: `r = V_3s_hub / Ve50_class` from `hub_height_3s_gust_mps` (accepts 10-m gust upstream field) |
| KAT | none in `current/` (v2.0 proposal carries one) — say so |
| Consumer | `Hazard_modeling/perils/convective_wind/src/convective_wind/damage.py` (`CURVE_DAMAGE_CODE_ID = "WIND_TORNADO_WIND_V1"`) |
| `00` specifics | the IEC class table and why a ratio axis; D50-shift method vs the consumer's co-sampled distribution (scope note in `SCOPE_AND_STORY.md` §10) |
| `01` specifics | ratio transform per IEC class; per-unit curves via `evaluate_curve_record` (`wind_tornado_logistic_ratio` is a supported form; pass `context={"tornado_variant": True}` to show the tornado D50 shift beside the straight-line curve); default structural aggregate vs full set |
| Gate | executes |

## WP-7 · `flood_wind`

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/flood_wind/current/flood_wind__model_v1_0__docs_r1__curve_artifact.json` (`FLOOD_WIND_FEMA_HAZUS_SUBSTATION_SCREENING_V1`, v3, 1 pathway) |
| Records / units | one exact FEMA Hazus-MH 2.1 whole-substation depth-damage atom / 15 units; every component and wind-specific unit withheld |
| KAT | `current/known_answer_tests_flood_wind__model_v1_0__docs_r1.json` |
| Consumer | none at grid support (Hazard flood CONUS is solar-only, decision JD-FL-22 in the Hazard repo); Hazard runs v3 KATs through its shared loader per the artifact index note |
| `00` specifics | the shared flood-electrical substrate discussion (`docs/plans/flood_wind_shared_electrical/`) and why the legacy assembly curve is not decomposed by assumption |
| `01` specifics | `pathways[0]`; the Hazus table plotted as the source gives it; withheld table with reason codes; same-substation value / exposure rule; KATs |
| Gate | executes |

## WP-8 · `wildfire_wind`

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/wildfire_wind/current/wildfire_wind__model_v1_0__docs_r1__curve_artifact.json` (`WILDFIRE_WIND_PARTIAL_ELECTRICAL_SCREENING_V1`, v3, 1 pathway) |
| Records / units | two exact FSim-class electrical units (`WT_PAD_ELECTRICAL`, `WT_GSU_PROTECTION_CONTROL_DC`) / 12 units; others withheld; Tier-4 |
| KAT | `current/known_answer_tests_wildfire_wind__model_v1_0__docs_r1.json` |
| Consumer | none at grid support |
| `00` specifics | why the strict v0.1 alternative is preserved; mandatory source / assumption acknowledgement; prohibition of whole-farm or annual defaults |
| `01` specifics | step tables for the two units; withheld table; KATs |
| Gate | executes |

## WP-9 · `hail_wind` *(owner gate G3)*

| Item | Value |
|---|---|
| Lead artifact | `docs/cells/hail_wind/proposed/hail_wind__model_v0_1__docs_r1__curve_artifact.json` (`HAIL_WIND_PROPOSED_V0_1`, v1) — **WITHHELD**, `curve_records: []`, `NO_RUNTIME_CURVE` |
| Units | 11 failure units; axis `WITHHELD_PENDING_QUALIFIED_BLADE_CONTACT_DEMAND_BRIDGE` (source-native hail descriptors kept separate from a future turbine-local contact-demand bridge) |
| KAT | `proposed/known_answer_tests_hail_wind__model_v0_1__docs_r1.json` (tests the withholding) |
| Consumer | none |
| `00` specifics | the evidence gate: seven reviewed sources, nine governed claims (docs r2), no same-blade disposition / economic atom; rejection of the mislabeled legacy real-estate curve |
| `01` specifics | WITHHELD banner; assert zero records; run KATs; **no plot**; list what evidence would reopen numerical promotion |
| Gate | executes; banner present |

---

## Close-out (Phase 6)

Matrix 10/10 · optional `notebooks/00_library_overview.ipynb` over the artifact index (every current
response on its native axis, one panel per cell) · `AGENTS.md` / `docs/README.md` rows · task-history
handoff · plan `done`, discussion `settled`.
