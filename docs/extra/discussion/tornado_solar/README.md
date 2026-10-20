<!--
author: owner-directed (Divy) · agent-drafted
created: 2026-08-29
updated: 2026-08-29
status: active
scope: Reasoning node — what Damage research, pathway contract and promotion evidence are required before Tornado × Solar can replace the current aerodynamic lower-bound sensitivity. Promotion target: a future tornado_solar plan and governed Damage cell/pathway package; no current version changes.
-->

# Tornado × Solar — from aerodynamic sensitivity to governed Damage pathway

> **Status: active.** The current Strong-Wind Solar artifact, current Hazard CONUS release and local Deep
> experiment remain unchanged. The native Tornado, observed-footprint and annual-risk mechanics are usable;
> a later Damage research/curation cycle must resolve Tornado-specific Solar response before a complete
> Tornado or Combined claim is promoted.

## The question

What evidence, intensity axis, failure-unit response, exposure/value composition and capability declaration
must a governed Tornado × Solar Damage pathway carry before Hazard may replace its current aerodynamic-only
sensitivity and mint coordinated new CONUS and Deep scientific versions?

This node opens that future question. It does not create a plan, choose a version number, change a canonical
cell, publish an artifact or authorize a Hazard consumer cutover.

## Verdict first

Preserve the current versions exactly as they are. Treat the existing Tornado × Solar calculation as a
reproducible **aerodynamic lower-bound sensitivity**: it correctly models Tornado occurrence, path contact,
swept Solar area and the part of vulnerability represented by ordinary gust loading, but it does not yet
represent debris/missile or Tornado-core destruction.

When the owner later starts the research cycle, curate Tornado × Solar in this repository first. The output
must be a proposed pathway-aware Damage package—not an arbitrary multiplier on the Strong-Wind curve. Only
after its scientific and publication gates pass should Hazard consume the new immutable GCS pin and create
new versions at both supports.

```text
NOW
---
STRONG_WIND_SOLAR_V1 remains current
        |
        +-- Strong Wind × Solar              current declared scope
        `-- Tornado × Solar                  aerodynamic sensitivity only

FUTURE, AFTER OWNER STARTS THE RESEARCH
---------------------------------------
Damage discussion -> bounded research -> plan -> proposed artifact + KATs
        -> owner scientific gate -> immutable publish + registry activation
        -> Hazard CONUS integration/version -> Hazard Deep integration/version
```

## What was verified before reasoning (2026-08-29)

| Check | Result |
|---|---|
| Current Solar Damage pin | `strong_wind_solar@model_v1_0__docs_r3`, SHA `832f47d69372ec54723a61b8a956addccef07bb39338c3ec99907e116f1855ca` |
| Current Damage scope | Straight-line/hurricane/derecho-style aerodynamic gust loading; Tornado debris, EF bridge and narrow-core destruction are explicitly deferred |
| Current Tornado × Solar artifact | No canonical or active `tornado_solar` entry exists in the machine-readable artifact index |
| Wind Farm precedent | `wind_tornado_wind@model_v1_0__docs_r4` has a Boolean Tornado D50 shift, but it is turbine-specific Tier-4 expert judgment and is not transferable to Solar |
| Pathway-aware contract | Bundle v3 / emit v2 supports first-class pathway identity and prohibits hiding a pathway behind a Boolean variant in newly promoted pathway-aware packages |
| Hazard native evidence | SPC path/event records; the executed Deep case used the rated 1996–2025 window and a 150 km collection support |
| Hazard M1/M2 mechanics | Local collection rate, EF mixture, path geometry, actual-PV-footprint contact and conditional swept fraction executed and independently validated |
| Deep result | Hayhurst Solar Tornado aerodynamic sensitivity EAL `$9.66/year`; complete Tornado and Combined claims withheld |
| Side effects | The experiment wrote no governed GCS object, database row, Damage artifact or Hazard scientific version |

The executed evidence is pinned at Hazard commit
[`381662a721ae8d452c3f7623a827742670295a00`](https://github.com/aamani-ai/Hazard_Modeling/commit/381662a721ae8d452c3f7623a827742670295a00).

## Current height-basis decision

No Solar height bridge is applied in the current method.

```text
Strong Wind
ASCE 10 m, 3-second gust
        |
        `-- consumed directly by STRONG_WIND_SOLAR_V1
            (the artifact accepts a 10 m wind-height basis)

Tornado sensitivity
EF damage-estimated near-surface gust band -> midpoint gust
        |
        `-- consumed on the same declared near-surface/10 m basis
```

This is different from Wind Farm, where the M2 handoff may convert a 10 m gust to turbine hub height before
evaluating the turbine curve. Solar equipment is close to the surface, and the current Solar artifact
explicitly accepts 10 m input. Direct use is slightly conservative relative to a lower array-height gust but
is a declared Version-1 choice, not an accidental omission.

The future Tornado research must declare its own pathway-native axis and height meaning. It must not add a
height conversion merely because Wind Farm has one. If research selects EF class, reconstructed near-surface
wind, debris energy or a composite state, the artifact must carry that basis explicitly.

## Where the current Tornado chain succeeds and stops

```text
M0  SPC event/path evidence
      date + EF/F rating + coordinates + length + width
                         |
M1  local collection process
      frequency + outbreak dispersion + EF/path mixture
                         |
M2  observed Solar coupling
      corridor hit? -> actual PV polygon fraction swept
                         |
                         |                    PASSES
-------------------------+--------------------------------
                         |                    INCOMPLETE
M3  current response
      EF midpoint gust -> STRONG_WIND_SOLAR aerodynamic curve
                         |
      missing: debris/missile + Tornado-core/local destruction
                         |
M4  annual loss
      mechanically valid lower-bound sensitivity
```

M2 already answers how much observed Solar area a Tornado corridor touches. M3 must answer what happens to
the equipment inside that area. The current response applies aerodynamic uplift/torsion/detachment/foundation
fragility only. A swept fraction is not itself a debris or core-destruction curve.

## Why a simple “higher wind curve” is not the default answer

The current Wind Farm artifact lowers D50 for its Tornado variant, making direct-hit turbine damage occur at
a lower normalized speed. That is useful precedent for pathway differentiation, not a Solar parameter source.
Solar introduces distinct mechanisms and failure units:

```text
Tornado × Solar
├── aerodynamic gust loading
│   ├── tracker/racking torsion and uplift
│   ├── module attachment/detachment
│   └── pile/foundation uplift
├── debris/missile impact
│   ├── module penetration and shattering
│   ├── inverter/combiner enclosure damage
│   └── SCADA/electrical damage
└── Tornado-core / narrow-swath destruction
    ├── concentrated row collapse
    └── localized severe or near-total contacted-stock loss
```

One blanket vertical multiplier or horizontal curve shift would silently mix occurrence, contact, physical
mechanism and conditional severity. A future model may share admitted aerodynamic curve records, but shared
Solar anatomy does not authorize shared parameters for debris or core destruction.

## Options weighed

| Option | What it is | Verdict |
|---|---|---|
| A · Keep the current proxy forever | Continue EF midpoint gust → Strong-Wind Solar response and call it complete Tornado loss | Rejected as a complete claim; retained now only as an explicitly labeled aerodynamic sensitivity |
| B · Raise the Strong-Wind curve | Add one Solar Tornado multiplier or D50 shift | Not pre-approved; too coarse unless bounded research proves it is an honest screening representation of the included pathway |
| C · New standalone `tornado_solar` cell | Separate cell with its own scope, axis, evidence, curves, capability and publication identity | Live candidate; cleanest when Tornado mechanisms/versioning change independently |
| D · First-class Tornado pathway in a shared Solar wind bundle | Bundle-v3 package with separate `straight_line_convective` and `tornado_direct_hit` pathways over a shared failure-unit/value substrate | Live candidate; valid only if shared anatomy/value and pathway-specific records remain explicit |

The future plan must choose C or D from evidence and consumer needs. This discussion deliberately does not
mint `model v2`, `tornado_solar model v1`, or another identifier in advance.

## Research and curation package required

The bounded research should produce the following decision-ready evidence:

1. **Scope boundary** — direct aerodynamic, debris/missile, core-swath and explicitly excluded compound
   mechanisms; physical destruction only, not downtime/business interruption.
2. **Source register** — Solar-specific forensic/claims, engineering, laboratory, standards and public-event
   evidence, each assigned an allowed role and transfer limitation.
3. **Pathway-native axis** — decide whether the governed input is EF class, EF-conditioned gust, reconstructed
   near-surface wind, debris proxy, contacted-core state or a declared combination.
4. **Failure-unit coverage** — give every pathway × failure-unit pair a modeled, secondary, DR≈0 or withheld
   treatment; never turn an expected subsystem into observed site anatomy.
5. **Exposure contract** — distinguish corridor contact, swept fraction, debris-affected fraction and
   Tornado-core fraction; state which object Hazard M2 must emit.
6. **Value linkage and composition** — attach each response to the correct physical value, combine competing
   mechanisms without double-counting and apply equipment/aggregate caps inside the event calculation.
7. **Uncertainty and calibration grade** — distinguish evidence-backed distributions, engineering envelopes
   and Tier-4 assumptions; never call an envelope a confidence interval.
8. **Capability declaration** — specify allowed use, withheld outputs, input prerequisites, valid domains and
   whether the result is screening-only or earns a stronger grade.
9. **Known-answer and pressure tests** — zero below declared thresholds, monotonic/bounded response, pathway
   routing, value parity, cap behavior, no silent fallback and exact emitted provenance.

The likely durable deliverables are a research memo, source register, claim/parameter register, value
crosswalk, proposed artifact, capability declaration, KAT package, validation report and promotion-gate
matrix. Their exact names and model identity belong in the later plan.

## Producer/consumer boundary

```text
Hazard_modeling owns                         damage_modeling owns
---------------------                       ---------------------
SPC source admission and event identity     pathway scope
local frequency / EF and path mixture       pathway-native intensity contract
observed asset polygon and corridor contact failure-unit response
swept/contact exposure state                value-linkage requirements
annual event state and W+T composition      Damage emit + capability + provenance
EAL / PML / VaR / TVaR                      KATs and valid-domain refusal rules
```

Damage must say what M2 exposure object it needs; Hazard must produce that object without copying Damage
physics into its driver. Hazard may preserve the current aerodynamic sensitivity during development, but it
may not silently relabel it as the future full pathway.

## Version and promotion sequence

The owner decision is to defer version changes now. Immutable/current state remains:

- current `STRONG_WIND_SOLAR_V1` Damage artifact and its GCS/registry identity;
- current screening-grade Hazard CONUS Convective Wind × Solar release;
- current local Deep experiment with Tornado/Combined explicitly withheld; and
- no `tornado_solar` current product seat.

When research is ready:

```text
1  settle this discussion's cell-vs-pathway and scope decisions
2  create a Damage plan with decision/assumption registers
3  build a proposed package; do not replace the current artifact
4  validate evidence, KATs, value/exposure composition and capability
5  owner approves the Damage scientific/model promotion
6  publish immutable GCS bytes and activate the exact registry pin
7  Hazard CONUS consumes the pin and mints its own new scientific version
8  Hazard Deep consumes the same admitted pin at observed support and mints its version
9  reconcile both supports and retire only stale current representations—not history
```

Damage semantic versioning and Hazard scientific versioning are separate decisions. Promotion at one support
does not silently upgrade the other.

## Pressure tests the answer must survive

1. The full result must differ from the aerodynamic sensitivity only where named evidence/mechanisms justify
   it; research cannot be a search for a desired higher loss.
2. EF is a damage-estimated category, not a direct measured Solar wind field; proxy and rural/reporting bias
   must remain explicit.
3. Exact footprint contact cannot be counted again as a Damage probability if Hazard M2 already conditioned
   on a strike.
4. Aerodynamic, debris and core responses cannot each consume the full same equipment value independently.
5. The model cannot borrow Wind Farm D50 shifts merely because both hazards are Tornado.
6. Unknown Solar configuration or debris environment must yield a declared default/envelope/withheld status,
   not invented precision.
7. The pathway must work at both canonical CONUS support and observed Deep support without copying support
   assumptions between them.
8. Existing immutable releases remain reproducible while the proposal is researched and shadow-tested.

## Owner gates carried into the future plan

`G1` cell versus first-class pathway identity · `G2` included/excluded mechanism scope · `G3` admitted axis
and height basis · `G4` evidence/parameter tier acceptance · `G5` exposure/value/cap composition · `G6`
capability/use grade · `G7` Damage publication · `G8` separate Hazard CONUS and Deep promotions.

## Exit condition

This node becomes `settled` when bounded research supports an owner decision for G1–G6 and a plan records
the chosen package identity, evidence work, validation bars and done-when conditions. It does not settle merely
because a candidate curve or higher loss number exists.

## Related

- Current Solar cell scope:
  [`strong_wind_solar/current/README`](../../../cells/strong_wind_solar/current/README_strong_wind_solar__model_v1_0__docs_r1.md)
- Current Solar metadata and height input:
  [`strong_wind_solar_damage_code_metadata_spec`](../../../cells/strong_wind_solar/current/strong_wind_solar_damage_code_metadata_spec__model_v1_0__docs_r1.md)
- Hazard-pathway scope-splitting standard:
  [`18_hazard_pathway_scope_splitting_standard`](../../../method/standards/18_hazard_pathway_scope_splitting_standard.md)
- Pathway-aware artifact/emit standard:
  [`22_pathway_aware_artifact_and_emit_standard`](../../../contracts/standards/22_pathway_aware_artifact_and_emit_standard.md)
- Wind Farm precedent, not a Solar parameter source:
  [`wind_tornado_wind current artifact`](../../../cells/wind_tornado_wind/current/wind_tornado_wind__model_v1_0__docs_r4__curve_artifact.json)
- Hazard Deep assessment at the pinned experiment commit:
  [`ASSESSMENT.md`](https://github.com/aamani-ai/Hazard_Modeling/blob/381662a721ae8d452c3f7623a827742670295a00/Notebooks/convective_wind/combined/solar/experiments/2026-08-29_observed_asset_m0_m4/ASSESSMENT.md)

