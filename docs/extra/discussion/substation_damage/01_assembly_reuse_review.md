<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Pinned evidence, compatibility review and research-only accounting for the first standalone substation response.
-->

# Flood assembly reuse — evidence and value comparison

## What the first model could mean

The retained FEMA Hazus-MH 2.1 Table 7.9 response treats a substation as one assembly. At 4 ft of water above
station grade, its ratio is 0.07. If a same-assembly repair denominator were qualified, an event loss would
be `0.07 × that denominator`. We have not qualified that denominator. Multiplying by our full $30.415M
budget would prematurely choose both scope and cost basis.

A component model would instead represent distinct equipment responses, their local exposure and repair
costs, then combine them without overlap. Our five-system inventory supports that future research. The
assembly curve cannot be divided into transformer/control/breaker curves by their cost shares.

## Exact evidence being reused

Damage commit `02eba9be57e40ae5301fa02a45c7a49d5e86b204`; current `flood_wind`, model v1.0, docs r1,
bundle v3, capability v3, emit v2. Artifact SHA-256:
`37da745d87a4722e13118319bd30d9d2bcfd18dabc2a198ac6b8b1422bc3e1c1`.
All input hashes, including the evaluator, are in the [review receipt](verification/review_receipt.json).

- [Current dossier](../../../cells/flood_wind/current/flood_wind_curve_derivation_dossier__model_v1_0__docs_r1.md), sections 2–11.
- [Source register](../../../cells/flood_wind/current/SOURCE_REGISTER_flood_wind__model_v1_0__docs_r1.csv), FW-S011 and FW-S012.
- [Current capability](../../../cells/flood_wind/current/flood_wind__model_v1_0__docs_r1__capability.json).
- Hazard profile, budget and summary at `509bf435e1990a5d04d59c0c34621cc2d9a82fdb`; the
  [budget](https://github.com/aamani-ai/Hazard_modeling/blob/509bf435e1990a5d04d59c0c34621cc2d9a82fdb/docs/plans/_cross_cutting/substation_conus/reference_budget.csv) is the editable cost authority in Hazard, not this review's derived CSV.

The candidate is `FW_HAZUS_GSU_SUBSTATION_ASSEMBLY`, pathway `flood_inundation_contact`, curve
`FW_HAZUS_2_1_SUBSTATION_SCREENING_PWL`. The Wind cell name is its current release address; evidence about
the underlying substation assembly is the reason to investigate transfer.

| Depth above grade (ft) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Damage ratio | 0 | .02 | .04 | .06 | .07 | .08 | .09 | .10 | .12 | .14 | .15 |

These values are transcribed from the governed dossier, not claimed as a fresh primary-PDF extraction.
The same table applies to ESSL, ESSM and ESSH; no new voltage multiplier is justified. Linear interpolation
preserves the source knots. Above 10 ft is unavailable, not a flat 15% extension.

## Source-to-target qualification

| Dimension | Source/released requirement | Our target | Disposition and next action |
|---|---|---|---|
| Physical grain | One whole substation assembly, mutually exclusive with its component rows | One 345/138 kV outdoor AIS station, 2×336 MVA autotransformers | Plausible assembly transfer; no component-level calibration claim |
| Voltage selector | Exact Hazus ESSL/ESSM/ESSH | 345 kV high side; 138 kV low side | ESSM proposed using 150–350 kV high-side classification; mixed-voltage interpretation remains an explicit mapping assumption |
| Control-room exposure | Dossier reports control-room damage begins at zero grade depth | Floor at +0.3 m; internal equipment heights not fully selected | Material proxy mismatch. A floor height is not each cabinet's vulnerable elevation; cannot subtract 0.3 m from the whole curve |
| Switchgear elevation | Dossier reports source assumption +3 ft (0.9144 m) | Yard equipment geometry is not fully specified; +1 m fact belongs to transformer control cabinet | No exact match established. Do not treat cabinet height as switchgear height |
| Configuration | No fit to this exact bay layout, enclosure area or two-transformer design | Explicit breaker-and-a-half HV yard, LV ring bus and 162 m² house | Screening transfer only if its limits are accepted; no claims-calibrated or configuration-specific response |
| Axis | 0–10 ft above station grade, or same-datum WSE-minus-grade bridge | Canonical geometry exists; event-level M2 is not built | Preserve grade axis and assign datum conversion once; source's internal heights are not another subtraction |
| Water/protection | Freshwater non-contaminated; unprotected or delivered internal post-bypass depth | No floodwall; riverine/pluvial first proposed | Freshwater scenario must be declared and justified; hazard label alone does not establish clean water |
| Endpoint | Direct physical assembly repair/replacement ratio | Direct physical station loss, with separate support budget | No outage, restoration-time, BI or customer losses; denominator still unresolved |
| Annual use | Current capability explicitly withholds annual/portfolio/tail metrics | CONUS annual risk is the eventual product | Separate Damage admission and Hazard frequency/spatial/cap/annual proof required |

The elevation mismatch does not prove the curve is conservative. Different parts can differ in opposite
directions. Reproducing its numbers proves faithful evaluation of its assumptions, not validity for our
specific station. It also cannot demonstrate the benefit of raising individual cabinets or installing a wall.

## Value accounting — complete, but not an admitted denominator

The [31-row value review](verification/value_review.csv) accounts for 28 installed-budget rows and three
support allowances. It is generated from the exact Hazard budget, carries no allocation percentages, and
marks every row `runtime_admitted=false`.

| Research disposition | USD | Meaning |
|---|---:|---|
| Candidate assembly members | 22,255,600.70 | Equipment/cabling plausibly within source assembly; source denominator and transfer still unqualified |
| Scope unresolved | 5,097,635.67 | Control house/foundation, trenches, containment, site works and mixed civil/shielding allowance need specific treatment |
| External access road | 296,818.00 | Outside this electrical response; remains in the station's physical budget and needs separate treatment |
| Support unallocated | 2,765,005.44 | PM, A&G and engineering/testing/commissioning new-build allowances; not independent fragilities or automatic repair-cost factors |
| **Full candidate budget** | **30,415,059.81** | Reconciles exactly; selected damage denominator remains null |

The $22.256M subtotal is **not an approved partial denominator or coverage percentage**. Simply applying a
whole-facility ratio to a smaller equipment subtotal changes its meaning. Related foundations/installation
may belong to a source-native denominator even when unrelated civil value does not. Clarify those rows
before choosing scope. New-build pricing is a reasonable first value proxy; repair mobilization/engineering
may follow a different cost basis. Keep physical station value visible if any response coverage is withheld.

## Evidence and bounded retrieval record — 2026-10-16

| Evidence/claim | Exact locator | Access/grade | Allowed use and remaining question |
|---|---|---|---|
| FEMA legacy table and built-in elevations | FW-S011; Hazus-MH 2.1 §§7.2.2/7.2.4/7.2.6, Table 7.9 pp.7-20–7-21, footnote 2/comments | Inherited reviewed source; T3 screening response. Recorded PDF SHA `476726f194ed7e0702e8d6b47ad62616c8ca78214e56e9efc848f3bd547ae669` | Exact table reuse research; fresh PDF context/denominator interpretation still unverified |
| Electric-power output disabled in Hazus 7.0 | FW-S012; Table 9-1 and §9.4.1 footnote 21 | Inherited reviewed source and official indexed text; no new PDF-byte receipt | Preserve legacy limitation; 7.0 is the inspected version, not a claim about the newest release |
| MISO station value | Hazard [source receipt](https://github.com/aamani-ai/Hazard_modeling/blob/509bf435e1990a5d04d59c0c34621cc2d9a82fdb/docs/plans/_cross_cutting/substation_conus/valuation_source_receipt.json); MTEP24 tables cited per cost row | Primary inspected during Hazard profile work; fixed-vintage installed-cost proxy | Price the selected reference; cannot calibrate DR or establish source repair scope |
| Transmission-station flood mechanism | [NERC LL20150402](https://www.nerc.com/pa/rrm/ea/Lessons%20Learned%20Document%20Library/LL20150402_Severe_Flooding_Damages_Transformer_Substations_final.pdf), April 21 2015, pp.1–2 | Primary text inspected this turn | Below-grade monitoring/protection/control equipment was damaged; conduit entry and relocation matter. No same-unit damage-ratio observations or repair values supplied |

Fresh requests to the [official 2.1 PDF](https://www.fema.gov/sites/default/files/2020-09/fema_hazus_flood-model_technical-manual_2.1.pdf),
legacy FEMA library route and download-query variant returned HTTP 403. Bounded search covered the source
register, local retained/cached PDF candidates, official indexed FEMA text and exact-title/table web queries.
No fresh matching primary PDF was recovered. This is an access/provenance gap, not evidence that the
published table is absent or invalid. The reviewed predecessor remains useful.

No new component-local economic curve was established in this review. This is **not** a comprehensive new
search proving none exists. The current dossier's older component-level negative result remains bounded by
its own search log. NERC's operating consequences are not dollar-damage ordinates. The 2026 NEMA guide's
technical content and any newer enabled Hazus electric-power methods remain specific refresh targets.

## Reproduction and limitations

The [review script](../../../../scripts/reference_helpers/review_substation_flood_reuse.py) passed 93 cases:
all 11 source knots and 10 midpoints for all three classes, the metre/feet bridge, missing/wrong inputs,
out-of-range depths, excluded water states and every unsupported unit. It also rejects an incorrect artifact
SHA and reconciles every value row. It produces no station dollar loss, annual metrics or new curve artifact.

The reference helper still emits historical `scenario_loss_status=withheld_noncanonical_proposal` even when
fed the current canonical artifact. This is a **helper metadata drift finding**, not a reversal of the
current release. The probe checks DR only. A future production path must take admission from the exact
current artifact/capability and resolve helper-versus-consumer behavior explicitly.

The current capability's annual prohibition is binding. Its listed prerequisites concern frequency/intensity,
spatial coupling, same-unit exposure/value, partial-loss reporting, compound-event partition and caps. The
absence of curve-intrinsic spread is a separate uncertainty limit: deterministic DR can still be driven by a
stochastic annual hazard process. The [plan](../../../plans/substation_damage/README.md) keeps these tasks separate.

## Concrete next decision

The subsequent owner direction is one generic canonical-substation grid, reusing existing work first.
The [station-type comparison](04_station_type_and_response_grain.md) is now background; no type-choice gate
remains. Preserve concrete physical/value assumptions and complete the selected response's qualification.

Finish the denominator/source-context review, then present a proposed binding with its full budget,
modeled/withheld physical scope, proxy assumptions and permitted metrics. Ask about that concrete product.
Retain the physical profile and evidence-backed anatomy in the meantime. No release, shared-runtime
promotion, profile alteration or annual-capability override is implied by this research checkpoint.
