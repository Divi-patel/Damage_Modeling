---
author: owner-directed (Divy) · agent-drafted
created: 2026-10-19
updated: 2026-10-19
status: active
scope: First-reader explanation of the local BESS wind candidate
---

# What this candidate means

Wind can damage an enclosure, its installation or the equipment inside. Those
are related outcomes, but an enclosure dent is not proof that every battery
needs replacement. The first local policy counts integrated replacement at
the assumed **major compromise state**, keeping repair as an alternative.

```text
event wind + compatible reference -> local pressure ratio
    -> assumed exact-state probabilities
    -> repair/replacement cost for the same physical unit
```

Our unit is one integrated $1.05M battery enclosure or one separate $520,000
PCS. Cells, management, cooling, racks and safety are already inside the cabinet
value. The source anatomy is illustrative/related evidence; the probabilities
and mapping to repair states are explicit T4 assumptions, not observed damage.

```text
cost within one enclosure
  no repair       limited composite       major compromise      destructive
      0                $148,620               $1,050,000           $1,050,000
  repair sensitivity at major compromise:    $204,352
```

A conditional mean averages the assumed state costs at a given demand. At a
pressure ratio of 1, the inherited central probability model gives approximately
$327,948 mean enclosure cost under replacement, versus $170,965 under repair.
Neither means every enclosure costs that amount to fix. The major state's
cost is still $1.05M under the selected policy. These conditional probabilities
are not the annual chance of a hurricane.

Missing demand, wrong wind basis, unsupported property and demand above the
source's ratio-2 domain return no DR/cost. A zero at zero demand is a modeled
conditional zero, not immunity to other mechanisms. No EAL, PML or TVaR is
available from this candidate alone.

Continue with [how it was built](HOW_THE_MODEL_IS_BUILT.md) and
[the exact reference](MODEL_REFERENCE.md).
