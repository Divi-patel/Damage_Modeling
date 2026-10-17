---
author: "owner-directed (Divy) · agent-researched"
created: 2026-10-16
updated: 2026-10-16
status: settled
scope: Preserved component feasibility findings; follow-up research deferred by the owner in favor of assembly-screening CONUS delivery.
---

# Can a small component model improve the first station grid?

**Later owner disposition, October 16:** component research is deferred to the
[future research plan](../../../plans/substation_damage/component_research_backlog.md), for coordination
with the intern. Continue the assembly screening grid and priority hazard sequence now. The earlier
recommendation below is historical reasoning, not an active prerequisite for national execution. The
measured audit remains useful future evidence; no response/capability was changed.

The owner supplied the side discussion about failure-sensitive anatomy, justified defaults and a finite
delivery scope, and asked whether we should do more than transfer a reference curve before an expensive
CONUS run. **Recommendation: compare a small component-aware candidate with the qualified assembly proxy
before national execution.** This is a bounded investigation, not a commitment to reproduce the whole twin
or a finding that additional detail is more accurate. The earlier facility-point screening approval remains
the implemented baseline; this review reopens the candidate comparison, not the station identity.

```yaml
change_class: EVIDENCE_ONLY_NO_OUTPUT_CHANGE
affected_candidates: [flood_solar, flood_wind, standalone_substation_binding]
outputs_can_change_for_same_inputs: false
primary_workflow: DOCS_EVIDENCE_ONLY_WORKFLOW
version_impacts:
  cell_model: unchanged
  cell_docs: unchanged_no_cell_package_edited
  package: unchanged_no_release
  schema: unchanged
runtime_admitted: false
```

No curve, selector, conditioner, runtime exposure/value mapping, capability or emit meaning changed.
Any subsequently selected component response/binding must follow its own model/release classification;
these research files are not a new cell scaffold or a replacement for the conditional handoff.

## What the existing library actually supplies

The inspected canonical artifact is
[`flood_solar@model_v1_0__docs_r4`](../../../cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json).
Its [dossier](../../../cells/flood_solar/current/flood_solar_curve_derivation_dossier_v1_0.md), §§7–8 and the
parameter-tier addendum, explicitly identifies intermediate percentages as engineering parameterization.
The whole-substation `flood_wind` curve remains a different response grain, with source-native heights.

| Candidate | Existing definition | Necessary transfer check |
|---|---|---|
| `FS_SCADA` | Cabinet/electronics damage ratio versus local depth above its critical datum | Relay electronics may be a related-component analog; batteries, station service and building shell do not automatically share it |
| `FS_XFMR` | `TRANSFORMER_MAIN` failure-unit ratio; dossier calls it transformer/control area | Resolve whether control-area exposure justifies the stated whole-transformer repair denominator; identify salvage/repair scope before transferring |
| `FS_SWG` | Switchgear/breaker cabinet ratio; dossier rationale cites low/medium-voltage gear | Our 345/138 kV outdoor AIS breakers and disconnects are not interchangeable with a distribution cabinet |
| `FS_CABLE` | Cable response with pathway/termination exposure | Possible supporting candidate; cable, conduit and trench values are different things and cannot all receive a cable DR |

The published `FS_SCADA`, `FS_XFMR` and `FS_SWG` axes use positive depth above a component datum, with
zero response at zero positive depth. They already supply tabular numeric candidates. We do not need to
invent a new curve simply because the asset label is Substation. But their Solar capability does not
automatically qualify a new station binding or transfer their permission for downstream annual metrics.

## Executed feasibility audit: complete accounting, not admitted coverage

The [31-row crosswalk](verification/component_candidate_crosswalk.csv) assigns each current budget row
to one research group. The [receipt](verification/component_candidate_audit.json) pins the exact artifact,
profile, current assembly value ledger, Pluvial method and audit helper by SHA-256.

| Research group | Candidate installed value | Interpretation |
|---|---:|---|
| Controls and auxiliaries | $3,194,667.00 | Electronics candidate plus battery/station-service items requiring separate disposition |
| Main transformers | $4,623,360.00 | Whole units; not the price of their vulnerable controls alone |
| Yard breakers and disconnects | $6,951,567.00 | Transmission transfer must be qualified; no universal switchgear allocation |
| Cables, conduits and trenches | $2,039,984.70 | Retain their distinct physical repair scopes and ingress role |
| Control-house building | $1,339,840.89 | Separate from equipment within the house |
| Remaining yard and civil | $9,203,816.78 | Explicit residual; no blanket zero or invented generic curve |
| Outside current response | $3,061,823.44 | Existing external-road and support allowances remain outside |

Totals reconcile to $30,415,059.81, including the unchanged $27,353,236.37 fenced assembly denominator.
These are **research buckets, not modeled-value coverage**. The budget remains an installed/new-build T4
proxy, not a freshly established repair-cost schedule. Allocation by cost share alone would not solve
response applicability. Never add the whole assembly loss to overlapping component losses.

### A concrete compatibility finding

The audit reads the actual `CAP_M = 0.30` in Hazard's Pluvial method and the authored reference heights:
control-house floor +0.30 m and transformer control cabinet +1.0 m. Under direct overtopping only,
`h = max(0, local_depth - critical_height)` cannot become positive for either threshold anywhere in the
current model domain. At a floor threshold of exactly 0.30 m, the maximum is exactly zero.

This is an algebraic domain check, **not a prediction of zero station damage**. A floor is not evidence
of a watertight building. Conduit entry, lower terminations, unmodeled auxiliaries and civil damage remain
separate mechanisms. Nor can lower equipment heights be selected merely to manufacture positive losses.
Keep the canonical design fixed while resolving the appropriate failure/ingress datum. More terrain
pixels alone cannot repair a response/domain mismatch.

## Source pressure test and explicit limits

1. **NERC, April 21, 2015, pp. 1–2:** the freshly retrieved primary
   [transmission-station flood lesson](https://www.nerc.com/pa/rrm/ea/Lessons%20Learned%20Document%20Library/LL20150402_Severe_Flooding_Damages_Transformer_Substations_final.pdf)
   reports damage to protection, telecommunications and station service, with below-grade equipment and
   conduit-entry corrections. It supports examining entry pathways and vulnerable equipment placement.
   Its below-grade design is not our canonical station, and it supplies no economic depth-damage ordinates.
2. **NEMA:** the library's linked 2016 PDF returned HTTP 404 on direct retrieval; an alternate official
   secure-library URL also failed to open. Search-index excerpts are not enough to resolve table alignment
   or adopt a transformer repair rule. The primary
   [May 28, 2026 announcement](https://www.makeitelectric.org/newsroom/news/nema-issues-guidance-on-evaluating-damaged-electrical-equipment-after-natural-disasters-and-extreme-weather-events/)
   confirms a newer CS 70006-2026 guide. Its linked store returned a redirect error. No 2026 equipment
   table or new numerical parameters were obtained. Retain the dossier's provenance as inherited and
   retrieve the applicable repair guidance in the bounded pass; do not describe the old percentages as
   NEMA-prescribed values.
3. **Local canonical evidence:** the Solar artifact has populated component curves, but its conduit
   conditioner is explicitly a flag with no universal numeric multiplier. The existing standalone
   [assembly handoff](../../../contracts/hazard_handoff/substation_flood_screening_v1/README.md) remains
   conditional and annual-withheld. No missing economic response is filled from the NERC narrative.

Search scope on October 16: canonical Solar artifact/dossier, existing station source review and complete
value binding; official NERC lesson; official NEMA legacy links, standards actions, updated announcement
and store link. This is a targeted feasibility search, not an assertion that no other useful evidence exists.

## Finite next comparison

**Budget:** three primary response groups (controls, transformer assemblies, yard switching equipment),
with cable/conduit ingress and residual value explicitly dispositioned; one targeted evidence/default pass;
one comparison on the existing four diagnostic windows and six rainfall anchors; one correction pass;
then a written selection. Reuse valid geographic placements and keep ineligible/unsupported controls as
such. Do not restart terrain resolution research or add national 1 m/site hydraulic work.

For each group: identify the failure unit and repair denominator, assign only necessary canonical
location/height/ingress assumptions with reference + reasoning, then accept an existing compatible curve,
propose a labeled engineering analog or mark the response unsupported. Calibration is not a prerequisite
for a labeled engineering screen; an unexplained transfer is not sufficient either. Local equipment
coordinates need a coherent selected layout, not claims of observed station geometry.

Use one shared rainfall scenario across the station's equipment; obtain local demand through the existing
Flood method and sum disjoint physical losses once. Component caps apply before station aggregation.
Do not assemble independent component percentiles or attach independent flood events to the equipment.
The local component candidate can remain a sensitivity comparator until its coverage and binding pass.

Selection must show: meaningful height/local-exposure sensitivity; no overlapping costs; explicit residual
and unsupported mass; unchanged canonical design; domain handling; source-tier/default record; measured
runtime. Different numbers or a smoother curve alone are not evidence of improvement. If no component
candidate passes, close the review with a specific failed seam and retain the assembly as the narrower
screening option; do not label it improved or expand indefinitely. A partial component result is never
silently a whole-station answer.

The [Hazard nested-grid plan](../../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/12_nested_grid_and_parent_aggregation.md)
owns the active coupling, M4, spatial mixtures and maps. Damage owns response/evidence/value-scope qualification.
The existing skill already supports this sequence; no additional skill framework is needed for this review.

## Reproduce the audit

From Damage:

```bash
.venv/bin/python scripts/reference_helpers/audit_substation_component_candidates.py \
  --output-dir docs/extra/discussion/substation_damage/verification
```

The helper only reads and accounts for current research inputs. It emits no Damage curve, hazard result,
annual loss or publication artifact. Stop and revisit the conclusions if the source profile/domain changes.
