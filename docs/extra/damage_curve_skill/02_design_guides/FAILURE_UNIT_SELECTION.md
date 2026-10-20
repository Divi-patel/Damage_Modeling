# Failure-unit selection guide

The failure unit is the component or subsystem slice that gets its own damage curve.

Inventory nodes and response units need not be one-to-one. A qualified source-native assembly can span
several nodes; a single node can require different responses for distinct pathways. For a new asset or
detailed twin, first use [illustrative asset intake and reuse](ILLUSTRATIVE_ASSET_INTAKE_AND_REUSE.md).
Preserve the assembly's scope and prevent overlap with any included component losses.

## Good failure unit criteria

```text
[ ] physical failure mechanism is coherent;
[ ] hazard intensity variable is meaningful for the unit;
[ ] y-axis can be defined as DR or probability/loss state;
[ ] value bucket can be mapped;
[ ] evidence can support or at least constrain the curve;
[ ] not just a subsystem added because it exists.
```

## Roles

| Role | Meaning |
|---|---|
| `primary_nonzero` | First-order direct damage unit |
| `secondary_nonzero` | Secondary direct damage, lower materiality |
| `conditioner_only` | Affects vulnerability of another unit but does not get direct v1 DR |
| `exposure_only` | Scales affected value or affected units |
| `reviewed_DR_near_zero` | Reviewed and intentionally near-zero for direct v1 effect |
| `out_of_scope_deferred` | Real mechanism but not in this cell/version |

## Anti-patterns

```text
Bad: one whole-plant solar hail curve because the hazard affects the plant.
Better: PV module glass/cell breakage curve, with tracker stow as conditioner and value basis explicit.

Bad: add inverter direct hail DR because inverter exists.
Better: mark inverter as reviewed_DR_near_zero unless evidence supports direct hail vulnerability.
```

## Required table

| Failure unit | Subsystem | Component | Role | Why modeled or not | Value bucket | Evidence strength | Update trigger |
|---|---|---|---|---|---|---|---|
