---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Plain-language local candidate explanation
---

# What this BESS candidate means

We test a selected battery plant, not an observed insured site. Each container
has expensive battery, control and cooling equipment; converters stand separately.

```text
local water depth -> one enclosure's entry policy -> its active hardware value
                  -> one separate PCS's depth    -> its own hardware value
other plant property ----------------------------> unresolved, not zero
```

The owner selected a conservative local test: when water exceeds an assumed
0.30m entry, replace that enclosure's active hardware ($901,380). At exactly
0.30m the direct-entry policy remains zero. A different enclosure can be dry.
This tests a clear rule; it does not establish a measured damage threshold.

```text
active-group DR
1 |        +----------------  d > 0.30m
0 |--------o                  d <= 0.30m
  +--------+---------------> external depth
          0.30m
```

The ordinary runtime and all annual metrics remain withheld. Missing or
unsupported depth is not zero damage. For example a wet yard below the assumed
entry has zero from this mechanism; bypass or other property damage may remain.
See [how it is built](HOW_THE_MODEL_IS_BUILT.md),
[exact reference](MODEL_REFERENCE.md) and [the package](../proposed/local_candidate_v0_1/README.md).
