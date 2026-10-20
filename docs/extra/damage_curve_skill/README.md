# damage_curve_skill

Evergreen governance skill for evolving the damage-curve library.

This folder can be used in two ways:

```text
inside_repo
  use it inside damage_modeling and edit canonical repo folders directly.

outside_package
  use it beside a current damage-curve-library package/folder and return a governed ZIP/source drop.
```

It is not named after v2.5, v2.6, or any future package because its job is to govern the transition from the
current library state to the next reviewed state. A ZIP is only required when the work happens outside this
repo and needs to be brought back through `docs/source_drops/`.

```text
canonical damage_modeling repo
        or
latest damage-curve-library package/folder
        +
damage_curve_skill/
        |
        v
classified change request
        |
        v
selected workflow
        |
        v
updated cells / artifacts / standards / registries
        |
        v
validated canonical repo change or next release package
```


## First-time reader path

Start with:

```text
FIRST_TIME_READER_GUIDE.md
```

That file explains what this skill is, why it exists, how it relates to the damage-curve library, how to use it with Codex/OpenAI agents, and how the version streams stay separate.

## New asset or illustrative twin

Start with [the intake and reuse guide](02_design_guides/ILLUSTRATIVE_ASSET_INTAKE_AND_REUSE.md)
when scope and response grain are not settled. Revision 0.7 adds this pre-cell step and asset-appropriate
value prompts; it preserves existing cell/runtime authority and version streams.

Revision 0.8 adds an explicit qualification-progress record and distinguishes retained versus newly
verified source evidence. It also aligns annual-tail guidance with the existing consumer ownership and
reportability rules. See the [changelog](SKILL_CHANGELOG.md) and [validation report](VALIDATION_REPORT.md).

## Main use case

Use this skill when a user says something like:

```text
Add solar × tornado.
Update hail_solar with this new report.
Decide if this parameter change requires a model bump.
Promote this scaffold to v1.0.
Add a new required JSON field.
Rebuild wind_tornado_wind with separate straight-line-convective and tornado pathways.
Package the next release zip.
```

The skill should answer five questions before any edit is made:

```text
1. Are we in inside_repo mode or outside_package mode?
2. What kind of change is this?
3. Which workflow applies?
4. Which version streams must bump?
5. Which validation gates must pass before release/commit?
```

## Why this exists

The damage-curve library now has multiple independent version streams:

| Version stream | Meaning | Bump when |
|---|---|---|
| Package release | The whole zip/delivery bundle | Any shipped package content changes |
| Cell damage-model version | Runtime damage behavior for one hazard × asset pair | Same inputs can produce different damage outputs |
| Cell documentation revision | Proof trail, rationale, metadata, crosswalks | Explanation/auditability changes without behavior change |
| Schema/artifact version | Machine contract | Required fields or field meanings change |
| Skill upload/version | This operating manual as a reusable skill | The governance process itself changes |

The skill keeps those streams separate so that a docs improvement does not look like a curve change, and a new hazard × asset scaffold does not look like a calibrated runtime model.

## Current skill status

```yaml
skill_revision: 0.6
status: controlled-use
library_package_version_impact: none
cell_model_version_impact: none
schema_version_impact: none
```

Revision 0.6 adds the governed multi-pathway rebuild workflow demonstrated by the proposed `wind_tornado_wind` v2.0 research program. It requires an explicit `pathway_id`, pathway-specific axes/evidence/records/capabilities/tests, consumer migration and pin checks, and fail-closed support at pathway × failure-unit grain. It changes this evergreen operating manual, not any released damage curve, artifact schema, or runtime by itself.

## Folder map

```text
damage_curve_skill/
  START_HERE_FOR_FIRST_READER.md   First-reader bridge: what this is, why it exists, how to use it
  SKILL.md                         OpenAI-compatible skill manifest + core instructions
  README.md                        This overview
  CODEX_SKILL_GUIDE.md             Practical Codex/OpenAI skill usage guide
  FIRST_TIME_READER_GUIDE.md       First-time/Codex onboarding: what this is, why it exists, how to use it
  CODEX_SKILL_ONBOARDING.md        How to place/invoke this folder in Codex-style usage
  OPERATING_PRINCIPLES.md          The philosophy and invariants
  OPENAI_SKILL_USAGE.md             How to package/invoke as a skill
  ROADMAP_AND_PROMOTION.md         How to test and promote this skill
  SKILL_CHANGELOG.md               Internal change log for the evergreen skill
  agents/openai.yaml               Optional OpenAI UI metadata for this skill

  00_governance/                   Change classification, versioning, lifecycle, deprecation, logs
  01_workflows/                    Task workflows: add, update, evidence, schema, release
  02_design_guides/                How to design cells and curve records
  03_contracts/                    Runtime JSON, damage emit, capability, field aliases
  04_validation_qc/                QA, cap-binding, known-answer tests, reportability
  05_release/                      Release notes, manifests, package assembly
  06_examples/                     Worked governance examples
  templates/                       Copy-forward templates
  registries/                      Schema and seed registry examples
  tests/                           Governance smoke tests
  tools/                           Small helper scripts
```

## Recommended first read

```text
1. FIRST_TIME_READER_GUIDE.md
2. SKILL.md
3. 00_governance/CHANGE_CLASSIFIER.md
4. 00_governance/VERSIONING_POLICY.md
5. 01_workflows/ADD_NEW_CELL_WORKFLOW.md
6. 02_design_guides/EVIDENCE_PRESSURE_TEST_AND_FAIL_CLOSED_CHECKLIST.md
7. 01_workflows/UPDATE_EXISTING_CELL_WORKFLOW.md
8. 02_design_guides/HAZARD_PATHWAY_SPLITTING.md
9. 04_validation_qc/REPORTABILITY_RULES.md
10. 00_governance/RELEASE_CHECKLIST.md
```

## Promotion path

This skill should start as `draft-operational`, then become canonical after two smoke tests:

```text
Test A - existing-cell docs/evidence update
  expected: docs revision bump only, no model version bump.

Test B - new-cell scaffold
  expected: new scaffold state, no false v1.0 release.
```

Both controlled workflow tests have now been exercised. Reviewer sign-off remains the final promotion gate; see `ROADMAP_AND_PROMOTION.md`.
