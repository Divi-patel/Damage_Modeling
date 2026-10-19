<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# wildfire_real_estate curve derivation dossier — model v0.1 / docs r1

How the three proposed records (one per reference building) are derived, what each number rests on, and what was
checked. Decisions: [decision log](DECISION_LOG_wildfire_real_estate__model_v0_1__docs_r1.md). Scope:
[proposal README](README_wildfire_real_estate__model_v0_1__docs_r1.md).

## 1. Scope, asset boundary, and failure mechanisms

The structure of three reference buildings (Hazard profiles r1) when a wildfire burns at their location. Buildings are
lost to wildfire through embers entering vents, eaves and openings or landing on combustible surfaces, radiant heat
breaking glass and igniting siding, direct flame contact, and spread from burning neighbouring buildings. One pathway,
`wildfire_building_exposure`, carries all of them, because neither source separates them (D-WFRE-02).

Out of scope: smoke or ash contamination without fire damage, post-fire debris flow and erosion, power shutoff,
contents, loss of use (D-WFRE-12).

## 2. Failure-unit decomposition and coverage

One numeric unit, `WFRE_BUILDING_STRUCTURE`, at whole-building grain: the USFS response is a whole-structure loss and
the CAL FIRE bands describe the whole structure. `WFRE_BUILDING_CONTENTS` is declared and withheld (not zero).

## 3. Hazard axis and local exposure bridge

Hazard delivers, per cell, a yearly fire rate (λ = −ln(1 − BP), burnable pixels) and the mix of six FSim conditional
flame-length classes given a fire, and looks up damage at the exact class (WFRE-C006). The axis is that exact class
state, 0–6 (0 = no event), in `conditional_flame_length_class_state`, with the FSim product pinned by
`source_wildfire_product_id` — the same contract as `wildfire_wind` (D-WFRE-04).

The USFS response was defined on WRC's 30 m flame-length classes; Hazard's are the 270 m FSim classes. Both use the
same boundaries (< 2, 2–4, 4–6, 6–8, 8–12, 12+ ft; WRC's 4 ft and 8 ft exceedance layers are sums of its classes
above those lengths), so the response is applied class for class as a flagged bridge (WFRE-C005).

The class describes the wildland fire in the cell, not the heat, embers or flame contact at the building. That is
the main limit of any class-based curve (§6).

## 4. Source register summary

| ID | Source | Role |
|---|---|---|
| WFRE-S001 | USFS Wildfire Risk to Communities, 2nd ed. (RDS-2020-0016-2), metadata | Structure response per flame-length class and lifeform (the curve) |
| WFRE-S002 | CAL FIRE Damage Inspection (DINS) master table, 2013–2025 | Building factors (same-fire comparison); level check for the house |
| WFRE-S003 | USFS FSim 270 m (RDS-2016-0034-3), metadata | Flame-length class definitions (axis) |
| WFRE-S004 | Hazard reference profiles r1 | Building identities, construction, budgets |
| WFRE-S005 | Hazard wildfire layer (code and M1 data) | Axis, fire rate, class mix, coupling; inputs for the NRI check |
| WFRE-S006 | FEMA National Risk Index, Dec 2025 | Order-of-magnitude check |
| WFRE-S007 | Syphard & Keeley 2019, *Fire* 2(3):49 | Context: what drives building loss |
| WFRE-S008 | Repository wildfire cells and station binding | Axis and contract precedent |

## 5. Claim/parameter provenance map

| Number | Claims | Tier |
|---|---|---|
| House loss per class (20 … 95%) | C001–C003 | T3 (agency response on Hazard's axis; stated judgment, checked against CAL FIRE) |
| Loss value read as repair cost / replacement cost new | C004 | T4 reading |
| WRC classes = FSim classes | C005 | T4 bridge (same boundaries) |
| Shrub default | C007 | T4 (JL decision; no Hazard lifeform) |
| Warehouse 0.8, office 0.9 | C009, C010 | T3 ratio (CAL FIRE same-fire); T4 transfer to the reference buildings |
| Axis, states, state 0 = 0 | C006, C014 | T2 |

## 6. Evidence pressure test

**Is a curve by flame-length class supportable?** Partly. The USFS response is the only published building loss on
these classes, and it is used nationally, but its numbers are stated assumptions without a published derivation
(WFRE-C003). Field studies find that building features that keep embers out matter more than defensible space and
that any single factor explains little; many "fire-safe" houses were destroyed (WFRE-C011). Outcomes are close to
all-or-nothing: of the CAL FIRE houses that were damaged at all, 92% were destroyed (WFRE-C008). So the class
changes the *odds* that a building is lost more than the *size* of a partial loss, and a class-based curve is a
screening average, not a prediction for one building. JL chose it over a flat loss because it keeps Hazard's
severity information (D-WFRE-03).

**House level.** The USFS shrub curve gives 0.42 of structure value on average over Hazard's class mixes (NRI
check, `mean_conditional_dr`). CAL FIRE houses of the profile's type (wood or vinyl siding, asphalt roof) lost 0.29 to
0.65 on average, depending on which fires are counted (all fires 0.59; fires that recorded undamaged houses well 0.29;
without the Camp Fire 0.33; without the 2025 Los Angeles fires 0.65). The two agree in level; neither calibrates the
other.

**Building factors.** In the same fires, metal-wall metal-roof commercial buildings lost 0.79 times as much as those
houses (258 buildings in 38 fires; 90% range 0.61–0.99) and multi-storey masonry commercial buildings 0.93 times (204
in 17 fires; 0.66–1.38). Pooled over all fires the ratios look like 0.30 and 0.42, but that mostly reflects which
fires hit which buildings: the Camp Fire destroyed thousands of houses and few commercial buildings, and the pooled
ratio swings from 0.27 to 0.60 across subsets ([CAL FIRE comparison](DINS_BUILDING_COMPARISON_wildfire_real_estate__model_v0_1__docs_r1.csv)).
Non-combustible walls do not stop embers entering through doors, vents and glazing, and interiors and steel framing
then fail; the handoff notes that a metal exterior "does not establish zero risk". The CAL FIRE commercial buildings
are smaller and of mixed use; the reference warehouse is larger and sprinklered, which could make it do better
(WFRE-C010), so 0.3 and 1.0 are in the sensitivity table.

**Lifeform.** Tree adds 5 points per class; grass removes 10 to 15. Hazard delivers no lifeform, so shrub is used
everywhere (D-WFRE-05).

## 7. Y-axis and row-level value crosswalk

y = repair cost of the structure / structure replacement cost new of the same building; one failure unit holds 100%
([value crosswalk](VALUE_CROSSWALK_wildfire_real_estate__model_v0_1__docs_r1.csv)). Same value basis as the other
real-estate cells; scenario dollars withheld until the consumer qualifies each budget (D-WFRE-11).

## 8. Site-condition adapter and double-counting matrix

| Overlap | Rule |
|---|---|
| Fire frequency vs damage | Burn probability is frequency (Hazard); it never enters the damage call (D-WFRE-10). |
| Embers, radiant heat, flame contact, building-to-building spread | Inside the one response; no add-on. |
| Defensible space, vegetation, ember-resistant construction | No credit in model v0.1 (D-WFRE-08); the profile has none. |
| Wildfire vs other perils on one building | Together at most 100% of structure value in one event (consumer). |
| Post-fire flooding and debris flow | Not here; a separate hazard if Hazard adds it. |

## 9. Curve-form decision

```text
DR_b(0) = 0
DR_b(k) = factor_b × WRC_shrub(FLP_k) / 100        k = 1 … 6
WRC_shrub = 20, 35, 50, 65, 80, 95;  factor = 1.0 house, 0.8 warehouse, 0.9 office
```

A table of seven exact states, six decimals, in a bundle-v3 `piecewise_linear` record whose evaluator never
interpolates (the same encoding as `wildfire_wind`). One factor at every class, because CAL FIRE records no flame
length.

| State | Class | House | Warehouse | Office |
|---|---|---|---|---|
| 1 | < 2 ft | 20% | 16% | 18% |
| 2 | 2 to < 4 ft | 35% | 28% | 31.5% |
| 3 | 4 to < 6 ft | 50% | 40% | 45% |
| 4 | 6 to < 8 ft | 65% | 52% | 58.5% |
| 5 | 8 to < 12 ft | 80% | 64% | 72% |
| 6 | 12+ ft | 95% | 76% | 85.5% |

Chart: [previews/wildfire_real_estate_v0_1_curves.png](../previews/wildfire_real_estate_v0_1_curves.png).

## 10. Parameter derivation and tiers

See the [parameter tier table](PARAMETER_TIER_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv), the
[USFS response table](WRC_RESPONSE_FUNCTION_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv) and the
[building factor table](BUILDING_FACTOR_TABLE_wildfire_real_estate__model_v0_1__docs_r1.csv).

## 11. Seven-step audit

| Step | Outcome |
|---|---|
| 1. Asset and boundary | Three reference buildings (profiles r1); structure only. |
| 2. Failure units | One whole-building unit; contents withheld. |
| 3. Y-axis and value basis | Repair cost / structure replacement cost new. |
| 4. Value split | One row, 100% of structure value; components not itemized by the source. |
| 5. Allocation by unit and zone | Whole building; no zones. |
| 6. Site-condition adapter | Exact FSim class at the location, as delivered; shrub lifeform; no mitigation credit; no hit probability added. |
| 7. Apply curves, reconcile or withhold | Numeric per building; contents withheld; invalid states, missing selectors and a burn probability in the call fail. |

Outcome: complete at screening grade with T4 links stated (value reading, class bridge, lifeform default, factor transfer).

## 12. Derivation rationale

USFS publishes how much of a home it assumes is lost at each flame-length class of a wildfire; that is the house
curve. CAL FIRE's inspections show that, inside the same fires, metal and masonry commercial buildings were lost at
about 0.8 and 0.9 times the rate of wood houses; those ratios scale the house curve for the warehouse and office.

## 13. NRI check

Order-of-magnitude check of yearly building loss on Hazard's grid against FEMA's National Risk Index, Dec 2025
([results](NRI_CHECK_wildfire_real_estate__model_v0_1__docs_r1.csv),
[receipt](NRI_CHECK_RECEIPT_wildfire_real_estate__model_v0_1__docs_r1.json); script
`wildfire_real_estate_nri_check.py`). Hazard's own M1 table (sha256 `2d931d87…`, as pinned in its runtime-input
manifest): yearly rate = λ (burnable pixels) × Σ P(class | fire) × DR(class). 12,981 cells with NRI wildfire loss.

| Building | Median cell, % of value per year (×NRI) | National, exposure-weighted (×NRI) | With Hazard's all-pixel rate (×NRI, national) |
|---|---|---|---|
| House | 0.046% (3.0×) | 2.0× | 1.8× |
| Warehouse | 0.037% (2.4×) | 1.6× | 1.5× |
| Office | 0.042% (2.7×) | 1.8× | 1.6× |

NRI median 0.021% per year. Rank correlation with NRI 0.88. Average house damage given a fire over Hazard's class
mixes: 0.42 (shrub; tree 0.47, grass 0.32).

What it means:

- The curves land within a factor of two to three of NRI with nothing tuned, and the ranking agrees well. The main
  western states sit at 1.5–2.0× (California 2.0×, Idaho 2.0×, Oregon 1.9×, Arizona 1.5×).
- The gap is larger in the East (median cell 4.7× against 1.8× in the West). Likely contributors, not tuned:
  Hazard's rate is the burn probability of the burnable land in the cell, while buildings sit mostly in developed
  land where fire arrives less often (Hazard's all-pixel rate lowers the national ratio by about 10%); Hazard couples
  every fire to the whole cell (p_hit = 1); NRI counts reported losses for all buildings in a county.
- Pooled CAL FIRE factors (0.3 / 0.4) would bring the warehouse and office to 0.6× and 0.8× NRI; the same-fire
  factors were chosen on evidence, not to match NRI (D-WFRE-07).

## 14. Capability and fail-closed decision

Conditional scalar damage ratio per building; scenario dollars, annual and tail metrics withheld (consumer-owned);
contents withheld; unknown pathway, building, product or unit, a missing or invalid class state, and a burn
probability in the call fail closed. Promotion gate blocked.

## 15. Open seams and update triggers

- A lifeform per cell from Hazard would replace the shrub default.
- Loss data for large sprinklered warehouses or offices would replace the factors.
- A flame-intensity-stratified building loss dataset would test the USFS response.
- Hazard-side: the fire rate at building locations (burnable-pixel BP is the wildland rate); see §13.
- Contents.

## 16. Validation/QC

[Validation report](VALIDATION_REPORT_wildfire_real_estate__model_v0_1__docs_r1.md): validator, hand checks
and the Hazard loader probe.
