---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Derivation and seven-step audit of the local candidate
---

# Evidence → policy → same-unit cost

The source and claim records live in
[the research register](../../../../extra/discussion/bess_damage/evidence/README.md).
BF-S02/09/15 support conditional replacement and modular anatomy; they do not
establish our entry threshold or all-active replacement policy. BF-S13/14
support cost categories and donor inputs. BF-S06 supplies the exact PCS curve.
BF-Q01 explicitly selects the conservative policy for local testing.

For one enclosure, let `d` be external depth above local grade and `e=0.30m`:

```text
state = 0 if d <= e, otherwise 1
DR_active(state) = state
V_active = $1,050,000 × (96.3 + 17.5 + 7.5) / 141.3
         = $901,380.0424628449
conditional cost = DR_active × V_active
```

Use exact binary states. The existing artifact schema represents the lookup as
two points `(0,0),(1,1)`; **intermediate states are forbidden by the adapter**.
This avoids a schema change or fictitious smooth transition. It is not evidence
that damage physically jumps at one exact depth.

For each separate PCS, `h=max(0,d−0.30)` and `DR=FS_INV(h)` with linear
interpolation between the nine source knots, native h in 0–2m. At d=0.45m,
h=0.15m, DR=0.75 and cost is $390,000 on that PCS's $520,000 value.
Its entry is an explicit T4 local-test assumption; the T3 proxy shape does not
become OEM calibration. Battery and PCS denominators do not overlap.

The uniform-height battery curve, averaged battery hypotheses, whole-substation
transfer and storage-availability equation remain rejected. A full-enclosure
replacement stress case is not the selected candidate. No spontaneous-fire rate
or invented secondary uncertainty is introduced.

| Seven-step audit | Result for this local test |
|---|---|
| 1. Asset / event | Pinned 100MW/400MWh AC, 450MWh DC outdoor LFP; freshwater natural flood only |
| 2. Failure units | Repeated active enclosure and separate PCS; other property explicit |
| 3. Endpoint | Conditional hardware replacement-policy cost, not mean claims or downtime |
| 4. Split rows | Same-budget allocation from r3; no discarded residual |
| 5. Allocate value | 80×active value +20×PCS +$27.2896M unresolved = $109.8M |
| 6. Site adapter | Explicit entry policy; unique unit-local depths; no double height or area factor |
| 7. Apply / restrict | Local candidate only; invalid/unsupported inputs withheld; annual and complete-plant results withheld |

Numerical parameters retain T3/T4 tiers in JSON. Reopen when a matched utility
service rule, entry test, repair quote or materially different architecture
arrives. Owner approval makes the policy testable, not empirically true.
