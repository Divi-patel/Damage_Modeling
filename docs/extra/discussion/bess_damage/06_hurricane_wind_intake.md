---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: active
scope: First bounded BESS Hurricane-wind curation pass; seven-step audit, qualified-reuse limits and next candidate
---

# Hurricane wind: first BESS curation pass

**The research has started using the existing Damage curation skill.** Nine
source records and eight claim records now distinguish construction evidence,
operating experience and numerical severity. Five existing Solar electrical/site
curves were reproduced at nine demands and three resistance scenarios: **135
independent DR checks**, 45 scenario-ordering checks, three invalid-axis controls
and five pressure/speed equivalence controls pass. All ten reference budget rows
reconcile. This is evidence and source-only numerical verification, **not a
qualified BESS wind curve or annual-loss result**.

Change class: `EVIDENCE_ONLY_NO_OUTPUT_CHANGE`; mode: `inside_repo`. No current
cell, runtime artifact, selector, value mapping, schema, model/docs version,
artifact index or consumer pin changes. No new-cell scaffold/runtime package is
created merely to show progress. The later numerical response follows the
new-cell workflow once a reviewable candidate exists.

## Scope and seven-step audit

The owner approved [Hurricane next](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/11_multi_hazard_roadmap.md)
after the Flood review. Keep one 100 MW / 400 MWh usable-AC outdoor liquid-cooled
LFP reference, 450 MWh installed DC, 80 enclosures / 20 PCS / 20 unit-MV groups,
shared collection/controls and a 200 × 160 m yard. Full TIV is **$109.8M in fixed
2024 dollars**. BW-C01 preserves the original boundary. This pass covers direct
tropical-cyclone wind; surge/rain flooding stay with Flood. Debris, rain ingress
and triggered escalation are explicit unresolved mechanisms, not included by
the direct-pressure curve name. Autonomous fires, BI and collector/export property
remain outside the agreed scope.

| Audit step | Current result | Open requirement |
|---|---|---|
| 1. Asset and boundary | Settled reference and physical value retained (BW-S01) | No new size or chemistry archetype |
| 2. Failure units | Enclosure/anchorage, separate PCS, unit-MV/shared electrical and civil candidates identified | Preserve bundled repair grain; do not precommit one curve per twin node |
| 3. Y-axis/value | Intended same-unit direct repair/replacement cost divided by that unit's pre-event physical replacement value | Neither survival rating nor failure probability is a cost ratio |
| 4. Value rows | All ten source rows reconciled; five retained groups sum to $109.8M | Mixed EBOS/civil and support rows remain unresolved for wind |
| 5. Physical allocation | 80 enclosures and 20 PCS have separate budgets | No assumed exposed share, full-cabinet replacement or component split admitted |
| 6. Local/site adapter | Native Hurricane source and demand/reference comparison can reuse Hazard's machinery | BESS height/exposure, anchorage/design reference and compatible gust basis require qualification; no shelter/kit efficacy assumed |
| 7. Apply or withhold | Existing source records reproduced; **BESS numerical response withheld** at this research checkpoint | Qualify target construction and economic consequence, then a proposed artifact and local proof |

## Which property needs which research?

The [reuse matrix](evidence/hurricane/reuse_matrix.csv) records every retained group.
These percentages describe ownership of the full budget, not modeled wind coverage.

| Target | Reference value / full TIV | Current research disposition |
|---|---:|---|
| Battery enclosures and included internals | $84.0M / 76.50% | Primary research target; no existing enclosure-matched Hurricane response. Separate shell/door/anchor damage from the disposition of contained hardware |
| Separate PCS | $10.4M / 9.47% | Inspect `PV_POWER_CONVERSION_AND_COLLECTION`; its Solar assembly also includes cables, grounding and collection. A matching name does not qualify this transfer |
| Unit MV, internal collection and shared controls | $13.2M / 12.02% | Existing electrical/SCADA records are candidates; the mixed budget cannot yet support separate component dollars. Whole GSU is not an isolated unit-transformer curve |
| Civil reinstatement | $1.6M / 1.46% | Separate relevant foundations/fencing from mixed site/access value; no default immunity or common wind DR |
| On-site fieldwork | $0.6M / 0.55% | Allocate support once after defining what replacement endpoints already include; no independent labor-damage curve |

Flood's 75.15% coverage does not carry into Hurricane. Charging cabinet internals
separately after charging an integrated cabinet would double-count property.
Transferring a foundation-only DR to all contained equipment would change its
economic meaning. These are binding questions for the candidate, not a demand
for cell-level electrochemistry or a full structural simulation.

## What the sources actually establish

See [sources](evidence/hurricane/sources.csv), [claims](evidence/hurricane/claims.csv)
and the [search boundary](evidence/hurricane/search_log.md) for exact locators and
permitted/prohibited inferences.

- **Existing Damage records (BW-S02):** Solar model v2.1/docs r2 site-facility
  curves use ordered lognormal damage states with explicit T4 costs and resistance
  assumptions. Their three resistance scenarios are unweighted sensitivities.
  The axis is pressure-demand/design ratio, with a conditional `(event/design
  gust)²` bridge. Reproducing the source does not upgrade its evidence tier.
- **SMA storage MV manual (BW-S03):** section 6.7 has a distinct Earthquake and
  Storm Package with twistlock/anchor instructions and a Hurricane Kit. This
  establishes configuration dependence; it gives this pass no universal wind
  failure threshold, curve or kit efficacy.
- **Utility foundation drawing (BW-S05):** a Connecticut project filing includes
  a Megapack 2XL bracket/anchor/pad detail on S-102. The rendered drawing was
  inspected. It is a project-specific load-path example, not our selected design
  or a capacity distribution.
- **SYL supplier sheet (BW-S06):** the CEC filing's PDF page 193 states 66 m/s
  wind load for an adjacent liquid-cooled utility product. The reviewed sheet
  does not identify the wind averaging/height/exposure basis or a repair endpoint.
  Do not turn that label into a three-second-gust fragility median.
- **Operating case (BW-S07):** AES reported two arrays operating during
  Irma/Maria. Regional hurricane conditions and continued service do not establish
  local equipment gust or zero repair cost. No zero-loss anchor is fitted.
- **Site and mismatched evidence (BW-S04/BW-S08/BW-S09):** Sungrow identifies
  possible wind-blown inlet obstruction; residential Powerwall mounting ratings
  are rejected for utility numerical transfer; the co-planning paper was screened
  at abstract level only. Its full contents are not declared irrelevant.

## Skill update: implemented versus shared

The [current skill](../../damage_curve_skill/SKILL.md) is being applied directly,
using the new-cell/evidence workflows, seven-step audit, provenance registers,
parameter tiers, value crosswalk and bounded-curation guide.

| Improvement | Verified state on 2026-10-19 |
|---|---|
| Interpret test protocol, intervention and measured endpoint before deriving repair response | Committed in Damage `a6634d3590ffecb3f66f3460d8397ea935941381`; the BESS Flood pressure test supplied the concrete example |
| Scope the deliverable, retain actionable future research and distinguish practical assumptions from arbitrary midpoints | Implemented in the local bounded-curation guide and routing; broader skill edits remain uncommitted |
| Illustrative twin -> scoped profile -> qualified reuse; inventory nodes need not equal curve records | Implemented in the local intake guide and associated guidance; broader edits remain uncommitted |
| Task-specific discussion stages/folders rather than a rigid three-step ritual | Separate discussion-skill update already recorded in Hazard's workflow review; not a Damage curve change |

The actual current local bundle passes **106-file validation and eight governance
self-tests**. [The receipt](evidence/hurricane/skill_check.json) records key hashes,
commands and pre-existing local modifications. That verifies bundle integrity and
governance fixtures, not independent scientific certification or a cloud-uploaded
skill release. This pass does not stage unrelated local workflow edits.

The Hurricane source review is already testing the improved method: construction
ratings, field operation and synthetic economic states stay distinct. Existing
axis/endpoint rules cover this case; no additional mandatory skill stage is
needed merely to restate them. Promote a further general rule only when a new
fail -> fix -> pass example shows a real gap.

## Next finite checkpoint and future discoveries

Develop the **enclosure and PCS candidate**, with matched wind-reference and
construction assumptions, explicit repair states and a small meaningful
sensitivity comparison if evidence requires judgment. Prefer qualified related
responses where appropriate. Do not require a national claims dataset before a
labeled engineering baseline can be considered, and do not hide unsupported
contained-hardware replacement inside a convenient proxy. Return consequential
policy choices to the owner with dollar examples; no owner choice is needed
to continue this evidence work.

| Discovery / priority | Current treatment and reason deferred | Reopen with / next acceptance check |
|---|---|---|
| Enclosure wind reference and load path / next | Unresolved target resistance; ratings found are construction-specific or incompletely defined | Matched design/test basis and wind averaging/height/exposure; document anchor/shell applicability before demand conversion |
| Enclosure damage -> contained-hardware repair / next | Not inferred from shell damage or a shutdown instruction | OEM repair guidance, damage inspection or explicit reviewed engineering repair states; demonstrate same-unit denominator and avoid double-counting |
| Electrical mixed value / next where needed | EBOS remains bundled; full GSU transfer not accepted | Qualified grouped endpoint or reconciled MV/control/collection shares |
| Wind-driven debris, rain ingress and auxiliary loss / later unless material to candidate | Separate mechanisms with no numeric contribution admitted | Delivered exposure and attributable physical repair evidence; causal/event-overlap check |
| Triggered propagation / later unless material to candidate | No invented initiation/spread probability or containment credit | Configuration-matched conditional consequence evidence and once-only property composition |

The pass closes with an evidence-rich reuse inventory and **no admitted BESS
wind curve yet**. It creates a bounded next derivation task rather than an
unlimited search. [Validation](evidence/hurricane/validation.json) and the
[input receipt](evidence/hurricane/input_receipt.json) retain the exact basis.
