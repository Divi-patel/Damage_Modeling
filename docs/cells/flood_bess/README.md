---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS Flood local candidate, not a released Damage cell
---

# Flood × BESS

**Local candidate v0.1 only.** BF-Q01 approves the conservative active-hardware
replacement policy for local testing. No canonical runtime, annual metric or
national publication is admitted.

```text
freshwater inundation × standalone outdoor LFP BESS
├─ active enclosure hardware: battery + management + cooling
│  └─ 80 repeated units; explicit common-entry replacement policy
├─ separate PCS: 20 repeated units; existing FS_INV proxy
└─ unresolved: enclosure/racks/fire safety, internal MV/cables/controls,
   civil property and fieldwork; retained in the full $109.8M denominator
```

Start with [the plain-language explanation](basics/README.md), then the
[candidate package](proposed/local_candidate_v0_1/README.md).
Source research and its exact locators remain in the
[BESS evidence record](../../extra/discussion/bess_damage/README.md).
The [version register](VERSION_REGISTRY.md) distinguishes local candidate status
from release. The global runtime index is deliberately unchanged.
