---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Standalone station depth-only screening reader.
---

# From inherited evidence to this delivery

1. **Question:** make the first station Flood screening maps with existing hazard methods.
2. **Evidence:** retain the pinned legacy Hazus facility table, including its built-in equipment
   assumptions. Current Hazus electric-power loss support is disabled; this is explicitly legacy evidence.
3. **Grain:** one whole assembly. Separate subsystem curves would double count its loss/value.
4. **Axis and form:** 0–10 ft above grade, piecewise-linear direct-loss ratio; no intrinsic random spread.
5. **Adjustments:** none to source knots. Coastal is an explicit Tier-4 depth-only engineering transfer,
   excluding chemistry, waves and scour; it is not independently calibrated coastal damage.
6. **Emit:** conditional assembly DR. The exact station/value and annual frequency belong to the consumer.
7. **Ship:** separate standalone cell, index SHA, known answers, 31-row value partition and annual binding.
   The old Wind cell's annual restriction is unchanged.

The consumer preserves missing probability/location mass, caps annual loss at full same-station
replacement value and calculates exact fixed-mass TVaR on its simulated distribution. Its combined
Flood display uses EAL sum and marginal-tail maximum, not a joint Flood distribution.

See the [seven-step dossier](../current/derivation.md), [metadata](../current/metadata.md),
[audit map and deviation](../current/README.md#audit-workbook-map-and-documented-deviation) and
[consumer handoff](../../../contracts/hazard_handoff/substation_flood_screening_v1/README.md).
