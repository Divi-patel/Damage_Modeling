---
author: "owner-directed (Divy) · agent-researched"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Executed non-reportable Flood binding candidate, complete station-value disposition and native-input preflight; no canonical or annual admission.
---

# First executable Flood binding review

We now have an executable candidate connecting the existing whole-substation response to our exact
station budget. It loads the unchanged, SHA-pinned response and evaluator; it does not copy the curve into
a new cell. Its dollar outputs are explicitly **audit arithmetic**, while reportable scenario loss,
whole-station loss and annual metrics remain null. This is a concrete review checkpoint before admission.

The owner asked us to retain future reuse into Solar/Wind and begin the next work. SD-D13 and Hazard's
DD-SUB8 preserve that direction. This first implementation demonstrates separation of a source response
from a local station/value binding without prematurely creating a general shared runtime.

## Proposed value policy

Use the **complete fenced station assembly** as the candidate denominator: electrical equipment,
control house, related foundations, cable/conduit/trenches, containment and fixed station site works.
Keep the separately priced external access road and project-support allowances outside that calculation.

| Scope | USD | Treatment in this review |
|---|---:|---|
| 27 fenced-station rows | 27,353,236.37 | Proposed same-assembly denominator; membership is an explicit Tier-4 engineering interpretation |
| External access road | 296,818.00 | Outside the assembly; no road response or zero-loss assumption |
| PM, A&G, engineering/testing/commissioning | 2,765,005.44 | Separate support treatment remains unresolved; not automatically multiplied by assembly DR |
| **Full candidate budget** | **30,415,059.81** | All 31 rows reconcile exactly; no whole-station loss emitted |

This replaces neither the Hazard budget nor the earlier review receipt. It develops one concrete proposal
from the earlier unresolved row categories. Hazard's authoritative summary still correctly has a null
**admitted** Damage denominator. The candidate is separately identified in
[flood_binding_candidate.json](../../../plans/substation_damage/flood_binding_candidate.json).

Including fixed station works in a facility replacement denominator does not claim that each has the same
vulnerability, or create a damage curve for each row. The source is a facility ratio. Applying that ratio
only to the earlier $22.256M equipment subtotal would also change its denominator without evidence.
The chosen station scope is a more coherent proposal, but FEMA does not supply our MISO-priced bill of
materials or prove this value composition matches its source population.

### Row rationale and provenance

| Rationale ID | Rows | Evidence and proposed interpretation |
|---|---|---|
| V-EQUIPMENT | Equipment, relays, auxiliaries, cabling and conduit | Parent FW-S011 assembly context plus selected MISO equipment definitions. Related installation/supports stay in the equipment costs once |
| V-HOUSE | Control house and foundation | Source table includes control-room damage; MISO Table 2.3-9 describes the house/installed foundation. Preserve our declared area-scaling proxy |
| V-TRENCH | Both yard trenches | Fixed pathway for the source's station cabling; inclusion is engineering interpretation, not a separately calibrated trench response |
| V-STATION-CIVIL | Containment and minor drainage/shielding | Fixed works within the selected station boundary; declared allowances. Assembly membership is proposed, not newly sourced dollar calibration |
| V-SITE | Site preparation/grounding/security | MISO p.22 includes these in substation site work. Include the existing fenced-area amount in the facility denominator; do not add separate flood damage to it |
| V-ROAD | External access | MISO p.22 treats the access connection separately; our profile explicitly places it outside the fence |
| V-SUPPORT | Three support allowances | New-build project support is not automatically repair support; withhold its loss treatment pending a defined policy |

Inputs: [parent dossier](../../../cells/flood_wind/current/flood_wind_curve_derivation_dossier__model_v1_0__docs_r1.md),
[Hazard cost source receipt](../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/valuation_source_receipt.json),
and [exact output crosswalk](verification/flood_binding_value_crosswalk.csv). The MISO text was rechecked at
pp.22 and 26–27 against the previously verified local PDF hash. The source quantities/rates were not changed.

## What was executed

The [review helper](../../../../scripts/reference_helpers/review_substation_flood_binding.py) verifies seven
input hashes, exact model/docs/schema/curve identity, unchanged annual withholding, one station, no
overlapping component responses, budget arithmetic and complete row membership before evaluating.

For an explicitly hypothetical, freshwater, unprotected **4-ft delivered station-grade depth**, the
existing source response returns **7%**. Applied to the proposed denominator, the review arithmetic is
**$1,914,726.55**. This is neither a national risk metric nor an admitted estimate for an observed station.
The output's `scenario_loss_usd` and `whole_station_loss_usd` remain null. Depth above 10 ft, unsupported
water, missing depth or incompatible datums cannot become a favorable numeric result.

The source's embedded equipment elevations remain unchanged. Our +0.3 m house floor and +1 m transformer
control-cabinet height are not subtracted from the whole assembly input. No elevation intervention benefit
is claimed. These differences remain material transfer limitations even if the arithmetic passes.

The source helper still emits historical `withheld_noncanonical_proposal` scenario metadata. The wrapper
preserves that field visibly and never uses it to authorize dollars. Correcting/promoting a production
consumer is a later explicit change, rather than a silent fix to the pinned evaluator.

## Verification

[Sixteen test methods](verification/flood_binding_validation.json), with additional subcases, passed:
source-knot/interpolation parity, same-datum metre/foot conversion, exact budget reconciliation, input-pin
drift, duplicate/missing value rows, above-range and invalid depth, unknown/saline water, missing support,
double depth payload, hidden height/value overrides, assembly/child overlap and annual-metric rejection.

From Damage:

```bash
.venv/bin/python scripts/reference_helpers/review_substation_flood_binding.py
.venv/bin/python scripts/reference_helpers/validate_substation_flood_binding.py
```

Use `--output-dir /tmp/substation-binding-review` on the first command for an independent reproduction.
The [review output](verification/flood_binding_review.json) retains eight illustrative cases and exact input
pins. No numerical cell version, source ordinate, canonical index or existing Hazard result changed.

## Native Hazard preflight and next engineering step

The [read-only preflight](verification/flood_native_input_preflight.json) verified three local Riverine
inputs against the selected September 30 reference-run manifest. They span 13,085 cells and 10/100/500-year
anchors. Their placement table carries **100 MW Solar**, with 256 placements per row. Reusing it under a
Substation name would reuse the wrong asset exposure. Underlying hazard fields/support are reusable;
station exposure must be rebuilt.

The asset-free parent summary has maximum depth above 10 ft in 21,213 of 39,255 cell/return-period rows,
touching 10,793 cells. These are **parent-cell maxima, not station depths or station unavailability counts**.
They demonstrate why the curve's finite domain needs an actual station-support audit. They do not justify
discarding rare/deep events, clipping them to 10 ft, or declaring an annual distribution complete.

For the first native engineering diagnostic, recommend **Pluvial before Riverine within the agreed Flood
workstream**: existing Pluvial M0/M1 transforms retain terrain/rainfall independently of the asset, while
their source method has a 0.30 m shallow-ponding cap. The installed placement/financial calculation is still
Solar-specific and needs a station binding. Retain that method's cap only within its stated pluvial model;
never impose it on Riverine to force curve compatibility. This recommendation changes neither hazard
science nor the agreed five-family roadmap.

The next executable checkpoint is a small native-support station M2 diagnostic, with a justified
point/footprint-to-assembly depth rule and explicit dry/missing/out-of-range states. Complete the screening
transfer/value disposition alongside it. A later admitted annual calculation must satisfy the current
capability gates; this prototype cannot override them.

## Source access and change classification

The official [FEMA 2.1 PDF](https://www.fema.gov/sites/default/files/2020-09/fema_hazus_flood-model_technical-manual_2.1.pdf)
again returned HTTP 403 on October 16. Official indexed chapter 3 text describes facility replacement
valuation, but fresh complete source bytes were not recovered. Retain FW-S011's governed source lineage
and recorded source hash as inherited evidence, not a claim of fresh primary-PDF verification. The bounded
search included the exact modern/legacy filenames, Table 7.9, §7.2.6 and switchgear-elevation terms; mirrors
and secondary reproductions were not promoted to primary-byte verification. No curve parameters changed.

Classification: research evidence and a non-runtime candidate-binding helper. Existing cell model/docs
versions, schemas, registry and package release are unchanged; no new canonical cell or shared-loader
contract was created. Target/value approval, repair-support treatment, native M2, annual admission and
production publication remain outstanding. Passing this review does not mark those gates done.
