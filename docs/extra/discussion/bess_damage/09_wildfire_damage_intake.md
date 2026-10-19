---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Bounded Wildfire BESS evidence intake, costed consequence discussion and next local candidate
---

# BESS Wildfire: evidence, reuse and the first candidate

**External Wildfire is next.** Flood and Hurricane national calculations are
complete; scientific publication/product selection remain separate. This pass
audits reusable responses and defines the changed BESS work. No BESS Wildfire
curve or national result is released here.

Classification: **EVIDENCE_ONLY_NO_OUTPUT_CHANGE**, prospective `wildfire_bess`.
No existing cell/model/docs/schema pin or runtime index changes. A later proposed
candidate follows the existing new-cell workflow; its folder is not a v1.0 release.

## 1. Reuse the hazard; qualify each physical response

The current index has **12 entries**, including BESS Flood and Hurricane, with no
indexed BESS Wildfire response. Existing `wildfire_solar` v1.0/docs r3 has exact
categorical electrical responses. Their absolute ordinates are explicitly **T4
engineering judgments**, even where hazard/mechanism evidence is stronger.
[Exact input pins](evidence/wildfire/input_receipt.json) and
[validation](evidence/wildfire/validation.json) retain their source-only status.

| Target | Physical value | Disposition |
|---|---:|---|
| 80 integrated battery enclosures | $84.0M | BESS-specific grouped candidate required. A PV module or MV station is not this failure unit. |
| 20 separate PCS | $10.4M | Related solar-inverter thermal response is a candidate requiring explicit construction/exposure transfer. |
| Unit MV, controls, collection, grounding | $13.2M | Useful MV/SCADA/cable records exist; mixed values need separation or remain unbound. No whole-GSU transfer. |
| Pads, fence and access reinstatement | $1.6M | Mixed civil repair membership remains unbound, not immune. |
| Included fieldwork | $0.6M | Allocate support once against justified repairs; no independent equipment fragility. |
| **Full reference** | **$109.8M** | Fixed2024 dollars, unchanged battery-plant boundary. |

All ten source budget rows reconcile, including $23.4M excluded original costs.
See [reuse matrix](evidence/wildfire/reuse_matrix.csv) and
[value crosswalk](evidence/wildfire/value_crosswalk.csv). Cooling/BMS/safety already
inside $84M cannot be added again as plant controls. We do not invent component
costs just to apply available curves.

## 2. What the primary evidence establishes

[11 sources](evidence/wildfire/sources.csv), [11 claims](evidence/wildfire/claims.csv)
and the [bounded search](evidence/wildfire/search_log.md) record exact locators,
reasoning, permitted transfers and rejected inferences.

- **USFS**, printed 25/PDF 31, establishes annual burn probability and six source
  flame-length classes. These do not supply equipment heat flux, duration or a
  replacement threshold. FIL6 remains open-ended. BWF-C02.
- **Tesla ERG rev2.8**, section 3.3, supports external-flame initiation of cell
  thermal reactions. Ambient/storage ratings are not wildfire failure thresholds;
  response/handling instructions are not mean repair bills. Product/chemistry
  transfer to our selected LFP design remains a limitation. BWF-C04.
- **Sungrow safety whitepaper**, printed 24/PDF 25, reports an intentionally burned
  unit and surviving neighbors under its layout. It includes a report cover,
  not the full underlying report reviewed by us. This contradicts automatic
  destruction of every nearby battery; it supplies no landscape-Wildfire curve
  or monetary loss point. Availability is not damage ratio. BWF-C05.
- **UL's April 23,2026 explanation** describes tests beginning inside an enclosure.
  It does not certify external-wildfire immunity or a repair-cost curve. BWF-C05.
- **CFA's2021 account** reports spread to a second battery. It contradicts
  universal perfect containment. This is not admitted as wildfire initiation,
  an LFP-matched trial or a probability estimate. BWF-C06.
- **DOE FEMP** identifies fuels/access/protection as site considerations, without
  an efficacy coefficient. **NEMA's2026 announcement** identifies the current
  fire/heat guide; its blocked body was not read or numerically adopted. BWF-C08/C10.

No matched FSim-class → enclosure repair-cost response was admitted in this
bounded pass. That is not a universal absence claim. A transparent engineering
candidate is a possible next deliverable; unlimited research and a new fire
simulator are not prerequisites.

## 3. BWF-Q01 — settled for local testing, 2026-10-19

**In plain words:** for an enclosure whose battery contents have been thermally
compromised, should the first local Wildfire test replace the integrated unit?
This chooses the cost of a defined damage state. It does **not** assume every
landscape burn causes that state.

| Distinct outcome / engineering hypothesis | Per enclosure | Percent of full plant TIV |
|---|---:|---:|
| Cooling/enclosure/rack/safety repair, only if cells **and BMS** remain serviceable | $204,352 | 0.1861% |
| Replace all non-cell groups, only if cells remain serviceable | $334,395 | 0.3045% |
| Replace integrated enclosure once battery contents are compromised | $1,050,000 | 0.9563% |

These are related-benchmark cost allocations, not OEM quotes, proven service
methods or probabilities. The [audit](evidence/wildfire/audit_reuse.py) computes
the [saved cases](evidence/wildfire/consequence_cost_probes.csv). Lower repair
cost does not establish serviceability. Fieldwork outside bound hardware stays
separately unallocated.

**Options:** A — use full replacement for the compromised-battery state in the
local candidate, keeping serviceable-cell repairs as unweighted sensitivities;
B — withhold this battery consequence until matched OEM disposition is obtained,
while continuing independent electrical work.

**Recommendation: A.** One integrated economic failure unit avoids inventing
serviceable modules inside a compromised battery. It can overstate cost where
selective repair is viable. Cost policy remains separate from the probability
or class assignment of that state. BW-Q01 previously covered **wind structural
compromise**, and is not silently extended to Wildfire.

**If chosen:** Damage gets a proposed T4 consequence policy and repair comparisons.
The categorical response, source/footprint coupling and annual loss distribution
still need qualification. No existing curve, database, dashboard or national
result changes from this choice.

**Owner ruling, 2026-10-19:** “Test full replacement; retain repair sensitivities (Recommended)”. Full replacement for the compromised-battery state is selected for local tests; repair sensitivities remain conditional on retained-hardware serviceability. The class response, annual capability and canonical release are not approved by this ruling.

[Proposed v0.1 and verification](10_wildfire_local_candidate.md) now implement that bounded consequence policy with explicitly T4 ordinal hypotheses.

## 4. Seven-step audit

| Step | Completed now | Remaining seam / acceptance check |
|---|---|---|
| 1. Define asset | Selected outdoor LFP plant, $109.8M, battery-plant boundary | No collector/export, BI, degradation or autonomous-fire constant; externally triggered consequences remain attributable. |
| 2. Failure units | Enclosure, separate PCS, MV/controls/collection; residual civil/support | Preserve source grain; split only when physics and value support it. |
| 3. Y-axis | Same-unit physical repair/replacement cost / same-unit replacement value | No ignition, availability or service-interruption shortcut to economic DR. |
| 4. Split rows | Ten rows reconcile; $109.8M in/$23.4M out | Mixed EBOS/support qualification before complete-property claims. |
| 5. Allocate value | $1.05M per enclosure, $520k per PCS; no repeated internals | Cost groups do not prove independent replaceability or an exposed fraction of one. |
| 6. Site adapter | Native source/layout preserved; changed-support diagnostic complete | Unit centroid is a screening support choice, not thermal dose; joint-event coupling remains open. |
| 7. Curves/loss | 35 donor-state comparisons, 29 published KATs and six rejection controls pass | No BESS response yet. Cost policy plus explicit, pressure-tested vulnerability hypothesis precede runtime. |

Proposed Y-axis: `DR_u(s) = E[same-unit direct repair/replacement cost /
same-unit replacement value | native class s and declared reference proxy]`.
An ordinal response must expose unresolved local attack/thermal heterogeneity;
it is not a measured delivered-heat function. A donor economic DR must never be
relabeled as an observed failure probability.

## 5. Equipment locations can change the source input

[Hazard's source diagnostic](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/verification/wildfire_source_support.json)
checks four pinned raster tiles and 12 deliberately selected subpixel placements:
121 equipment centroids plus the reference point give **1,464 samples**. In
**nine of 12 controls**, some equipment receives a different raw source vector
from the facility point; a control spans four vectors. These are stress probes,
not a national percentage, siting-approved locations or financial results.
They justify checking unit exposure before inheriting the station's single point.

Starting reporting remains **0.05° detail and 0.25° parents**. Reuse FSim and original
BESS siting populations; qualify changed coupling. Do not rerun fire physics,
invent fine-scale hazard variation, average tail metrics or interpret marginal
BP as an observed joint fire footprint.

## 6. Site controls: no double count

| Inputs | Current treatment | Prohibited shortcut |
|---|---|---|
| Landscape fuels/BP/classes and selected yard | Native source; missing yard transfer explicit | Assume gravel makes equipment safe, then also discount DR for clearing. |
| Fence/barriers/separation/enclosure | No numerical protection credit without matched evidence | Barrier discount plus protected response for the same effect. |
| BMS/cooling/suppression/response | Included enclosure membership; effectiveness unqualified | Repeated cost or detection accuracy interpreted as loss reduction. |
| Cable routing and value | Require exposed/buried split | Entire collection budget treated as exposed cable, then burial discounted again. |
| Direct damage and fieldwork | Hardware first; support allocated once | Support receives independent DR plus repeated labor. |
| Primary damage and internal escalation | Separate attributable consequence disposition | Add spread on top of the same enclosure already replaced. |

Autonomous fires stay outside the natural-hazard product. External-fire-triggered
cell involvement is not excluded. Escalation remains unquantified until qualified,
not silently zero or certain whole-plant propagation.

## 7. Finite next checkpoint

After the now-settled BWF-Q01, prepare a proposed grouped enclosure/PCS response with explicit
ordinal engineering assumptions, costed repair comparisons, parameter tiers and
partial-property capability. If a state-cost representation is used, any new
probability interpretation is a new T4 hypothesis, not source-observed ignition.

Qualified physics/response goes in `perils/wildfire` through its public API;
generic mechanisms in `shared`; deployment sampling/orchestration in `drivers`.
Prove no event, exact classes, invalid/frequency inputs, unavailable sources,
unit support, unique-unit caps, original weights and annual tails before cloud
canary/national work. Notebooks only read and explain production outputs.

Matched external-fire tests, full reports, repair bills, yard/fuel transfer,
propagation and mixed values are actionable [BR-24–BR-26](../../../../../Hazard_modeling/docs/discussion/_cross_cutting/bess_conus/03_future_research.md).
They improve later versions; missing proofs for calibrated/complete-property
claims cannot be waived by deferring them.

Existing curation rules already cover these endpoint, exposure, value, bounded
research and future-work checks. **No new mandatory skill stage or schema change
is needed.** Broader unrelated uncommitted skill edits remain untouched.
