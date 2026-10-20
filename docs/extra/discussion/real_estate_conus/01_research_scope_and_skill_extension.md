---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-15
updated: 2026-10-15
status: active
scope: Decide how the existing Damage governance skill should use detailed asset anatomy for realistic building research; preserves evidence grain and proposes additions before implementation.
---

# From building anatomy to supported Damage research

## October 15 implementation follow-up

The owner accepted the reusable-inventory approach and authorized targeted improvements. The selected
research candidates are warehouse, three-story office and detached house; the initial boundary is building
physical loss. The earlier proposal below is retained as reasoning history. Its intake/reuse/unit changes
are now implemented in local skill revision 0.7; see the
[flow review](02_flow_and_reuse_review.md) and the shared
[plan and registers](../../../../Hazard_modeling/docs/plans/_cross_cutting/real_estate_conus/README.md).
No runtime building capability is asserted by this process change.

## The question

What should be added to the existing research method so the Digital Twin's detailed buildings improve
curve research without requiring unsupported part-level models?

## Owner intent and verified inputs

The owner wants Hazard and Damage workstreams to produce a CONUS building grid after scope, discussion
and planning. The twin is explicitly idealized. It supplies building configurations, systems, components,
failure-mode notes and source leads; it does not set the required depth or numerical truth of v1.

The proposed three-track scope and alternatives are in
[Hazard node 01](../../../../Hazard_modeling/docs/discussion/_cross_cutting/real_estate_conus/01_categories_archetypes_and_scope.md).
The [source audit](../../../../Hazard_modeling/docs/discussion/research/_cross_cutting/real_estate_reference_inputs.md)
records exact local source hashes, inspection limits and preliminary references.

The existing [governance skill](../../damage_curve_skill/SKILL.md) already contains:

- [Failure-unit selection](../../damage_curve_skill/02_design_guides/FAILURE_UNIT_SELECTION.md): coherent
  mechanism, meaningful axis, explicit denominator/value bucket and supportable evidence.
- [Engineering mapping](../../damage_curve_skill/02_design_guides/ENGINEERING_SUBSTRATE_MAPPING.md) and
  [value reconciliation](../../damage_curve_skill/02_design_guides/VALUE_CROSSWALK_GUIDE.md).
- [Evidence pressure tests](../../damage_curve_skill/02_design_guides/EVIDENCE_PRESSURE_TEST_AND_FAIL_CLOSED_CHECKLIST.md),
  pathway boundaries, source/claim registers and withhold-not-caveat behavior.
- The [new-cell workflow](../../damage_curve_skill/01_workflows/ADD_NEW_CELL_WORKFLOW.md), including a
  legitimate no-runtime-curve result and distinct model/docs/schema/skill versions.

The needed addition is a disciplined intake and simplification bridge, not replacement of these controls.

## Options weighed

| Approach | Consequence | Assessment |
|---|---|---|
| Research a curve for every twin leaf | Large search surface; implies detail the sources may not support | Not recommended as a default |
| Ignore anatomy and obtain one generic building curve | Fast initial shape; loses mechanisms, configuration and denominator constraints | Not a sufficient research method |
| Map anatomy to hazard-specific units or qualified assemblies, then research the material uncertainties | Retains physical meaning while allowing evidence-supported resolution | Adopted process direction; intake now in local skill revision 0.7 |

## Proposed reusable intake

Start with the declared building boundary and candidate configuration. Capture the six anatomy groups
(foundation/floor, structure, roof, walls/openings, fixed services, interiors) as an inventory vocabulary.
Record contents, process equipment and site works separately according to the selected scope.

For each hazard, make this mapping before fitting or transferring a curve:

| Reference node | Mechanism/pathway | Candidate response unit | Target/value scope | Research treatment |
|---|---|---|---|---|
| Roof cover, deck and attachments | Hail or wind, separately defined | Cover or assembly, subject to evidence | Repair/replacement of the affected roof scope | Split only where mechanism, endpoint and value evidence support it |
| Floor, drywall, finishes and fixed equipment | Inundation | Qualified building assembly or separate supported units | Source-specific structural/fixed-system value | Preserve source grain; do not add unit losses already included in the assembly |
| Structural frame and envelope | Wind loading/contact mechanisms | Source-matched building class or supported units | Declared building or component denominator | Qualify construction, openings, height, gust basis and mechanism |
| Barriers, elevation or protective conditions | Changes exposure or vulnerability | Input/conditioner where causally supported | Does not automatically create independent damaged value | Assign ownership of the transformation and prevent duplicate credit |

These are research candidates, not admitted responses. A source-native whole-building/assembly response
may be useful only after its physical and economic scope, transfer limits and contract fit are qualified.
The presence of a whole-building table alone does not pass that test. Existing whole-substation work is
a process precedent for preserving source grain, not a source of building parameters.

## Classification refinement from the owner follow-up

Keep Industrial/Commercial/Residential as use categories, with explicit physical archetypes underneath.
The response-selection contract should consume only the attributes relevant to its hazard and mechanism.
Construction, stories/height, roof, openings, foundation/elevation, condition and occupancy are distinct
dimensions; one story alone does not define one vulnerability class.

A profile identifies the assumed building. A Damage record identifies a governed response at its declared
pathway/failure-unit or qualified assembly grain, with applicability and version pins. Several profiles may
use one qualified response, and one profile may require several responses. This does not preselect whether
future runtime packages are split by segment or use selectors within a shared building cell.

Avoid manufacturing a new curve solely because occupancy changes. Equally, do not reuse a curve solely
because two buildings share occupancy. For a proposed roof-response transfer between warehouse and retail,
test the assembly, condition, demand, repair endpoint and denominator. Reusing roof response does not imply
identical whole-building loss. The [classification source review](../../../../Hazard_modeling/docs/discussion/research/_cross_cutting/real_estate_reference_inputs.md#classification-follow-up)
and [shared scope refinement](../../../../Hazard_modeling/docs/discussion/_cross_cutting/real_estate_conus/01_categories_archetypes_and_scope.md#refinement-physical-archetypes-select-responses-categories-organize-them)
carry the evidence and recommendation. No category/profile/curve mapping is admitted here.

## Proposed skill changes

1. **Reference intake and evidence labels.** Distinguish observed facts, class templates, declared
   assumptions and illustration-only values. Record source version/hash and node identifiers without
   treating the twin's tree or numeric defaults as authority.
2. **Archetype qualification.** Separate occupancy/use, construction, geometry, age/code assumptions,
   floor/roof attributes, fixed systems and value scope. Require explicit permitted configurations and
   unknown-input behavior. An Industrial tag alone cannot select a damage response.
3. **Anatomy-to-response crosswalk.** Allow many displayed parts to map to one evidence-supported response
   unit, and different hazards to use different units. Explain every split, merge and deferred branch.
4. **Depth and materiality decision.** Deepen when distinct response, exposure, replacement consequence or
   a useful intervention depends on it. If fine evidence is absent, retain a qualified broader response
   or an explicit gap; do not allocate its curve to parts by arbitrary value shares.
5. **Building value and scaling bases.** Generalize the energy-oriented $/MW prompts to appropriate floor
   area, roof/wall area, component quantities and replacement budgets. Preserve price year and source
   scope. Replacement value differs from property market value and insurance limits; income loss has a
   separate endpoint. Scaling to other buildings needs an applicability argument.
6. **Joint M2/M3 worksheet.** State the demanded intensity, units, datum/height/duration, exposure meaning,
   response denominator, uncertainty, caps and missing-input behavior before detailed fitting.
7. **Worked examples and regression cases.** Use warehouse/office/house cases to exercise the method;
   preserve Solar/Wind behavior and the current evidence standards.

Keep the generic workflow concise and place building-specific references/examples alongside it. A skill
change is a separate skill-revision event; it does not itself migrate runtime contracts or publish models.
The edited files and verification cases are recorded in the flow review and current skill validation report.

## Early research deliverables to specify in the plan

- One candidate profile/evidence sheet per selected track, with missing attributes explicit.
- A peril × archetype feasibility matrix, with mechanisms, likely response grain, axis/coupling needs,
  value scope, evidence maturity and next research action. Initial review is not a release promise.
- Source and claim registers with exact locators and transfer limitations; bounded search logs where a
  negative-evidence conclusion is load-bearing.
- Anatomy/response/value crosswalks and explicit modeled, conditional and withheld coverage.
- A proposed skill amendment demonstrated on contrasting building cases before broad use.

Detailed curation should follow the established new-cell procedure after the scope and plan exist. No
building cell is named or versioned here because segment/profile identity and pathway architecture remain
open. Reusable source evidence may span tracks without implying shared numerical behavior.

## Integration boundary

Damage owns conditional physical vulnerability and its artifact/capability/provenance contract. Hazard
owns occurrence, source support, building coupling/exposure, annual loss composition and risk metrics.
Both must agree on the bridge early. The profile and value receipt consumed by Hazard must match the scope
Damage actually supports; partial response coverage cannot be silently normalized to full-building loss.

See the shared [integration discussion](../../../../Hazard_modeling/docs/discussion/_cross_cutting/real_estate_conus/02_hazard_damage_integration.md).
A scientific completion claim requires the integrated proof, not two independently finished documents.
Resiliency continues to own intervention scenarios; illustrative twin reduction factors are not baseline
Damage research results.

## Pressure tests for the amendment

1. Changing a use label alone does not silently select new physical behavior.
2. Adding decorative/detail nodes to the twin does not automatically create new runtime curves.
3. Whole-building and component outputs cannot charge the same value twice.
4. Physical damage scope survives changes to insurance exclusions or loss-of-use limits.
5. Unsupported archetypes and pathways remain explicit; a neighboring curve is not silently borrowed.
6. Hail, convective wind and hurricane evidence keep their own axis and mechanism qualification.
7. Solar/Wind examples still satisfy their existing provenance, unit and value controls.

## Classification, verdict and remaining application

The original discussion was `DOCS_ONLY`. The subsequent owner-directed implementation contains a separate
process-only `SKILL_REVISION` 0.6 → 0.7. No curve form, parameter, runtime selector, conditioner, exposure,
value mapping, artifact or output meaning changes; existing cell documentation revisions remain pinned.

The intake/reuse/materiality direction is accepted and implemented locally. The node remains active for
the first building research application and any evidence-driven adjustments. Follow the
[current flow review](02_flow_and_reuse_review.md) and shared plan rather than treating the earlier
proposal as still awaiting permission.
