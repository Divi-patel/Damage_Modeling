---
author: "owner-directed (Divy) · agent-implemented"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Standalone Substation Flood assembly screening, using existing hazard methods.
---

# Inputs, outputs and consumer qualification

The consumer pins `flood_substation`, `model v1.0`, `docs r1`, bundle-v3 and exact JSON SHA. Supply `sub_peril` and direct `flood_depth_above_substation_grade_ft`. Negative/nonfinite ordinary inputs reject; explicitly missing source values remain unavailable. Supported0…10ft demands return the source PWL DR. Above10ft returns null, never a clamped DR.

Use the fixed, separately pinned same-station value. Physical reference, datum and value are not selected by a power-capacity alias. The source-unit identifier retains its historical `FW_` prefix for traceability, not a Wind-only physical restriction.

A downstream annual object may use deterministic DR. It must preserve location selection, native event/year clock, incomplete response/support probability, once-only value caps and fixed-mass TVaR. Missing values can contribute zero only in the explicitly tagged partial screening product; raw state stays inspectable. No fake kWp normalization is valid for a station. Annual or compound metrics are not emitted by Damage itself.

