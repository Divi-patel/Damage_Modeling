---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Standalone canonical-station consumer binding to unchanged canonical flood_wind response; conditional point screening only.
---

# Substation Flood — conditional screening binding

The owner accepted facility-point screening first on October 16. This handoff qualifies an explicit
**consumer binding**, using the current `flood_wind` model v1.0 / docs r1 / bundle v3 artifact unchanged.
It creates no new curve, cell, shared numerical model or annual permission. The cell name records where
the response was curated; its failure unit is already a substation assembly, not a turbine.

## Classification and authority

The existing capability permits scenario loss with explicit same-failure-unit value and exposure. This
binding supplies those missing consumer facts for one canonical station, while narrowing the reported
meaning to a facility-point proxy. The new-cell package/workbook workflow is not invoked: there is no new
intrinsic response. Its existing [cell package](../../../cells/flood_wind/README.md), source/claim registers,
workbook, artifact and capability remain the numerical authority. No released cell file was changed.

[binding.json](binding.json) is the machine handoff. [value_crosswalk.csv](value_crosswalk.csv) is its
row-for-row review export, not an independent value authority. [validation.json](validation.json) verifies
all source pins and the byte-identical installed Hazard resources. Hazard's pinned physical profile and
budget remain the editable source owners. The profile-stage budget summary intentionally retains its
then-null admitted denominator; this handoff owns the later conditional selection.

The Hazard [checkpoint](../../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/09_conditional_screening_binding.md)
owns spatial proof, code, outputs and the annual work remaining. Its consumer installs exact local JSON
resources; it does not import this repository's reference helper at runtime.

## Seven-step qualification audit

Following the existing [seven-step template](../../../extra/damage_curve_skill/templates/TEMPLATE_SEVEN_STEP_AUDIT.md),
the numerator is the source's direct repair/replacement cost and the denominator its same-substation
replacement value. The conditional consumer estimates that denominator using the declared fenced budget.
BI, revenue, insurance terms, land value, external road and unallocated repair support are outside this loss.

| Step | Status for the declared scope | Evidence / remaining seam |
|---|---|---|
| 1. Define asset and boundary | Pass: selected canonical reference | One hypothetical 345/138 kV outdoor AIS, two 336 MVA transformers, 150 × 178 m fence. Profile/value vintage pinned; no observed ownership or insured interest asserted |
| 2. Decompose failure units | Pass for assembly proxy; component response withheld | Five inventory systems crosswalk to one existing `FW_HAZUS_GSU_SUBSTATION_ASSEMBLY` response. No overlapping child DR or inferred component curves |
| 3. Choose y-axis and basis | Conditional pass, T4 denominator transfer | Source direct physical repair/replacement ratio times $27,353,236.37 fenced installed-cost proxy. Not insured value, claims, MW-scaled wind-farm value or full project budget |
| 4. Split value rows | Pass for accounting; source membership T4 | 27 fenced rows, one external-road row and three support allowances. All 31 reconcile to $30,415,059.81. Fixed civil/related works stay within declared facility value, not separate fragilities |
| 5. Allocate physical value and zones | Pass for equivalent facility proxy; physical wet-value share unknown | Apply one assembly value once. Exposure=1 explicitly represents the equivalent source facility at one point demand, **not an assumed measured wet-yard value fraction**. Road/support $3,061,823.44 unmodeled; no support allocation inside DR |
| 6. Specify site adapter | Partial: facility-point screening only | Source grade-depth/height assumptions preserved. Centre containing pixel, full valid/buildable fence, freshwater and unprotected/post-bypass demand. No fence mitigation, pad/drainage credit, profile-height subtraction or area/value weighting. Equipment-local transfer remains unsupported |
| 7. Apply curves or withhold | Pass for source-native conditional proxy; whole-station/annual withheld | Unchanged knots, linear interpolation, 0–10 ft. Domain guards and 73,752-row parity proof. Keep null whole-station/annual/tail results and unknown support. Annual capability needs separate governed admission |

This is a deliberately narrower output than equipment-aware loss. Partial steps do not become physically
complete because the owner accepted the product scope. New component evidence or observed layouts would
require a new transfer/value review. The existing cell artifact is not altered to advertise these as new
intrinsic capabilities; the annual restriction and source limitations remain binding.

## Source transfer and limitation disposition

The source artifact SHA is `37da745d87a4722e13118319bd30d9d2bcfd18dabc2a198ac6b8b1422bc3e1c1`.
The binding SHA is `f0491594d67780eef27a1c19e6232f9bf49f1fbb5d1f5914d815b3c4679a04cb`.
Capability and evaluator pins are also in the handoff. Every exposed ordinate comes from that artifact.

The inherited 2.1 source bytes were not recovered in the bounded October 16 search; its archived source
hash is an inherited reference, not freshly verified. Current FEMA 6.1 facility-point methodology is
general precedent only: its same page lists electric substations as mapping-only. Neither reference
validates a geometric fence centre or heterogeneous-yard transfer. The full retrieval/claim record is
[discussion 08](../../../extra/discussion/substation_damage/08_assembly_depth_and_terrain_qualification.md).

The source embeds control-room damage starting at grade and switchgear elevation at 3 ft; the target's
control-house floor and transformer cabinet heights differ. Keep the source assumptions and label the
response a screening proxy. No source-curve height adjustment, exact-design claim, elevation-resilience
credit or response decomposition is supported. The five profile systems organize inventory, not five
qualified component curves. Conditional-area mean depth was rejected as the selected whole-station
transfer after the bounded terrain study; the point result cannot certify other parts of the yard dry.

## Value membership: reference plus engineering reasoning

Amounts are the Hazard MTEP24 published-table new-build proxy, used as-is. Source wording conflicts between
2023 USD and amounts escalated to 2024; do not apply a second uplift or claim 2026 market replacement value.
The cost ledger is internally detailed; applicability to the source's replacement denominator remains
**T4 engineering interpretation**, not a reconstructed FEMA bill of materials.

| Rationale ID | Selected role and reasoning |
|---|---|
| V-EQUIPMENT | Include fixed station electrical/control equipment in one facility value. Failure-unit wording is whole station; no evidence permits decomposing its DR into separate equipment responses |
| V-HOUSE | Include control house/foundation, with Hazard's declared size correction. Source explicitly includes control-room damage; it does not establish the target's exact height response |
| V-TRENCH | Include fixed cable/trench works as related station works, once. This is facility-boundary interpretation, not a supported separate trench fragility |
| V-STATION-CIVIL | Include fixed foundations, containment, fence and minor works within the station assembly; no arbitrary DR≈0 claim and no additional civil damage sum |
| V-SITE | Include fenced site-development cost as related installed works. This is the most approximate membership: retained in the declared assembly proxy, not proof all grading/earthwork suffers the same DR |
| V-ROAD | Exclude the explicitly external access road from the fenced response boundary. Its physical loss is unmodeled, not zero |
| V-SUPPORT | Track project management, administration and engineering/testing separately. No justified disaster-repair allocation is available; do not apply an assumed fragility or infer immunity |

The seven rationale IDs resolve every CSV row. Value shares are accounting quantities; they do not create
damage curves. The reported loss is source DR times the fenced denominator, rounded to cents once. The
full project budget stays visible beside the represented and unmodeled values.

## Required output and annual boundary

Supported demand returns `point_proxy_loss_usd` and source DR. Dry-centre/pondable-yard cases may return
zero **only in that field**, with a conspicuous flag; `whole_station_loss_usd` stays null. Unsupported
support/domain stays null with a reason. No missing placement is dropped or converted to zero.

The source capability's annual prohibition remains binding. The next Hazard qualification must specify
annual rainfall assumptions, complete versus unavailable placement support, and a maximum response
for each point's local ponding capacity. It must not inherit Solar's rare-tail extension and available-only
mixture blindly. A governed Damage admission/version decision follows that evidence; this handoff cannot
grant annual permission by relabeling a response.

Recheck from the Damage repository:

```bash
.venv/bin/python scripts/reference_helpers/validate_substation_screening_binding.py
```

This validates evidence and cross-repository packaging, not empirical loss accuracy. Publication, national
execution, the production standalone-reference registry, dashboard adoption and Total eligibility remain
separate milestones. The scope decision and engineering selection are recorded as SD-D18 in
[the register](../../../plans/substation_damage/decisions.md).

## Standalone annual successor

The conditional `binding.json` above remains unchanged as predecessor evidence.
The separate [annual_binding.json](annual_binding.json) pins the new
[`flood_substation` model v1.0/docs r1](../../../cells/flood_substation/current/README.md).
It retains the same station/value partition and permits downstream annual construction only
with the successor's frequency, domain, cap and missing-mass rules. Coastal is explicitly a
Tier-4 depth-only transfer. This does not retrospectively loosen `flood_wind` or supply
component curves. Hazard's executed annual tests and cloud run own downstream proof.
