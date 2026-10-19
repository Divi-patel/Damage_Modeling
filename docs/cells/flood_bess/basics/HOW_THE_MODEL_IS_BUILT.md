---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Evidence-to-test reasoning
---

# How the candidate was built

**Question → evidence:** determine which water-affected property is replaced.
OEM/NEMA guidance supplies conditional consequences; original NREL inputs supply
cost categories. Neither supplies a matched utility depth–repair dataset.

**Grain → axis → form:** one enclosure's active hardware and one separate PCS.
Explicit local freshwater depth drives the owner-selected binary policy, or the
existing PCS proxy after one entry-height subtraction. No height-proportional
battery value assumption or borrowed substation assembly is used.

**Adjustments → emit → test:** same-budget allocation and no numerical IP or
certification credit. Local v0.2 adds explicit saline replacement and freshwater
saturation, preserving earlier supported values. Canonical v1.0 keeps those
responses unchanged and qualifies conditional annual consumption through exact
pins, domain/condition tests and independent annual mean/tail checks. No measured
mean, intrinsic spread or complete-property claim follows. See
[the derivation](../current/derivation.md) and [validation](../current/validation.json).
