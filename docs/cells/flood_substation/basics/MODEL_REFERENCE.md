---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Standalone station depth-only screening reader.
---

# Exact model reference

Pin `flood_substation@model_v1_0__docs_r1`, bundle/capability v3, SHA
`f001eb0191439a1345a7a794995c684ef731f777c4b3e1eff0298de592999f30`.
Human and runtime docs are r1. This standalone release does not change the predecessor Wind runtime.

| Depth ft | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DR | 0 | .02 | .04 | .06 | .07 | .08 | .09 | .10 | .12 | .14 | .15 |

```text
DR .15 |                              *
   .10 |                     *
   .05 |       *
   .00 |*________________________________ depth above grade
         0       3           7        10 ft
```

For adjacent knots `(x0,d0),(x1,d1)`, DR = d0 + (depth−x0)/(x1−x0) × (d1−d0).
For example 1.5 ft gives .03. Negative/infinite ordinary inputs reject; missing and >10 ft
remain unavailable. The source-unit ID is `FW_HAZUS_GSU_SUBSTATION_ASSEMBLY` for provenance.
There is one atom and no component-specific curves. The value crosswalk is a denominator audit,
not a component damage allocation.

Known-answer/source checks pass; annual and national qualification is consumer-owned. Component
height benefits, complete physical-risk totals and portfolio use are not admitted.

Inspect [runtime JSON](../current/flood_substation__model_v1_0__docs_r1__curve_artifact.json),
[capability](../current/flood_substation__model_v1_0__docs_r1__capability.json),
[tests](../current/known_answers.json), [validation](../current/validation.json),
[value crosswalk](../current/value_crosswalk.csv), [source register](../current/sources.csv),
[derivation](../current/derivation.md) and [changelog](../CHANGELOG.json).
