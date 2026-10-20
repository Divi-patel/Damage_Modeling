# AGENTS.md — damage_modeling

> **Status — 🟡 new repo, docs-first (just spun out of `Hazard_modeling`).** It now holds the foundations,
> standards, contracts, cells, evidence, and source-drop records in shallow docs folders. The v2.5 ZIP is
> preserved as the raw source drop; repository-current runtime contracts now use bundle/capability v2 with
> pollable model+docs+schema+SHA pins. Durable runtime publishing is **step two**. Start at
> **[`docs/scope/SCOPE_AND_STORY.md`](docs/scope/SCOPE_AND_STORY.md)** — the end-to-end anchor.

**damage_modeling** is the **damage-curve / vulnerability layer** of InfraSure's risk platform. It turns
**hazard intensity → a damage ratio** at the right granularity, with full provenance, and emits a clean
**damage-code** object downstream systems consume. It does **not** compute EAL / PML / portfolio / financial
metrics — those belong to the consumer (the Hazard tier).

It was carved out of [`Hazard_modeling`](Hazard_modeling) because building the curve properly — granularity,
x-axis, curve form, coverage, provenance, value linkage, emit object — is a deep discipline in its own right
and should not clutter the hazard engine that merely consumes its outputs.

---

## Where it sits — a shared substrate feeding Hazard's M3

```
   1. PERFORMANCE  (model-gpr)        normal ops → P50/P90/P99
   2. HAZARD       (Hazard_modeling)  M0→M1→M2→[M3]→M4  → asset loss · EAL/PML/VaR
                                                   ▲
                                                   │ consumes versioned curve code
                          ┌────────────────────────┴──────────────────────┐
                          │  DAMAGE MODELING   (this repo)                  │
                          │  intensity → damage ratio, per failure-unit     │
                          │  provenance-carried · versioned curve packages  │
                          └─────────────────────────────────────────────────┘
   3. OVERALL                         performance + hazard → Total Loss
```

The damage curve used to live *inside* hazard M3 as a few borrowed curves. Now M3 **consumes** this repo's
published `damage_code()`; this repo **owns the physical vulnerability response**. The separate
`resiliency_modeling` discipline pins that response when a measure scenario needs it; it owns the measure
profile, applicability, operational state/failure/dependence, composition, scenario, and direct cost. Hazard
still owns execution and annual risk metrics. See the
[`Resiliency handoff`](docs/contracts/resiliency_handoff/README.md).

---

## The three-phase arc (where we are)

```
   PHASE 1  hazard-first ("IDF")  →  PHASE 2  damage from the ground up  →  PHASE 3  adaptation & resiliency
   a few borrowed curves             THIS REPO — build it properly          separate scenario discipline
   damage = assumed                  damage = built                         measures pin Damage + Hazard
```

This is a historical work arc, not a repository-ownership rule. Phase 3 now has its own
`resiliency_modeling` home because measure evidence, state/failure logic, composition, cost, and decisions
change independently from vulnerability artifacts and the Hazard engine.

Full story + tier/contract/migration detail: [`docs/scope/SCOPE_AND_STORY.md`](docs/scope/SCOPE_AND_STORY.md).

---

## The unit hierarchy (how a curve is organised)

```
   CELL  =  hazard × asset             (project-management unit; e.g. hail × solar)
     └── FAILURE-UNIT  =  what fails   (the curve-record / damage-code ATOM)
            └── SUBSYSTEM / COMPONENT  =  the value bucket the DR applies to
   ASSEMBLY:  loss = Σ_u  DR_u(x_u) · value_u     (sum, don't group; tile exhaustively; immune = DR≈0)
```

Riders: **coverage roles** (primary / secondary / conditioner-only / exposure-modifier / DR≈0, *per cell*) ·
the **selector (fixed attr) / conditioner (event-time state) / exposure (value touched)** split ·
**provenance is the deliverable** (every parameter → a source-ID or assumption-ID; standards *anchor*, they
are not curves).

> **Scope of the curve.** Physical **destruction only** (repair cost ÷ replacement value). Disruption
> (downtime → BI, derating) is a separate additive stage, not in the curve. v1 = single-site, occurrence
> basis, current-climate. The one open seam is the **spread** (secondary uncertainty).

---

## Repo map

| Path | What |
|---|---|
| `docs/` | All damage-curve docs. Index: [`docs/README.md`](docs/README.md). |
| `docs/scope/SCOPE_AND_STORY.md` | **The anchor** — scope, phases, tier/contract boundary, migration. |
| `docs/cells/` | Shallow entrypoints for current hazard × asset cells and canonical runtime artifacts. |
| `docs/contracts/` | Repo-level damage-code, artifact, capability, and Hazard handoff contracts. |
| `docs/method/` | Durable foundations, value-basis support, and global method standards. |
| `docs/evidence/` | Cross-cell evidence-ingestion protocol/register. |
| `docs/source_drops/` | Raw ZIP/source-drop landing zone: raw ZIPs, optional local extracted mirrors, manifests, and source context. |
| `docs/method/foundations/` | Principles (P1–P3) + the 6 question-docs + the assembled-curve-record spec. |
| `docs/method/standards/` | Global method standards from the v2.5 deliverable. |
| `docs/contracts/standards/` | Hazard-facing interface, artifact, capability, and versioning standards. |
| `docs/contracts/schemas/` | JSON schemas for curve bundles, damage emit, and capability declarations. |
| `docs/contracts/hazard_handoff/` | Hazard M2/M3 handoff notes. |
| `docs/contracts/resiliency_handoff/` | Damage producer boundary for Resiliency scenarios; links to the canonical cross-repo contract. |
| `docs/plans/` | Plans of record (README + `decisions.md` + `assumptions.md` per folder) with a dated ledger and [`_templates/`](docs/plans/_templates/README.md); Hazard-style stamps and the closed status vocabulary. [Index](docs/plans/README.md). |
| `docs/extra/discussion/` | Reasoning nodes — one bounded question each, ending in a verdict — with a dated ledger and [`_templates/`](docs/extra/discussion/_templates/README.md). [Index](docs/extra/discussion/README.md). |
| `docs/extra/tasks_history/` | Per-session handoffs; read the newest `handoff.md` first. [Index](docs/extra/tasks_history/README.md). |
| `docs/extra/learning_logs/` | Team-shared, non-canonical atomic lessons and complete newcomer/re-entry project learning packages. [Index](docs/extra/learning_logs/README.md). |
| `scripts/reference_helpers/` | Reference helper scripts only; not a stable `src/` API. |
| `data/` | Curve-record artifacts + manifests (large/binary gitignored). [README](data/README.md). |
| `notebooks/` | Companion notebooks per cell — `<hazard>/<asset>/00_curve_curation_walkthrough` + `01_runtime_curve_walkthrough`, reading the pinned artifact through the artifact index, never authoring one. **2 of 10 cells covered; both existing pairs currently fail (their loader targets the removed `docs/damage_curves/` tree).** Repair + the other eight cells: [`docs/plans/cell_notebook_coverage/`](docs/plans/cell_notebook_coverage/README.md). [README](notebooks/README.md). |
| `.github/workflows/` | CI (starter). |

### Cross-project symlinks (gitignored, local-only — machine-specific absolute paths, never commit)

| Link | → Points at | Why it's here |
|---|---|---|
| [`infrasure-damage-curves`](infrasure-damage-curves) | the **old** damage-curve repo | weak method, strong **evidence** — the harvest source (via implementation standard 16) |
| [`Hazard_modeling`](Hazard_modeling) | the **consumer** repo | M3 integration target; shared principles / plans / learning-logs live there |
| [`model-gpr`](model-gpr) | Performance-tier sibling | house-style reference (docs layout, venv conventions) |
| [`Learning`](Learning) | `~/Desktop/Learning` | domain knowledge base |
| [`renewablesinfo_org`](renewablesinfo_org) | renewables-info website / data org | renewables & asset context cross-reference _(role TBD)_ |

---

## What this repo owns — and does not

| OWNS | does **NOT** own |
|---|---|
| failure-unit granularity · x-axis · physical vulnerability response · supported selector/conditioner/exposure input semantics · provenance · value/assembly linkage · valid domains · KATs · the **emit object** + capability declaration | measure profile/applicability · measure state/failure/dependence · operator composition · scenario choices · direct cost · ancillary financing effects · hazard frequency/runtime · **EAL / PML / VaR / TVaR** · portfolio accumulation |

Damage declaring a conditioner input does not make it the owner of the process that sets that conditioner.
The boundary (and the EAL/PML resolution) is in
[`SCOPE_AND_STORY.md`](docs/scope/SCOPE_AND_STORY.md) §4, §6, and §8; the canonical three-repository contract
is linked from the [`Resiliency handoff`](docs/contracts/resiliency_handoff/README.md).

---

## Conventions

- **Single source of agent guidance = this file** (`AGENTS.md`); `CLAUDE.md` imports it.
- Mirror the house style of `Hazard_modeling` / `model-gpr`: `docs/` layout, gitignored local-only symlinks,
  plain `venv` + `requirements.txt`, a README per folder, `python3.12` for venvs.
- **Plans and discussion follow the Hazard ledger conventions**: every plan/node carries the five-field stamp
  (`author · created · updated · status · scope`), the status vocabulary is closed
  (`draft · proposed · active · settled · superseded · done`), each index is a dated ledger updated in the
  same commit as the doc, and new folders start from the tier's `_templates/`
  ([plans](docs/plans/README.md) · [discussion](docs/extra/discussion/README.md)). Agent-drafted work is
  stamped `owner-directed (<name>) · agent-drafted`; an owner ruling is never inferred.
- For any new ZIP/source drop, follow
  [`docs/extra/guides/source_drop_ingestion_guide.md`](docs/extra/guides/source_drop_ingestion_guide.md):
  preserve raw first, use `extracted/` only as a local mirror/staging area, inventory before moving, and
  promote only reviewed canonical material.
- For governed damage-curve changes, use
  [`docs/extra/guides/damage_curve_skill_usage_guide.md`](docs/extra/guides/damage_curve_skill_usage_guide.md)
  and the draft-operational skill bundle at [`docs/extra/damage_curve_skill/`](docs/extra/damage_curve_skill/):
  inside this repo, edit canonical folders directly; outside this repo, return a package/ZIP and ingest it
  through `docs/source_drops/`.
- **The cell-package standard** governs every new cell (`docs/method/standards/02_cell_package_standard.md`): README +
  derivation dossier + metadata spec + workbook + version registry.
- **Versioning** (standard 17): package version ≠ cell-damage-model version ≠ docs revision. The consumer
  pins the *cell-damage-model version*.
- **Provenance discipline** (standard 08 + P3): a reference is *input, not authority*; no orphan claims.
- **Validators need the `python3.12` venv.** Run `.venv/bin/python scripts/reference_helpers/validate_*.py`.
  A bare `python3` may be a Homebrew build without `expat`, which cannot read the `.xlsx` workbooks — every
  workbook-reading validator then fails with a misleading `No module named expat` ImportError.
- **`outputs/` is gitignored** — a regenerable render target. The canonical workbook for a cell always lives
  under `docs/cells/<cell>/{current,proposed}/`, never in `outputs/`.

### Syncing with the fork — check the direction first

`aamani-ai/Damage_Modeling` (remote `origin`) and `Divi-patel/Damage_Modeling` (remote `divi`) are **the same
project as this checkout**, not separate ones. Work happens on the fork because the work GitHub org has access
issues.

Do **not** assume the fork is ahead. Skill and agent runs write straight into this working tree, so the local
checkout is frequently the newer side with the work merely uncommitted. Before syncing, run:

```bash
git status --porcelain                              # uncommitted local work?
git rev-list --left-right --count main...origin/main # who is actually ahead?
```

On 2026-07-29 this mattered: both remotes sat at `f8b5ec3` from 2026-07-13 while the tree held ~180 files of
uncommitted work, including the tropical-cyclone (hurricane) cells. They looked missing only because they had
never been committed. The correct action was commit + push, not pull. If recent file mtimes are only minutes
old, a generation run may still be in flight — let the tree go quiet before staging.

> **Known cleanup.** The old `docs/damage_curves/` tree and the drifted
> `damage_curve_implementation/` copy were removed. Current docs now live under `docs/scope/`, `docs/method/`,
> `docs/contracts/`, `docs/cells/`, and `docs/evidence/`. The untouched raw ZIP remains under
> `docs/source_drops/raw_zips/`.

## Getting started

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Status

🟡 **New repo, docs-first.** Method mature (foundations + global standards + 8 current cells at model v1.0;
the original five plus canonical partial-screening `flood_wind`, Tier-4 `wildfire_wind`, and source-native
`tropical_cyclone_wind_wind` releases).
Portable v2.5 remains preserved; repository-current artifacts use the stricter v2 consumer seam. Durable
artifact publishing and automated Hazard M3 loading remain future system work.
