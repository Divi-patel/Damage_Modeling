# Skill changelog

The folder name remains stable: `damage_curve_skill/`.

Skill changes are tracked here rather than in the folder name. When uploaded to an OpenAI skill environment, the platform may assign skill versions; that upload version is separate from damage-library package versions.

## 2026-10-18 — Interpret test evidence before fitting economic response

- Focused `SKILL_REVISION`: the evidence-pressure-test guide now distinguishes
  test protocol, exposure, post-test treatment, intervention and repair endpoint.
- BESS application: extended final soaking confounds a short-soak damage anchor;
  early re-immersion censors thermal escalation; heterogeneous packs are not
  repeated trials of the target BESS.
- Hypothesis comparisons cannot become a mean by averaging or be labeled a
  confidence interval. Uses existing registers; no mandatory new folder sequence.
- No cell, runtime schema, model version, indexed artifact or consumer pin changed.

## 2026-10-18 — Bounded curation and actionable future research

- Owner-directed `SKILL_REVISION`: separate the agreed current deliverable from
  useful later refinements; retain source locators, current treatment, deferral
  reason, expected benefit, reopening trigger and acceptance check while researching.
- Clarifies practical evidence-based assumptions versus arbitrary midpoint estimates,
  optional refinements versus missing required proof, and initiating events versus
  downstream physical consequences.
- Routes new-cell and material re-curation work to one focused guide. Stable skill
  name and existing admission rules retained; no cell, model, cell-docs revision,
  schema, runtime value mapping, artifact, package release or consumer pin changed.
- Local authoring update only; no cloud upload or numerical release implied.

## Initial draft-operational build — 2026-07-07

Added:

```text
- OpenAI-compatible SKILL.md manifest.
- Governance decision tree and version-bump policy.
- Workflows for new cells, existing-cell updates, docs/evidence updates, schema changes, evidence ingestion, and release packaging.
- Design guides for failure units, x-axis, curve form, value crosswalk, selectors/conditioners/exposures, caps, and parameter tiers.
- Contracts for JSON curve artifacts, damage-code emit, capability declaration, field-name aliases, and machine-readable registries.
- Validation/QC guides for cap-binding, known-answer tests, reportability, and common failure modes.
- Templates, seed v2.5 cell registry, governance test cases, and helper scripts.
```

Status:

```text
draft-operational
```

Promotion requirement:

```text
Pass controlled tests on one docs/evidence-only update and one new-cell scaffold before treating this as canonical operating process.
```


## Skill change — first-reader onboarding and first controlled application support

- Added `FIRST_TIME_READER_GUIDE.md` to connect what the skill is, why it exists, how it should be used by a first-time reviewer, and how Codex/OpenAI agents should invoke it.
- Updated `SKILL.md` and `README.md` to point first-time users to the guide.
- This is still an evergreen skill: the folder name remains `damage_curve_skill/` and is not tied to any package release version.


## 0.2 — first-reader / Codex onboarding guide

- Added `FIRST_TIME_READER_GUIDE.md`.
- Updated `README.md`, `SKILL.md`, and `OPENAI_SKILL_USAGE.md` to point first-time users and Codex/agent workflows to the guide.
- No governance classification logic changed.


## 2026-07-07 — First-reader and Codex onboarding guides

- Added `START_HERE_FIRST_TIME_READER.md` to connect what the skill is, why it exists, and how to use it.
- Added `CODEX_SKILL_ONBOARDING.md` with placement and invocation examples.
- Updated `README.md`, `SKILL.md`, and `OPENAI_SKILL_USAGE.md` to point to the onboarding path.
- Used the skill in a first controlled real update: `hail_solar` docs r6 benchmark/value/damage crosswalk.

## 2026-07-07 — first-reader / Codex onboarding hardening

Added:

```text
FIRST_TIME_READER_GUIDE.md
CODEX_SKILL_ONBOARDING.md
```

Reason: make the skill self-explanatory to a first-time reader and easier to use as a Codex skill. This is a skill-process documentation update; it does not change damage-curve-library model behavior.


## First-reader / Codex guide update — 2026-07-07

Added:

```text
- START_HERE_FOR_FIRST_READER.md
- CODEX_SKILL_GUIDE.md
- README.md first-read order update
- SKILL.md pointer to first-reader guide
- OPENAI_SKILL_USAGE.md first-reader orientation note
```

Status:

```text
controlled-use
```

Rationale:

```text
The skill now contains an explicit bridge for someone who has no prior context: what this is, why it exists, how to use it with the latest library package, and what outputs to expect from a governed update.
```


## 0.3 — controlled application and Codex guide

- Added `CODEX_AGENT_GUIDE.md` for Codex/coding-agent use.
- Expanded `FIRST_TIME_READER_GUIDE.md` with the real v2.5.1 controlled-use example.
- Updated `ROADMAP_AND_PROMOTION.md` to record that Test A was applied to a real docs/evidence-only package update.
- Governance logic unchanged.


## 0.4 — two-mode repo/package workflow clarification

- Added explicit `inside_repo` versus `outside_package` mode language to `SKILL.md`, `README.md`,
  `FIRST_TIME_READER_GUIDE.md`, `START_HERE_FOR_FIRST_READER.md`, `CODEX_AGENT_GUIDE.md`,
  `CODEX_SKILL_ONBOARDING.md`, and `OPENAI_SKILL_USAGE.md`.
- Clarified that normal work inside `damage_modeling` edits canonical repo folders directly and does not need
  a ZIP round-trip.
- Clarified that ZIP/source-drop ingestion is for outside-package work that needs to be preserved, inventoried,
  compared, and promoted back into canonical repo folders.
- Governance logic unchanged.

## 0.5 — evidence rigor and fail-closed new-cell hardening — 2026-07-09

Added:

```text
- Hazard-neutral seven-step audit and evidence pressure-test checklist.
- Controlled wildfire_solar no-curve worked example.
- Source-register, claim/parameter-register, row-level value-crosswalk,
  legacy-ingestion, site-condition-adapter, and seven-step templates.
- Required exact locators, endpoint transfer limits, canonical parameter tiers,
  reproducible legacy equation/table checks, and explicit update triggers.
- Site-condition controls for fences, walls, barriers, bypass pathways,
  no-credit defaults, and exposure/vulnerability/value double-count prevention.
- No-curve known-answer tests and NO_RUNTIME_CURVE reportability checks.
- Rectangular CSV-register validation so missing or extra fields cannot silently shift provenance columns.
- Canonical input-field alignment across metadata, JSON, site adapters, and known-answer tests, with explicit alias and documentation-group rules.
- Bounded evidence-search logging for load-bearing negative-evidence claims, including cutoff, queries, endpoint tests, scope limits, and update triggers.
- Expanded NEW_CELL_SCAFFOLD gates and an executable governance self-test.
```

Changed:

```text
- Normalized capability statuses to supported | conditional | withheld, with
  conditions and withholding explanations carried as reason codes.
- Clarified that repository presence is not package/runtime promotion. Proposed
  artifacts use package_release=unreleased, package_baseline=<current release>,
  package_inclusion_status=not_included, and canonical_runtime_artifact=false.
- Kept model/document revisions atomic and moved scaffold, promotion, review,
  and documentation state into separate lifecycle/status fields.
- Marked controlled Test B complete using the wildfire_solar scaffold.
```

Version impact:

```yaml
skill_revision: 0.4 -> 0.5
damage_library_package_release: unchanged
cell_model_versions: unchanged
cell_documentation_revisions: unchanged_by_this_skill_update
schema_artifact_version: unchanged
runtime_outputs_can_change: false
cells_used_as_controlled_examples:
  - wildfire_solar
```

Status remains `controlled-use` until independent reviewer sign-off. The stable folder name remains `damage_curve_skill/`.

## 0.6 — governed multi-pathway cell rebuilds — 2026-07-11

Added:

```text
- A first-class pathway contract: stable pathway_id values are explicit runtime inputs and
  appear on pathway definitions, curve records, failure-unit outputs, capabilities, and KATs.
- A test for deciding when related mechanisms share one cell while retaining independently
  governed axes, bridges, evidence chains, numerical behavior, and support states.
- Partial-pathway fail-closed rules at pathway × failure-unit grain; an unsupported pair cannot
  borrow a curve from a neighboring pathway or silently default to a supported pathway.
- Required per-pathway old-vs-new comparisons, cross-pathway negative tests, consumer migration,
  exact model/docs/schema/SHA pin verification, and rollback/readiness checks.
- An explicit neighboring-cell boundary: tropical-cyclone/hurricane wind is not delivered by a
  straight-line-convective/tornado run unless separately classified, researched, and governed.
- A worked wind_tornado_wind model-v2.0 proposal example covering separate model-behavior and
  schema-contract change events without prematurely replacing the current v1.0 artifact.
```

Changed:

```text
- Tightened the artifact, damage-code, capability, KAT, workflow, review, and validation guidance
  so pathway is never represented by a boolean, selector, conditioner, inferred alias, or prose branch.
- Extended governance tests and bundle validation markers for multi-pathway rebuilds.
- Updated templates to expose pathway architecture and pathway-specific support without asserting
  that a skill-only revision has migrated the repository's live schemas.
```

Version impact:

```yaml
skill_revision: 0.5 -> 0.6
damage_library_package_release: unchanged_by_this_skill_update
cell_model_versions: unchanged_by_this_skill_update
cell_documentation_revisions: unchanged_by_this_skill_update
schema_artifact_version: unchanged_by_this_skill_update
runtime_outputs_can_change: false
controlled_example_cell: wind_tornado_wind
controlled_example_target: proposed model v2.0 / docs r1
```

The workflow requires a separate schema-contract change event when a live bundle/emit/capability schema adopts required pathway fields. Skill revision 0.6 does not perform that runtime migration by itself.

## 0.7 — illustrative asset intake and qualified reuse — 2026-10-15

- Added a conditional pre-cell intake guide and worksheet: idealistic twin provenance, scope reduction,
  category/profile/response separation, reuse qualification and the early Hazard–Damage interface.
- Routed the entrypoint, new-cell workflow, design-guide/template indexes and operator guide to it.
- Reused the existing shared-component substrate standard; no new runtime registry, loader or schema.
- Generalized value prompts to declared area, item, amount, share or capacity while preserving CSV columns.
- Reviewed warehouse, office, house, assembly overlap, non-runtime candidate and existing Solar/Wind cases.

Version impact: `SKILL_REVISION` 0.6 → 0.7 only. Package release, cell model versions, cell documentation
revisions, schemas, numerical artifacts and consumer pins are unchanged. Status remains controlled-use;
real building research and numerical admission still require the existing cell gates.

## 0.8 — reviewable reuse and annual-distribution clarity — 2026-10-16

- Exercised the intake on a pinned substation profile and an existing whole-assembly Flood response:
  numerical reproduction, applicability, value binding and metric admission are separate proofs.
- Added a compact progress table to the existing guide/worksheet, including owners and next evidence;
  retained source verification is distinguished from fresh retrieval and unresolved transfer claims.
- Require a concrete source-to-target/value comparison before asking about a consequential proxy.
- Corrected workflow/capability prose that conflated curve-intrinsic spread with annual loss variation.
  Deterministic DR can feed a stochastic annual hazard model; existing capability withholding still binds.
- Clarified that the illustrative capability guide does not migrate a released runtime schema.

Version impact: `SKILL_REVISION` 0.7 → 0.8 only. The associated Substation review is evidence/documentation
outside current cell packages. No cell model/docs revisions, numerical artifacts, runtime schema, package
release, registry or consumer pins change. Status remains controlled-use. This is local skill authoring,
not an upload/installation or admission of a standalone substation curve.
