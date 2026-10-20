---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-10-15
updated: 2026-10-16
status: active
scope: Review and reuse of Junga's Flood Real Estate research, office-specific source checks, workflow entry points and the next Hazard–Damage integration work.
---

# Reuse Junga's research and continue from its actual state

**October 16 ownership update:** Junga owns Real Estate curve curation, including the office amendment
and the first references/reasoning documentation example. Hazard's immediate deliverable is three
defined physical profiles and a failure-mechanism Markdown guide; its next end-to-end numerical task is
Substation CONUS. The findings and future integration checks below are retained evidence, not an assignment
for Hazard to duplicate her research. Current authority:
[DD-RE6](../../../../Hazard_modeling/docs/plans/_cross_cutting/real_estate_conus/decisions.md#dd-re6-finish-the-profile-handoff-junga-owns-real-estate-damage).

Junga has already completed a substantial proposed Flood package. The useful next step is targeted review
and integration of that work, with a separate office amendment. A new search from an empty scaffold would
discard source registers, reference assumptions, curve extraction, pressure tests, an evaluator and tests
that we can inspect and reproduce now.

The user explicitly authorized using whatever available work is useful and confirmed that the missing
NFIP comparison is not a blocker. Shared scope and the warehouse-first sequence are recorded in the
[Hazard decisions](../../../../Hazard_modeling/docs/plans/_cross_cutting/real_estate_conus/decisions.md).

## What the Slack conversation adds

[Junga's latest message, October 12](https://aamani.slack.com/archives/D0ACH17MH7B/p1791819653636769),
links `cell/flood-real-estate`, describes Hazus freshwater/NACCS coastal candidates for house, small
commercial and warehouse, reports an NFIP claims comparison, and names hurricane wind as the next research
step. The inspected remote branch contains the Flood proposal; no corresponding hurricane building package
was located in the inspected branch list.

[Divy's October 8 direction](https://aamani.slack.com/archives/D0ACH17MH7B/p1791455461197249) already says
to build the grid pipeline on the warehouse first, then add the other two. It also separates CONUS reference
buildings from later OSM matching. The October 15 three-story office choice refines the earlier broad
retail/office candidate; it does not change the meaning of Junga's existing retail evidence.

The message reports roughly 106,000 NFIP claims from 2016–2026 and a freshwater/coastal comparison. The
inspected branch still lists claims comparison as open and contains no results supporting that report.
Divy has no newer copy. Record this as **reported, not verified**. Continue with the inspected source work;
do not reject NACCS, choose a replacement coastal curve or claim calibration on the basis of an unseen result.
If the analysis becomes available, inspect depth datum, occupancy, payout versus repair endpoint, limits,
coverage and selection before using it to judge these curves.

## Exact intake and reproducible checks

Source: [Damage branch](https://github.com/aamani-ai/Damage_Modeling/tree/cell/flood-real-estate), pinned at
`bc2752451189ac2ed56f6cc82253c4380df03720`. The
[intake receipt](junga_branch_intake_receipt.json) records all 29 imported new files and their hashes.
They were copied unchanged into the main working tree after checking for path collisions; the helper
index received four additive entries. This is an intake of an existing **noncanonical proposal**, not a
merge of all branch history or scientific promotion. Authorship and the original proposal are preserved.

The [cell entry](../../../cells/flood_real_estate/README.md) now makes the research discoverable locally.
Its validator passes **29 checks and 166 known-answer cases**, including schema checks, deterministic
artifact reproduction, source/claim references, monotonicity, workbook contents and withholding cases.
These are package/behavior checks. They do not establish national applicability, a claims-validated model
or a completed Hazard integration. No `current/` package, canonical artifact index or publication was changed.

```bash
.venv/bin/python -B scripts/reference_helpers/validate_flood_real_estate_v0_1_package.py
```

Run from the Damage repository with its Python 3.12 environment. Both the isolated branch snapshot and
the imported local package are covered in the intake receipt.

## What can be reused, and at which level

| Existing work | Disposition | Remaining qualification |
|---|---|---|
| Source/claim registers, source locators, extraction and pressure tests | Reuse as inspectable evidence | Retain inherited checks versus freshly reproduced checks distinctly |
| Hazus DF129 house and DF341 warehouse tables | Reuse as proposed source-native responses | Applicability, source structure-value scope, Hazard input/consumer fit and promotion |
| Hazus DF217 commercial table | Retain as retail evidence | It is COM1 retail; do not bind it to the selected office |
| NACCS 5A/P2/P3 tables and min/max envelopes | Retain as proposed coastal evidence | Prototype/region transfer, source domain and mechanism scope; bounds are not probability spread |
| Source-native whole-building structure assembly | Keep this grain for the first Flood proof | Reconcile fixed services/interiors; no added overlapping component loss |
| House 0.75 ft and commercial/warehouse 0.25 ft floor heights | Retain labeled assumptions and sensitivity candidates | Residential documented default versus T3 three-county nonresidential inference; not measured national building facts |
| Evaluator, builder and known-answer cases | Reuse as pinned reference implementation/oracle | Production consumer and per-record routing/range parity are not yet complete |
| NFIP finding reported in Slack | Track for later evidence intake | No data/report located; non-blocking, no numerical or source-choice authority |

The proposal's `FRE_BUILDING_STRUCTURE` is an assembly atom, not only the structural frame. Its name does
not prove that every item in our desired building/fixed-service/interior boundary is covered. Source-native
structure replacement cost new is the proposed denominator; the precise crosswalk remains work. Contents
are explicitly withheld. Waves, velocity and scour are deferred mechanisms, not zero-damage assumptions.

## Office: advance the research without relabeling retail

Junga already identifies COM4/DF431 as an office alternative and records a revisit condition if office is
selected. The owner has now selected it. This pass extracted that table from the pinned Plymouth carrier
and independently compared all 29 ordinates to the pinned primary USACE implementation. They match exactly.
The [office evidence receipt and table](../../../cells/flood_real_estate/research/README.md) record this check.

At 4 ft above first floor, the compared retail and office tables return 0.18 and 0.28 respectively. The
values demonstrate a material source distinction; they do not establish story-specific calibration. The
next amendment needs an explicit office selector, supporting claims and value scope, source-range tests,
and a coastal applicability decision. The original v0.1 retail artifact stays unchanged while that amendment
is researched. No office runtime ID is invented by this evidence check.

## The skill exists; choose the entry point that fits the change

The repository's [damage-curve-library-governance skill](../../damage_curve_skill/SKILL.md) is the operational
method. Local revision 0.7 adds the twin-to-scope and reuse step discussed with Divy. Its
[operator guide](../../guides/damage_curve_skill_usage_guide.md) explains inside-repository authoring; a ZIP
round-trip is unnecessary here. The workflow is deliberately conditional:

| Situation in this task | Entry and work required |
|---|---|
| Existing Junga proposal arrives from another branch | Inventory and pin it, reproduce its checks, assess applicability and preserve unmodified evidence |
| Same warehouse/house source and behavior remain suitable | Inherit completed research with exact pins; close missing value, capability and consumer proofs |
| Three-story office replaces the intended retail candidate | Use the existing-cell change workflow for an explicit proposed response/selector addition; compare old/new outputs where meaningful |
| New source/report, such as the missing NFIP analysis | Use evidence ingestion; classify whether it changes documentation, parameters, mechanism or reportability |
| A genuinely new hazard or unsupported mechanism | Use full intake/new-cell steps where scope and evidence are unsettled; reuse compatible anatomy, definitions and evidence |
| Consumer needs a new field or changed semantics | Separately classify and prove the contract/consumer change; skill revisions do not authorize runtime changes |

See [update-existing-cell workflow](../../damage_curve_skill/01_workflows/UPDATE_EXISTING_CELL_WORKFLOW.md)
and [evidence ingestion](../../damage_curve_skill/01_workflows/EVIDENCE_INGESTION_WORKFLOW.md).
Record inherited steps and the reason for skipping repeated work; retain the ability to trace every
output to evidence. The seven-step audit is an evidence map, not a demand to redo unchanged source work.
This branch application already has the needed skill route; another skill revision is not justified yet.

## Remaining integration work and repository maturity

A read-only test of Hazard's current common Deep loader reproduces a real gap: building-only selectors
cannot uniquely choose this proposal's freshwater/coastal/response-band records. A dry-grade request also
lacks the axis the common loader expects. Unknown water type is withheld correctly. The
[four-case receipt](../../../../Hazard_modeling/docs/plans/_cross_cutting/real_estate_conus/flood_consumer_probe.json)
and [profile/proof plan](../../../../Hazard_modeling/docs/plans/_cross_cutting/real_estate_conus/01_reference_profiles_and_flood_proof.md)
distinguish observed failures from domain/bridge work identified by inspection. Passing Damage's validator
does not make the current Hazard consumer ready.

The most useful maturity improvement is therefore a complete worked handoff: exact physical profile,
source-qualified assembly/value scope, emitted response, consumer parity, integrated annual semantics and
an inspectable result. A general framework rewrite would not resolve those missing facts. Keep qualified
cell-local responses while the shared-component standard governs any later runtime inventory.

Proceed warehouse first; finish the bounded freshwater proof while retaining coastal research. Continue
office/house qualification and other-peril discovery without making every pair a prerequisite. Do not
turn replacement cost per area, price year, floor area or source coverage into arbitrary numbers just to
produce dollars. Those are the next research tasks, and the shared plan records their acceptance criteria.

## Verdict

Use Junga's available work now, preserve its noncanonical scientific state, and amend only the mismatches
or missing proofs. The absent NFIP comparison is a deferred validation input. The office source check and
consumer probe move the research forward without implying a finished building Damage release or CONUS grid.
