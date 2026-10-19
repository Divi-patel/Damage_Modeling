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

**Adjustments → emit → test:** same-budget value allocation, no numerical IP,
salinity or duration benefit. Test-only costs, exact candidate hashes, invalid
input/domain cases and unchanged Pluvial controls. No shipped runtime or annual
loss claim. Full method and provenance are in
[the derivation](../proposed/local_candidate_v0_1/derivation.md).
