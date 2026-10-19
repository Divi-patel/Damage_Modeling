<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: settled
scope: First bounded BESS Flood evidence/reuse decision; later numerical qualification remains active
-->

# First Flood review: what transfers, and what needs a BESS model?

**Use the existing electrical research, but develop the battery response at the
enclosure boundary.** The missing link is how external water reaches vulnerable
contents and what then needs replacement. Neither a whole-substation curve nor
an equipment-outage probability answers that question for a battery plant.
This review closes the first evidence-search pass, not the BESS modeling task.

## 1. The physical and monetary target

The [Hazard reference](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/01_reference_profile_and_value.md)
has 80 battery enclosures, 20 separate PCS groups, 20 unit-MV groups and shared
controls/collection. Its direct physical budget is **$109.8M in 2024 dollars**.

| Budget group | Value | Share | Research treatment |
|---|---:|---:|---|
| Integrated battery enclosures | $84.0M | 76.50% | Main new response; preserve embedded cooling/BMS/safety |
| PCS | $10.4M | 9.47% | Test existing inverter response as an explicitly qualified proxy |
| Internal electrical/MV/controls | $13.2M | 12.02% | Existing evidence helps; finer monetary split remains unresolved |
| Civil reinstatement | $1.6M | 1.46% | Separate damage mechanism; a wet yard does not imply destroyed concrete |
| Installation | $0.6M | 0.55% | Allocate once to physical work, not an independent damage curve |

These are budget shares, **not admitted damage coverage**. One enclosure has an
equal hardware allocation of $1.05M; one PCS group has $0.52M. Neither includes a
pro-rata share of every other plant component by default. All ten source budget
rows, including exclusions, reconcile in [the value crosswalk](evidence/value_crosswalk.csv).

## 2. What the primary evidence actually supports

Exact URLs, locators, source roles and prohibited inferences are in the
[source register](evidence/sources.csv); load-bearing decisions are linked in the
[claim register](evidence/claims.csv).

- **NEMA GD 1-2016:** its water-damaged equipment table lists batteries for
  replacement; its electronics discussion also allows manufacturer-led
  evaluation/reconditioning. It distinguishes equipment types and water
  conditions. This supports consequence reasoning **after relevant equipment is
  water-damaged**, not a probability that water outside a sealed container causes
  damage or that every integrated enclosure part must be replaced. The table's
  column alignment was visually checked. [BF-S02; BF-C01]
- **Tesla industrial ERG revision 2.8:** covers Megapack/Powerpack and contains
  flood shutdown precautions and damaged-product handling. It gives no
  depth-versus-repair-cost function. It is useful safety/mechanism context, not
  evidence that our synthetic LFP enclosure shares a particular Tesla design or
  containment performance. [BF-S03; BF-C02]
- **Chen et al., Processes 2025, equation 28:** models storage-node failure
  probability from flood depth. It does not establish an LFP enclosure repair
  ratio. The rendered equation leaves depths at/above its upper threshold
  undefined; the reviewed text does not supply a calibrated battery-specific
  parameter set. Retain as a model-form lead, reject direct numerical transfer.
  [BF-S04; BF-C03]

The [bounded search](02_bounded_search.md) did not locate a directly usable
external-depth-to-LFP-enclosure-repair-cost dataset. This is not a claim that such
evidence does not exist. Several public sources address safety, system outages
or siting rather than the required endpoint.

For completeness, the paper's interior expression is
`p = zeta * exp(gamma * (d - base) / protection_height)`. For positive `gamma`,
the lower right-hand limit is `zeta` while its lower branch is zero; probability
boundedness requires an appropriate constraint on `zeta * exp(gamma)`. Its
printed upper endpoint has no branch. These are analytic checks, not fitted
BESS parameters. We have not filled in coefficients, capped a guessed function
or equated this functional-failure probability with economic DR.

## 3. Existing curves: reproduce first, qualify second

Five Solar electrical records were evaluated at every native knot, every
midpoint and both sides of their stated depth domain: **95 source-response
evaluations**. [Audit receipt](evidence/audit_receipt.json).
The unchanged reference helper reproduces the knot values, monotonicity and
bounded response. Its endpoint clamping is documented as helper behavior,
**not permission to extend a new BESS model's valid domain**.

| Existing record | BESS disposition | Reason |
|---|---|---|
| `FS_INV` | Priority PCS proxy candidate; not yet admitted | Similar power-electronics function; validate target construction, critical datum and whole-group replacement scope |
| `FS_SWG` | Unit-MV switchgear candidate only | Applies to compatible switchgear, not automatically transformer/RMU/skid as one value |
| `FS_XFMR` | Reject automatic whole-MV transfer | Existing shared review flags control-waterline versus main-transformer value mismatch |
| `FS_SCADA` | Limited electronics candidate | Plant monitoring is not all protection, communications and station-service equipment |
| `FS_CABLE` | Mechanism/termination candidate | Wet-rated cable body, ends and conduits need different exposure treatment |
| Whole-substation Hazus | Reject as whole-BESS model | Wrong inventory, internal heights and replacement denominator |

The existing numerical shapes are **engineering T3 proxies**, not measurements
published by NEMA. Their provenance must retain that distinction after reuse.

An audit-only example makes the denominator issue visible: `FS_INV` gives DR
0.75 at **0.15 m above its own critical datum**. Applied to the $10.4M PCS
hardware, that is $7.8M (7.10% of the plant budget). Applied incorrectly to the
whole $109.8M plant, it becomes $82.35M. This is not a predicted BESS loss, and
0.15 m here is not automatically 0.15 m above site grade. [BF-C04]

## 4. Seven-step audit and interface

| Step | Result | Remaining work |
|---|---|---|
| 1. Asset/boundary | Pinned reference, chemistry, units, exclusions and value vintage | Runtime projection when first response is bound |
| 2. Failure units | Enclosure / PCS / compatible MV and control parts / civil | Keep source-native bundles; do not invent cell/rack counts |
| 3. Loss endpoint | Expected direct repair/replacement cost divided by pre-event value of the **same unit** | Qualify replacement scope for each response |
| 4. Value rows | All ten rows reconciled, including excluded fractions | Disaggregate $13.2M electrical bucket only when useful and supported |
| 5. Allocation | Equal identical enclosure/PCS allocations are explicit arithmetic | Installation allocation and mixed electrical subshares not selected |
| 6. Exposure adapter | Separate external water level, local grade, mounting and vulnerable-entry datum | Qualify ingress; preserve duration/water quality and unknown states |
| 7. Response/loss | Existing source records reproduced; no BESS curve admitted | Bounded candidate derivation, physical applicability and consequence checks |

Candidate causal chain:

```mermaid
flowchart LR
  A[Existing Flood hazard: depth or water level] --> B[Local exposure and reference geometry]
  B --> C[Water reaches vulnerable equipment]
  C --> D[Inspection / repair / replacement state]
  D --> E[Same-unit direct physical loss]
  E --> F[Once-only support costs and plant aggregation]
```

For a compatible datum, `h = max(0, water_level - critical_elevation)`. The
0.30 m reference mounting base is geometry; it is not yet a validated ingress
barrier. The existing Pluvial ponding method also uses a 0.30 m cap. Therefore a
simple base-overtopping calculation would have zero positive depth above the base
throughout that capped domain. Test and explain that outcome; **do not lower the
base, raise the hazard cap or assume bypass ingress simply to obtain loss**.
Riverine/Coastal may exercise different demand ranges. [BF-C05]

| Related effects | Single treatment | Avoid | Missing-data behavior |
|---|---|---|---|
| Mounting and ingress | One declared local-exposure transformation | Subtract height twice; equate pad top with lowest vulnerable entry without evidence | No inferred protection claim |
| Enclosure rating and seal performance | Qualified construction/ingress response | IP label as numeric flood discount | No invented coefficient |
| BMS/cooling/fire equipment | Included within $84M enclosure hardware unless budget is repartitioned | Separate added losses on already included hardware | Preserve bundle |
| Direct wetting and triggered thermal damage | One compatible consequence chain, capped once per unit | Count a replaced enclosure twice | Unquantified escalation remains visible |
| Isolation and stored energy | State-conditioned evidence, if available | Assume disconnect removes all stored energy or damage | No automatic de-energization credit |
| Installation and hardware | Support allocated once after direct work is known | Independent installation DR plus installed-cost curve | Withhold complete total until reconciled |
| Freshwater and saline | Separate evidence/disposition under inundation | Uncalibrated saltwater multiplier | Mark unsupported condition explicitly |

## 5. Verdict and next bounded step

1. **Battery first:** draft the simplest enclosure-level ingress/consequence
   hypothesis, with a separate ledger for sourced facts and engineering choices.
   Compare partial internal replacement with whole-enclosure replacement only
   where the source supports those consequences. Do not require electrochemical
   simulation or invent a “middle” percentage.
2. **PCS alongside it:** test `FS_INV` transfer against the selected separate-PCS
   architecture. Its $10.4M hardware allocation is already available. This is a
   useful candidate, not an 86%-complete plant response.
3. **Use representative depths before a map:** include dry/no-contact, equality
   at the chosen datum, shallow ponding, deeper inundation, invalid/missing
   demand and freshwater/saline differences. Confirm first whether the input
   supports the mechanism. Source curves do not validate exposure by themselves.
4. **Keep research finite:** the broad search stops here. Next retrievals must
   answer a specific ingress, repair-unit or same-unit-cost question. Record an
   explicit engineering screening assumption if defensible; escalate only a
   material unresolved product choice. Existing hazard physics is reused.

No hazard rebuild, national run, change to an existing Solar/Wind/Substation
curve, autonomous failure-rate model or recipient publication is part of this
checkpoint. Scaling to other MW/MWh sizes remains a required later
[production handoff](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/03_scaling_and_production_handoff.md).
