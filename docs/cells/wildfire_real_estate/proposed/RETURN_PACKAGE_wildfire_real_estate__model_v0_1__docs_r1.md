<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# Return package for Hazard — wildfire × real estate, model v0.1

The Damage return for wildfire on the three Hazard reference profiles r1, in the fields the profile handoff asks
for: one card per profile. Everything is a **noncanonical proposal** (model v0.1 / docs r1, promotion gate blocked);
nothing is admitted at runtime. The binding table is
[PROFILE_BINDING](PROFILE_BINDING_wildfire_real_estate__model_v0_1__docs_r1.csv).

## 1. Summary

| Profile | Record | Applicability |
|---|---|---|
| `re_house_1s_wood_slab` | `WFRE_RES_WRC_SHRUB` | exact match: USFS home response, shrub |
| `re_warehouse_1s_steel_slab` | `WFRE_IND_WRC_SHRUB_X0_8` | qualified proxy: 0.8 × house (CAL FIRE same-fire ratio, T4 transfer) |
| `re_office_3s_slab` | `WFRE_OFF_WRC_SHRUB_X0_9` | qualified proxy: 0.9 × house (CAL FIRE same-fire ratio, T4 transfer) |

Shared by all three cards:

| Item | Content |
|---|---|
| Profile pin | Hazard reference profiles **r1**, `aamani-ai/Hazard_Modeling` commit `8b0d61c88fbcf85daa1c098516cee22398cdb524`, `reference_candidates.yml` (git blob `a74fb72b0a2edce593b5505e0fd8852f4c0253f8`); source WFRE-S004 |
| Damage artifact | `wildfire_real_estate` model v0.1 / docs r1, [`wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json`](wildfire_real_estate__model_v0_1__docs_r1__curve_artifact.json) (sha256 in the [validation report](VALIDATION_REPORT_wildfire_real_estate__model_v0_1__docs_r1.md)), branch `cell/wildfire-real-estate` of `aamani-ai/Damage_Modeling` |
| Pathway, unit | `wildfire_building_exposure` (embers, radiant heat, flame contact and building-to-building spread in one response); failure unit `WFRE_BUILDING_STRUCTURE` (contents withheld) |
| Demand | `conditional_flame_length_class_state`: exact FSim class state 0–6 from USFS RDS-2016-0034-3 (0 = no event; 1 < 2 ft … 6 12+ ft), with `source_wildfire_product_id = USFS_RDS_2016_0034_3_270M`. Burn probability is frequency and never enters the damage call |
| Domain | Integers 0–6 by exact lookup; fractional, non-numeric or out-of-range → error `INVALID_CLASS_STATE`; burn probability in the call → error |
| Output | Conditional expected repair cost / structure replacement cost new given a fire at the building location in that class (USFS relative structure loss, read as a repair-cost ratio); not an ignition or destruction probability |
| Uncertainty | Point value only; lifeform and building-factor ranges in [SENSITIVITY](SENSITIVITY_wildfire_real_estate__model_v0_1__docs_r1.csv), not sampleable. Real outcomes are near all-or-nothing (92% of damaged CAL FIRE houses were destroyed) |
| Value | Structure replacement cost new of the same building (shared with flood, hurricane and convective); covered fraction of the profile budget not stated by the source (Hazard's call); contents, land, site works and BI excluded |
| Overlap | One response covers all wildfire mechanisms; all perils on one building in one event ≤ 100% of structure value (consumer) |
| Consumer probe | Hazard `damage_loader.py` (main `08748ae5`, blob `4bdadaa1`): 30 of 44 known-answer requests agree, including every priced and withheld value; two real differences (§6, items 1–2) |
| Reproduce | `wildfire_real_estate_dins_check.py`; `derive_wildfire_real_estate_curves.py`; `wildfire_real_estate_nri_check.py`; `build_wildfire_real_estate_v0_1_package.py`; `wildfire_real_estate_profile_binding.py`; `validate_wildfire_real_estate_v0_1_package.py` |
| Missing profile detail | Fuel lifeform (tree, shrub, grass) at the location is not delivered; shrub is used everywhere |

## 2. Card — `re_house_1s_wood_slab`

| Field | Content |
|---|---|
| Applicability | USFS Wildfire Risk to Communities response for a home (shrub), used directly. The profile (wood frame, vinyl siding, asphalt shingles, vented attic without ember-resistant vents, no declared vegetation buffer) matches the CAL FIRE house group; no mitigation credit |
| Evidence | WFRE-S001 (USFS response), S002 (CAL FIRE level check), S003 (FSim classes); WFRE-C001, C004, C008, C012 |
| Values by class (< 2, 2–4, 4–6, 6–8, 8–12, 12+ ft) | 20%, 35%, 50%, 65%, 80%, 95% |
| Uncertainty | Tree lifeform +5 points; grass −10 to −15 points. CAL FIRE houses of this type lost 0.29–0.65 on average depending on which fires are counted |
| Yearly loss vs NRI | 0.046% of value per year in the median cell (3.0× NRI); 2.0× nationally |

## 3. Card — `re_warehouse_1s_steel_slab`

| Field | Content |
|---|---|
| Applicability | 0.8 × house. CAL FIRE: inside the same fires, metal-wall metal-roof commercial buildings lost 0.79 times as much as those houses (258 buildings, 38 fires; 90% range 0.61–0.99). Size (100,000 ft²), sprinklers and the eight overhead doors are not resolved by CAL FIRE |
| Evidence | WFRE-S001, S002, S003; WFRE-C009, C010 |
| Values by class | 16%, 28%, 40%, 52%, 64%, 76% |
| Uncertainty | Factor 0.3 (pooled over all fires) to 1.0: 6–29% to 20–95% |
| Yearly loss vs NRI | median cell 2.4×; 1.6× nationally |

## 4. Card — `re_office_3s_slab`

| Field | Content |
|---|---|
| Applicability | 0.9 × house. CAL FIRE: inside the same fires, multi-storey stucco/brick/cement commercial buildings lost 0.93 times as much as those houses (204 buildings, 17 fires; 90% range 0.66–1.38). TPO roof, 33% glazing and sprinklers are not resolved |
| Evidence | WFRE-S001, S002, S003; WFRE-C009, C010 |
| Values by class | 18%, 31.5%, 45%, 58.5%, 72%, 85.5% |
| Uncertainty | Factor 0.4 (pooled) to 1.0 |
| Yearly loss vs NRI | median cell 2.7×; 1.8× nationally |

## 5. Short example — warehouse, class 4 (6 to < 8 ft)

```text
request  : pathway_id = wildfire_building_exposure, reference_building_id = RE_IND_WAREHOUSE,
           source_wildfire_product_id = USFS_RDS_2016_0034_3_270M,
           failure_unit_id = WFRE_BUILDING_STRUCTURE, conditional_flame_length_class_state = 4
record   : WFRE_IND_WRC_SHRUB_X0_8 (state 4)
DR       : 52% of structure value
dollars  : 0.52 × $11.0M = $5.72M, if Hazard qualifies the full budget as covered
```

## 6. Items for the Hazard team

1. **Generic loader, fractional class.** The exact-integer class rule in `damage_loader.py` applies only when
   `cell_id == "wildfire_wind"`; for this cell a state of 2.5 is interpolated (0.425) instead of rejected. Key the
   rule on the axis (e.g. `FSIM_CONDITIONAL_FLAME_LENGTH_CLASS_STATE_SCREENING`) rather than the cell ID.
2. **Generic loader, burn probability.** A `burn_probability` field in the damage call is ignored by the generic
   loader; Hazard's own wildfire consumer rejects it. The same guard is needed for this cell.
3. **Fire rate at building locations.** The NRI check is 2.0× nationally but 4.7× in the East (median cell, house).
   Hazard's rate is the burn probability of the cell's burnable land, while buildings sit mostly in developed land;
   the all-pixel rate lowers the national ratio by about 10%. A developed-area exposure rate (e.g. WRC's oozed burn
   probability or exposure type) may suit buildings better.
4. **Lifeform (optional).** A tree / shrub / grass lifeform per cell (LANDFIRE EVT, as WRC uses) would replace the
   shrub default.
5. **Whole-cell coupling.** `p_hit = 1` treats every fire in the cell as reaching the building; fine for the screening
   grid, to be revisited for deep runs.
