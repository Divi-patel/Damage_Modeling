<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-16
updated: 2026-10-16
status: settled
scope: Separate network function, physical model boundary and response resolution before selecting the first substation Damage model.
-->

# Which substation, and which response resolution?

**Outcome, October 16:** the owner chose one generic canonical-substation grid and deferred type-level
products. This comparison remains background. The current concrete reference is retained as working input;
exact response/value qualification continues under SD-D11. No further type-choice gate applies.

The owner questioned whether the prior assembly curve was a shortcut caused by treating a substation as a
Solar/Wind subsystem, and whether our new reference is distribution or switching. These are separate
questions. The current profile is a **transmission transformation station**, 345/138 kV, outdoor AIS, with
two 336 MVA autotransformers. That was the agent-selected candidate drawn from the supplied twin; the
owner's latest question does not select a replacement or accept the existing proxy.

## Three independent distinctions

| Dimension | What it answers | Consequence |
|---|---|---|
| Network function | Generation/collector step-up, transmission transformation, distribution, switching-only, or a combination? | Changes the expected equipment and service boundary |
| Model boundary | Is this station the modeled asset, or a subsystem serving a generation facility? | Changes the enclosing scope and accounting; does not itself change the same equipment's physical response |
| Response resolution | Component, subsystem or source-supported assembly? | Determined by evidence, exposure, repair consequence and intended use; not by depth in a tree |

The same physical station can be a standalone modeled asset and serve a Solar/Wind facility. Moving its
position in a hierarchy does not create different physics. Shared equipment is represented once and linked
to the assets it serves. A different station design can require different response selection and composition.

## Functional profiles — illustrative classification

| Functional profile | Main function | Distinction for this work |
|---|---|---|
| Generation/collector step-up | Raises plant/collector voltage for grid connection | GSU describes a step-up transformer/function, not every substation located at a power plant |
| Transmission transformation | Connects grid voltage levels | Our existing 345/138 kV candidate belongs here |
| Distribution | Supplies lower-voltage distribution feeders | Requires its own equipment, geometry and value reference |
| Switching-only | Connects/routes circuits without main voltage transformation | A pure switching reference excludes main step-up/down power transformers; auxiliary/instrument transformers may still exist |

OSHA distinguishes generation step-up, transmission step-down and distribution functions and notes combined
types: [illustrated substation glossary](https://www.osha.gov/etools/electric-power/illustrated-glossary/sub-station).
Actual names can be looser than functional definitions. For example, PJM's
[Gloucester study](https://www.pjm.com/pjmfiles/pub/planning/project-queues/facilities/s107_fac.pdf), §1.4,
describes a 230/138 kV transformer at a facility named a switching station. Classify from equipment/function,
not the station name alone. Outdoor/indoor and AIS/GIS are separate configuration dimensions.

## Why the existing assembly curve exists

The [historical discussion](../flood_wind_shared_electrical/README.md) first sought reusable electrical
responses across Solar/Wind. The current
[derivation dossier](../../../cells/flood_wind/current/flood_wind_curve_derivation_dossier__model_v1_0__docs_r1.md),
§§1–3, records the subsequent reasoning: component-level economic response evidence remained incomplete,
while Hazus-MH 2.1 Table 7.9 supplied a whole-substation response. The
[release decision](../../../cells/flood_wind/current/RELEASE_DECISION_flood_wind__model_v1_0__docs_r1.md)
accepted that limited screening use. The older discussion's noncanonical status is historical; the current
release controls current status.

Thus, the evidence supports a deliberate source-grain choice under limited evidence. It does **not** support
the claim that a detailed component model existed and was collapsed merely because the station was a child
of a wind farm. The `GSU` and `flood_wind` identifiers describe the existing consumer/release context; they
do not prove applicability to every GSU, transmission, distribution or switching design.

## Does a different station type change Flood damage?

It can change both absolute physical loss and the normalized damage ratio. The direction and magnitude
cannot be inferred from the functional label alone. Relevant differences include:

- presence, construction and replacement value of transformers, breakers, panels and cables;
- vulnerable elevations, enclosure/building water entry and local water exposure;
- repair-versus-replacement decisions, shared repair work and the cost denominator;
- the physical footprint and the event's spatial support.

DOE-hosted [Oncor flood practices](https://www.energy.gov/oe/articles/oncor-response-grid-rfi) identify yard
grading/elevation and separate equipment assessment, providing operational context for these distinctions;
they are not a source of numerical damage modifiers. Our current curve's ESSL/ESSM/ESSH voltage classes
share identical ordinates. This is a resolution limit of the retained source. It neither distinguishes the
functional profiles above nor establishes equal physical vulnerability across them.

For matched equipment under matched local demand and repair rules, an intrinsic component response can
be reusable across station types. Changes to composition, exposure and value still change the assembly
result. A component that is absent has no asset value in that profile; a present component without a
qualified response remains an explicit modeling gap.

## Proposed structure and immediate decision

Use typed physical profiles with explicit equipment inventories and independent response selection. Reuse
qualified component/subsystem responses across profiles. Admit assembly responses only with an explicit
scope match; an assembly and its included component losses remain mutually exclusive. This is an
architectural direction, not a new shared-runtime schema or a claim that the component curves exist.

**Historical choice, now resolved by deferral:** the comparison was transmission transformation versus
distribution versus pure switching. The owner then selected one generic first grid rather than separate
type products. Preserve the concrete station assumptions, existing budget and reuse proof; qualify the
response for that reference. [SD-D11](../../../plans/substation_damage/decisions.md) controls the next work.
