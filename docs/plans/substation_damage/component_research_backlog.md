---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-16
updated: 2026-10-16
status: proposed
scope: Deferred standalone Substation component-Damage research for coordination with the intern; independent of the active assembly-screening CONUS delivery.
---

# Future work: standalone Substation component Damage

**Owner priority, October 16:** deliver canonical Substation screening grids across the important hazard
families first, using qualified high-level responses. Component-level research is a future workstream
that the intern may take on. It is **not a prerequisite for the active Pluvial assembly grid**. No person
has been assigned by name, no message has been sent, and no completion date is assumed.

The active execution order lives in
[Hazard's multi-hazard roadmap](../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/04_multi_hazard_roadmap.md).
One high-level response means a response qualified for each hazard and its axis, not one Flood curve
reused indiscriminately for wind, fire or hail. Existing annual/domain/value gates still apply.

## Research brief and preserved starting work

Use the existing [Damage skill](../../extra/damage_curve_skill/SKILL.md) in `inside_repo` mode. Research
Substation as a standalone asset, beginning with Flood; classify the actual release event before changing
canonical behavior. Preserve source-native assembly evidence as a benchmark. The
[feasibility review](../../extra/discussion/substation_damage/09_bounded_component_feasibility.md) contains:

- Existing Solar component candidates (`FS_SCADA`, `FS_XFMR`, `FS_SWG`, `FS_CABLE`) and transfer limits.
- A complete, hashed 31-row value grouping; these groups are research queues, not admitted coverage.
- The shallow-depth/height compatibility finding and unresolved conduit/entry mechanisms.
- Primary-source retrieval outcomes, including evidence that does not supply numerical damage ratios.

## Checklist for the eventual research owner

1. Confirm the specific hazard, direct physical-loss boundary and canonical station reference. Reuse the
   source twin and present anatomy; split only where failure, exposure or repair behavior requires it.
2. Identify failure units: protection/control and auxiliaries, transformers, switching equipment,
   cable/entry pathways and building/civil residuals. Distinguish equipment repair from station outage.
3. Review compatible existing curves and primary evidence before proposing new curves. Resolve x-axis,
   datum, y-axis, voltage/configuration transfer, repair scope and evidence tier for every included unit.
4. Fill necessary defaults with reference + reasoning. Engineering proxies are allowed when labeled;
   unavailable response is not zero. Do not adjust a selected height merely to create a nonzero result.
5. Produce disjoint value/quantity/exposure crosswalks, response artifacts, provenance, capabilities and
   known-answer tests through the skill's seven-step audit. Do not reverse-engineer component curves by
   multiplying an assembly DR by cost percentages.
6. Hand the proposed response to Hazard for a bounded old/new comparison at the same station placements
   and hazard support. Preserve the current numerical pin until a replacement passes its gates.
7. If justified, release through explicit versions and rerun the affected M2–M4/grid products. Evaluate
   compatible adoption into Solar/Wind later; shared/owned equipment is counted once per loss boundary.

**Bound and exit:** one hazard first, one targeted evidence/default pass, the existing four diagnostic
windows/six rainfall anchors where applicable, and one correction pass before a written disposition.
Accept a useful screened component scope or record precisely why it remains unsupported. Additional
types, detailed hydraulics, every twin node and all-hazard component research are separate expansions.

## Responsibility and handoff

| Responsibility | Owner |
|---|---|
| Confirm research assignment and priority | Divy; intern assignment pending |
| Curves, failure units, evidence, value-scope mapping and capability | Damage research owner |
| Canonical profile, hazard coupling, annual distribution and grid comparison | Hazard |
| Select and publish a replacement | Governed Damage/Hazard release workflow |

The active grid team can complete assembly-screening delivery while this item remains proposed. Research
in `main` does not by itself release a new Damage model or change Hazard's installed response. Resume
this item when an owner begins it; keep results and any skill adjustments in Damage's existing homes.
