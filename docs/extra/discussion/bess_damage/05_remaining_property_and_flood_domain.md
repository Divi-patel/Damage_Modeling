---
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Remaining BESS property disposition; deep-water continuation; coastal repair-policy comparison
---

# BESS Flood: finish the bounded review before extending the candidate

**Recommendation:** carry the existing battery/PCS scope into a separately
versioned local candidate with explicit saturation at deeper freshwater depths.
Keep the remaining property visible and unmodeled for this bounded proof. For
coastal testing, review the single new repair-policy choice in **BF-Q02** below.
Neither a transformer assumption nor an invented budget split should delay the
unaffected battery/PCS work.

This review is `EVIDENCE_ONLY_NO_OUTPUT_CHANGE`. The local v0.1 model, its four
consumption pins, profile, runtime code and capabilities are unchanged. There is
no new annual-loss or national-map authorization in this record. Changing the
depth domain or coastal behavior is a subsequent `MODEL_BEHAVIOR_CHANGE`, even
if all previously supported freshwater inputs retain their old outputs.

## 1. What this pass resolves

The [Riverine proof](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/05_riverine_local_proof.md)
left two different issues: 876 known depths beyond a chosen test limit and
8,649 missing hazard inputs. We can address the first without rebuilding M0/M1.
The review also closes the present search for a defensible subdivision of the
remaining $27.290M. Its result is a documented partial scope, not a claim that
the remainder is undamageable.

| Evidence step | Completed result |
|---|---|
| Define scope | Same 100 MW / 400 MWh reference; direct physical equipment loss; no collector station/export line |
| Identify failure units | Preserve battery active hardware and separate PCS; distinguish transformer tank, controls, switchgear, cable body/ends and civil work |
| Inspect prior sources | Revisit NEMA, Solar electrical curves, SMA anatomy, NREL/PVSCM and the twin cost code |
| Targeted primary search | Schneider recovery bulletin, EIA standalone-BESS cost case and NEMA's 2026 edition announcement |
| Reproduce numbers | 70 checks; exact replay of all 43,800 saved v0.1 cases; capped continuation comparison |
| Decide current treatment | Recommend deeper freshwater saturation; residual value withheld; one coastal policy question |
| Retain next work | Specific evidence and acceptance conditions below; annual and national use still separate gates |

Sources and claims: [registers](evidence/README.md), especially BF-S16–S19 and
BF-C23–C29. Exact access outcomes, local hashes and locators are in
[r4 captures](evidence/r4/source_captures.json). The
[bounded-search record](02_bounded_search.md#fourth-bounded-pass--remaining-property-and-water-conditions-2026-10-18)
preserves the unsuccessful access as well as the useful evidence.

## 2. Remaining property: what can and cannot be reused

| Remaining budget | Amount | Current disposition and reason |
|---|---:|---|
| Container, racks and fire-safety composite | $11.890M | No separated fire/electronics/structure value. Do not apply an electronics curve to the entire composite. |
| Electrical balance | $13.200M | Contains MV equipment, cables, grounding and controls. Candidate responses exist for some failure units, but their same-unit values are not allocated. |
| Civil works | $1.600M | Depth alone does not establish erosion, scour or foundation damage. No zero-damage inference. |
| Fieldwork | $0.600M | Installation allowance; not an independent object that fails. Allocate to repair actions later without charging labor twice. |
| **Total still unmodeled** | **$27.290M** | **24.854% of the unchanged $109.8M reference value.** |

The existing local candidate covers **$82.510M / 75.146% of reference value**.
These percentages describe value membership, not the fraction of actual losses
captured. Do not divide candidate losses by 75.146% to manufacture a whole-plant
loss. The [disposition CSV](evidence/r4/remaining_property.csv) gives the reusable
response, missing input and next test for each group. Child rows have no new
dollars; they do not duplicate the parent budgets.

Three findings justify the boundary:

- **Transformer and switchgear repair are not interchangeable.** Schneider's
  [2011 bulletin, pp1–2](https://ckm-content.se.com/ckmContent/sfc/servlet.shepherd/document/download/0691H00000EDoYrQAL)
  distinguishes electronic/dry-type equipment requiring replacement from larger
  equipment that may be reconditioned, including liquid-filled transformers.
  SMA's adjacent storage-station manual separately identifies tank, bushings,
  tap changer and monitoring devices (BF-S12, pp31–32). A low controls datum
  cannot qualify full-transformer destruction. This does not establish immunity
  of a submerged tank or settle our target transformer construction.
- **The public BESS budget remains aggregated.** The
  [EIA/Sargent & Lundy case, pp113–116](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf)
  describes a 150 MW / 600 MWh plant and separates main substation cost. Its
  $36.857M BOP line still combines inverters, unit transformers, cables,
  foundations and controls. It supports scope checking, not a measured split of
  our $13.2M. It is a 2023-dollar EPC case, not our 2024-dollar replacement budget.
- **The twin's finer split is illustrative.** BF-S19 explicitly marks estimates.
  Its $14/kWh MV bucket gives $5.6M at 400 MWh; the 62% transformer allocation is
  $3.472M, or $173,600 per 20 units. That is useful plausibility evidence, but the
  controls allocation elsewhere gives $896,000 while the equipment card shows
  $40,000–$120,000 per plant. Do not treat internally inconsistent estimates as
  independent quotes. The older PVSCM donor also includes solar-specific items.

NEMA announced **CS 70006-2026** on May 28, 2026 (BF-S18). We read the official
announcement but could not retrieve the new guide body. GD 1-2016 remains an
inspected historical source, not a claim that we reviewed the latest edition.
The current Schneider FAQ still links its dated 2011 bulletin. Keep issue dates
separate from website update dates.

## 3. Deeper freshwater: retain the replacement ceiling

For the same covered hardware, replacement cost cannot keep increasing merely
because water gets deeper. The proposal is a **T4 continuation rule**, not new
empirical flood calibration:

- Battery active hardware: retain the approved strict `depth > 0.30 m` rule
  and its $901,380.04 per-enclosure ceiling.
- PCS: preserve every source knot; it reaches DR=1 at 0.60 m above entry
  (0.90 m above grade). Continue at DR=1 beyond the last source knot.
- Accept finite nonnegative freshwater depths; retain missing/invalid source
  status. No linear extrapolation, new multiplier or enlarged covered value.
- This is capped equipment replacement only. Additional cleanup, contamination,
  debris, scour, external property and full-plant consequences are not silently
  covered. The result is neither an empirical mean nor a whole-plant upper bound.

| Same uniform external depth, for illustration | One active enclosure | One PCS | All 80 enclosures + 20 PCS |
|---|---:|---:|---:|
| 0.30 m | $0 | $0 | $0 |
| 0.45 m | $901,380 | $390,000 | $79.910M |
| 0.90 m | $901,380 | $520,000 | $82.510M |
| 3.00 or 10.00 m, proposed continuation | $901,380 | $520,000 | $82.510M |

The last row is currently withheld by v0.1. The
[saved-case comparison](evidence/r4/audit_receipt.json) recovers **701 enclosure
and 175 PCS cases**: available cases increase from **34,275 to 35,151**, while
**8,649 missing-hazard cases stay missing**. Diagnostic placement/RP cases with
all 100 candidate units evaluable increase from **305 to 330 of 438**. All
previously supported amounts reproduce exactly within floating-point tolerance.

These deliberately selected controls are not a CONUS sample. A repeated-RP sum
is not a synchronized event loss, EAL or PML; no annual quantity is computed.

## 4. BF-Q02: one coastal policy choice

**Question:** for the next local coastal test, should saline water above the
assumed 0.30 m entry trigger replacement of the covered PCS hardware, as it does
for the active battery group?

**Recommendation: yes, as an explicitly conservative local-test hypothesis.**
Salt exposure and contaminated equipment guidance support caution, but do not
give a calibrated salinity multiplier or our exact enclosure ingress behavior.
This choice deliberately avoids claiming a measured average. The main risk is
overstating loss near entry, particularly when only part of a PCS needs repair.

| Coastal what-if at 0.45 m | Active battery hardware, one enclosure | PCS, one unit | Difference |
|---|---:|---:|---:|
| Transfer the existing gradual PCS proxy unchanged | $901,380 | $390,000 | Baseline hypothesis; salinity effects unquantified |
| **Replace covered hardware after entry** | **$901,380** | **$520,000** | **+$130,000 per affected PCS** |

At uniform 0.45 m depth across all candidate units, the difference is $2.6M,
or 2.368% of full TIV. At 0.90 m or deeper both reach the same equipment ceiling.
Below or exactly at entry, both direct-entry hypotheses return zero; this does
not claim all routes to water damage are impossible. Neither option supplies
the remaining $27.290M or grants wave/scour protection. Unknown water condition
still remains unknown. Freshwater shall not be relabeled to bypass this choice.

**State: OPEN, local-test choice only.** The research helper compares the two
alternatives; it is not imported by runtime. Do not record owner approval until
an actual reply arrives. The approved BF-Q01 rule remains intact.

## 5. Bounded next work and future research

Proceed to a new local candidate after BF-Q02: preserve all v0.1 freshwater
answers; add explicit saturation and the selected coastal treatment; bind the
existing Coastal source and test positive, dry, missing and deep cases. No new
hazard model or additional whole-budget valuation search is required for that
partial-scope proof. Then qualify conditional-to-annual use separately, including
common-event meaning, coverage, value caps and the resolution pilot.

| Follow-up | Trigger / acceptance condition | Owner / priority |
|---|---|---|
| Allocate MV/controls/cables | Consistent target BOM or defensible unit quotes; preserve $13.2M and separate tank from controls and cable body from terminations | Damage + Hazard value owner; before a complete-property claim |
| Split composite and repair work | Matched service/budget evidence; no overlapping shell/fire/electronics or repeated labor | Damage + value owner; future coverage improvement |
| Replace ingress/repair policies | Configuration-matched water ingress or service results; compare near-entry dollars before changing the model | Damage; high-value refinement |
| Review NEMA 2026 body | Accessible official full guide; compare exact equipment rows and resolve any conflict with historical sources | Damage; targeted source upkeep |
| Extend beyond direct inundation | Source-supported wave/velocity/scour/cleanup demand and matching physical endpoints | Peril + Damage owner; separate scope, not an invented depth modifier |

The curation skill already requires this bounded outcome, source/claim registers,
pressure tests and future triggers. No skill rewrite is necessary in this pass.
The useful lesson is practical: **resolve the covered response and retain the
uncovered denominator; do not turn an incomplete cost split into a whole-asset
curve or an unlimited search.**
