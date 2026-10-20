# Guide: Using The Damage Curve Skill

Use this guide when deciding whether `damage_curve_skill` should operate directly inside this repo or as an
outside package-building workflow that returns a ZIP/source drop.

## Short Answer

`damage_curve_skill` is the governance engine for changing the damage-curve library.

It has two operating modes:

```text
Mode A - inside repo
  edit the canonical repo folders directly

Mode B - outside repo
  edit a package working copy and bring the result back as a ZIP/source drop
```

The ZIP/source-drop path is only needed for outside work. If work happens inside this repo, do not route it
through a ZIP.

## Starting a new asset family

Before choosing cell names or searching for a curve for every illustrated part, follow the skill's
[intake and reuse guide](../damage_curve_skill/02_design_guides/ILLUSTRATIVE_ASSET_INTAKE_AND_REUSE.md).
Preserve the idealistic reference, decide the initial physical scope, map anatomy to evidence-supported
response units and inspect existing reusable inventory. The
[Real Estate flow review](../discussion/real_estate_conus/02_flow_and_reuse_review.md) records the first
application and current implementation limits. The
[Substation worked review](../discussion/substation_damage/README.md) applies the same intake to an existing
assembly curve with exact pins, numerical checks and unresolved physical/value qualifications. Revision 0.8
clarifies this progress record and the distinction between curve spread and annual hazard variability.
Numerical admission still follows the existing workflows.

## Core Picture

```text
damage_curve_skill
  = classify change + choose workflow + enforce versioning + validate release

docs/source_drops/
  = bridge for package work that happened outside this repo

canonical repo folders
  = live repo state used by readers and future Hazard integration
```

## Mode A: Use The Skill Inside This Repo

Use this when the current work is being done directly in `damage_modeling`.

```text
user change request
  |
  v
read docs/extra/damage_curve_skill/SKILL.md
  |
  v
classify the change
  DOCS_ONLY
  EVIDENCE_ONLY_NO_OUTPUT_CHANGE
  MODEL_BEHAVIOR_CHANGE
  NEW_CELL_SCAFFOLD
  NEW_CELL_MODEL_RELEASE
  SCHEMA_CONTRACT_CHANGE
  PACKAGE_ONLY
  |
  v
choose workflow under docs/extra/damage_curve_skill/01_workflows/
  |
  v
edit canonical repo folders directly
  docs/cells/
  docs/contracts/
  docs/method/
  docs/evidence/
  scripts/reference_helpers/
  |
  v
validate links / hashes / versions / no src
  |
  v
commit
```

No ZIP is needed in this mode.

### Inside-repo examples

```text
"Add a guide explaining how to request the hail_solar curve"
  -> DOCS_ONLY
  -> edit docs/extra/guides/
  -> no model version bump

"Update hail_solar stow logic with a behavior-changing formula"
  -> MODEL_BEHAVIOR_CHANGE
  -> edit canonical cell docs/artifacts
  -> bump hail_solar cell model version if outputs change

"Start tornado_solar as a scaffold"
  -> NEW_CELL_SCAFFOLD
  -> create shallow cell docs only
  -> do not call it v1.0 until runtime artifact and capability declaration are reviewed
```

## Mode B: Use The Skill Outside This Repo

Use this when someone works outside the repo, produces a portable package, and later needs that package
plugged back into `damage_modeling`.

```text
outside workspace
  |
  v
latest library package or exported repo snapshot
  +
damage_curve_skill/
  |
  v
classify change + apply workflow
  |
  v
produce governed package / ZIP
  |
  v
place ZIP in docs/source_drops/raw_zips/
  |
  v
follow docs/extra/guides/source_drop_ingestion_guide.md
  |
  v
inventory and compare
  |
  v
promote reviewed material into canonical repo folders
  |
  v
keep raw ZIP as preserved source material
```

In this mode, `docs/source_drops/` is the bridge. It is not the final navigation layer.

### Outside-repo examples

```text
"A researcher sent a ZIP with new flood_solar evidence"
  -> preserve ZIP in docs/source_drops/raw_zips/
  -> extract only as local/staged mirror
  -> inventory before moving
  -> promote only reviewed evidence/cell docs/artifacts

"A vendor used the skill outside the repo to build a new package"
  -> ingest package as source drop
  -> compare against canonical repo
  -> decide what is duplicate, new, or conflicting
  -> promote clean canonical changes
```

## What Goes Where

| Thing | Normal home |
|---|---|
| Current human-readable cell pages | `docs/cells/<cell>/` |
| Repo-level Hazard contracts | `docs/contracts/` |
| Durable modeling method | `docs/method/` |
| Cross-cell evidence protocol/register | `docs/evidence/` |
| Raw source ZIPs and original drops | `docs/source_drops/raw_zips/` |
| Local extracted source mirrors | `docs/source_drops/extracted/` |
| Operator guides | `docs/extra/guides/` |
| Skill/governance workflow bundle | `docs/extra/damage_curve_skill/` |
| Stable runtime library/API | deferred `src/`, not created yet |

## How This Relates To New ZIPs

When a new ZIP arrives, first decide what it is:

```text
new ZIP
  |
  +-- raw source material from research/vendor?
  |     -> source-drop ingestion guide
  |     -> preserve raw
  |     -> inventory
  |     -> promote only reviewed content
  |
  +-- governed package produced by damage_curve_skill outside repo?
  |     -> source-drop ingestion guide
  |     -> compare package contents with canonical repo
  |     -> update canonical folders only after review
  |
  +-- working material generated inside this repo?
        -> probably no ZIP needed
        -> commit canonical repo changes directly
```

## Source Drop vs Skill

```text
source_drop_ingestion_guide
  job: safely bring outside ZIP/source material into the repo

damage_curve_skill
  job: decide how a damage-curve-library change should be classified,
       versioned, validated, and released
```

They work together, but they are not the same thing.

## Non-Negotiable `src/` Rule

`src/` means this repo now has a stable importable library/API that Hazard can depend on.

Do not create or promote `src/` until the runtime path is decided:

```text
- cloud bucket layout;
- artifact publishing/versioning;
- how Hazard loads the curve;
- whether this repo publishes code, data, or both;
- version pinning and compatibility rules.
```

Until then, helper Python stays under reference/script material, not a stable importable API.

## Acceptance Checklist

Before saying a new package/source-drop/skill-driven update is complete, check:

```text
[ ] change class is recorded;
[ ] mode is clear: inside_repo or outside_package;
[ ] raw ZIP/source material is preserved if it came from outside;
[ ] duplicate extracted folders are not promoted as canonical navigation;
[ ] canonical docs/artifacts are updated only after comparison;
[ ] version impacts are explicit;
[ ] model version bumps only when runtime behavior changes;
[ ] links and references are updated;
[ ] validation output is recorded;
[ ] no src/ was created by accident.
```
