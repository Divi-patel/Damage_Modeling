---
name: damage-curve-library-governance
description: Govern, extend, validate, and release the damage-curve library. Use for adding or updating hazard x asset damage cells; rebuilding multi-pathway cells with explicit pathway IDs, pathway-specific axes, evidence, curves, capabilities, and tests; pressure-testing evidence and legacy numbers; governing source/claim provenance, seven-step audits, site-condition adapters, value crosswalks, and fail-closed outcomes; classifying changes; deciding version bumps; enforcing machine-readable artifacts, consumer migrations, and cap-binding gates; handling source drops or in-repo edits; and packaging releases.
---

# Damage Curve Library Governance Skill

Use this skill when the user asks to add, update, review, validate, package, or version-bump the damage-curve library or any hazard × asset damage cell.

This is an evergreen operating skill. It is not tied to any one library package version. Before editing, decide
whether the task is running in `inside_repo` mode or `outside_package` mode:

```text
inside_repo
  edit the canonical damage_modeling repo folders directly; no ZIP round-trip.

outside_package
  use the latest package/folder as input, produce a governed package/ZIP, then ingest it through source_drops.
```

For first-time orientation, read `START_HERE_FOR_FIRST_READER.md` before the detailed workflow files. For the
two-mode operating guide, read `../guides/damage_curve_skill_usage_guide.md`.

For a new asset family or detailed illustrative twin, start with
[illustrative asset intake and reuse](02_design_guides/ILLUSTRATIVE_ASSET_INTAKE_AND_REUSE.md)
before naming cells or fitting curves. It connects idealistic anatomy to a scoped profile, qualified
reuse and the Hazard–Damage interface. Skip this intake for bounded updates whose scope is already settled.

When adding or materially re-curating a response, use
[bounded curation and future research](02_design_guides/BOUNDED_CURATION_AND_FUTURE_WORK.md):
agree the deliverable, choose the simplest justified baseline, and retain actionable
discoveries for later improvement in the existing dossier/register. A practical
baseline is not an arbitrary midpoint or permission to emit unsupported numbers.

## First-time orientation

For a human or agent opening this skill for the first time, read `FIRST_TIME_READER_GUIDE.md` after this file. It connects the dots on what the skill is, why it exists, and how it governs future package/version changes.

## First-time use

If the user is asking how to use or install the skill, or if the operator is unfamiliar with this project, read `FIRST_TIME_READER_GUIDE.md` before executing a workflow. For Codex or other coding-agent use, also read `CODEX_AGENT_GUIDE.md`.

## Required operating sequence

1. **Choose the operating mode.** If working inside `damage_modeling`, edit canonical repo folders directly. If working outside the repo, use the latest package/folder as task input and bring the output back through `docs/source_drops/`.
2. **Locate the current library state.** In `inside_repo` mode, read the relevant canonical files under `docs/cells/`, `docs/contracts/`, `docs/method/`, and `docs/evidence/`. In `outside_package` mode, read the latest package's `START_HERE.md`, `VERSION_REGISTRY.md`, `machine_readable_artifact_index.json`, and relevant current cell files before proposing edits.
3. **Classify the requested change before editing.** Use `00_governance/CHANGE_CLASSIFIER.md`. Do not assume that every update is a model change.
4. **Choose the workflow.** Use one of `01_workflows/`: add new cell, update existing cell, docs/evidence-only update, schema/contract change, release packaging, or evidence ingestion.
5. **Preserve separate version streams.** Package release version, cell damage-model version, cell docs revision, schema/artifact version, and skill upload version are different things.
6. **Never silently overwrite the current cell.** Archive prior current artifacts before replacing them, or create a clearly named proposed/draft folder.
7. **Run the seven-step audit.** Define the asset, decompose failure units, choose the y-axis/value basis, split value rows, allocate physical value, specify the site adapter, then apply qualified curves or withhold.
8. **Declare pathway architecture before fitting.** Keep one cell only when the asset/value substrate is shared and each mechanism can be independently governed. Require a stable `pathway_id`; never encode a pathway as a boolean, selector, conditioner, or undocumented branch. Give each pathway its own axis/bridge, evidence disposition, curve records, capabilities, and known-answer tests.
9. **Pressure-test evidence and legacy numbers.** Use a stable source register, claim-level provenance, exact locators, canonical tiers, reproducible equation/table checks, endpoint transfer limits, and explicit denominators.
10. **Keep the grain correct.** Damage cells contain pathway × failure-unit records. A whole-asset or source-native assembly response needs explicit applicability, included mechanisms and a repair denominator supported by its dossier. Preserve that source grain; do not reinterpret aggregate evidence as independent component curves or infer full-asset coverage from an assembly name.
11. **Govern site conditions causally.** Separate bridge inputs, derived exposure, vulnerability, and value allocation. Fences, walls, barriers, protection, maintenance, access, and response receive no blanket credit and cannot be double-counted.
12. **Maintain the M3 boundary.** The damage-code layer emits vulnerability/severity: failure-unit DRs and scenario loss views with explicit value basis. It does not own hazard frequency, EAL aggregation, insurance terms, BI, VaR, PML, or TVaR unless those are downstream objects consuming the emit.
13. **Use JSON as the runtime artifact.** Workbooks are derivation/audit views. Runtime M3 should pin to canonical JSON artifacts and an exact cell-model/docs/schema/SHA tuple.
14. **Enforce withhold-not-caveat.** If a requested pathway × failure-unit pair is unsupported, withhold that pair with a reason code; do not substitute a neighboring pathway. If `capability_declaration` says a metric is withheld or conditional and the gate is not satisfied, do not emit it with a caveat. A rigorous `NO_RUNTIME_CURVE` or partial-pathway outcome is acceptable.
15. **Run validation/QC before packaging or committing.** Use `04_validation_qc/` and `tools/validate_skill_bundle.py` or equivalent package validation logic. In `inside_repo` mode, also run repo link/hash/no-`src` checks when relevant.
16. **Write the release or change reason.** Every release or canonical repo change must say why the package/repo changed, which cells/pathways changed, which model versions changed, which docs revisions changed, whether schemas changed, what consumers must migrate, and what is explicitly not changed.

## Quick decision tree

```text
Is the work happening inside damage_modeling?
  yes -> inside_repo mode; edit canonical docs/cells/contracts/method/evidence directly.
  no  -> outside_package mode; output a governed package/ZIP and ingest through source_drops.

Does the change alter damage-code outputs for the same inputs?
  yes -> existing-cell model behavior change; bump cell model version.
  no  -> docs/evidence/package/schema triage.

Does it add a new hazard × asset pair?
  yes -> new-cell workflow; scaffold first unless runtime curve is derived and reviewable.

Does it alter JSON/emit/capability/schema required fields or meanings?
  yes -> schema/contract governance workflow.

Does it only improve proof trail, wording, evidence narrative, or reviewer clarity?
  yes -> docs/evidence workflow; do not bump cell model version.
```

## Files to read by task

- First-time human onboarding: `FIRST_TIME_READER_GUIDE.md` and `CODEX_SKILL_ONBOARDING.md`.
- First-time reader: `START_HERE_FOR_FIRST_READER.md`, then this `SKILL.md`.
- Start every task: `00_governance/CHANGE_CLASSIFIER.md`, `00_governance/VERSIONING_POLICY.md`, `00_governance/RELEASE_DECISION_TREE.md`.
- New cell: `01_workflows/ADD_NEW_CELL_WORKFLOW.md`, then `02_design_guides/EVIDENCE_PRESSURE_TEST_AND_FAIL_CLOSED_CHECKLIST.md` and the remaining `02_design_guides/`.
- Existing cell update: `01_workflows/UPDATE_EXISTING_CELL_WORKFLOW.md`; for a multi-pathway rebuild also read `02_design_guides/HAZARD_PATHWAY_SPLITTING.md` and `06_examples/EXAMPLE_MULTI_PATHWAY_REVAMP_WIND_TORNADO_WIND.md`.
- Evidence-only update: `01_workflows/DOCS_EVIDENCE_ONLY_WORKFLOW.md`, `01_workflows/EVIDENCE_INGESTION_WORKFLOW.md`.
- Runtime/schema work: `03_contracts/` and `01_workflows/SCHEMA_CONTRACT_CHANGE_WORKFLOW.md`.
- Validation/reportability: `04_validation_qc/`.
- Release packaging: `05_release/`.

## Non-negotiables

- Model version changes only when behavior changes.
- Docs revision changes when explanation/proof trail changes.
- New cells do not become v1.0 until they have a reviewed runtime curve artifact and capability declaration.
- Tail metrics remain withheld unless an annual loss distribution or equivalent tail-supporting object exists.
- Cap-binding preflight is fail-closed for scalar EAL when caps can bind.
- Record every material assumption, default, alias, open seam, and update trigger.
- Every new cell completes the seven-step audit, source/claim registers, row-level value crosswalk, and evidence pressure test; add legacy and site-condition controls when applicable.
- A load-bearing “no evidence located” decision carries a bounded, reproducible search log and never becomes a universal absence claim.
- Guidance or a plausible mechanism does not become a numeric modifier without calibration at the intended endpoint and grain.
- `pathway_id` is a required first-class runtime dimension for multi-pathway cells. It is not a selector, conditioner, boolean variant, or inferred alias, and each curve record/output/test must carry it.
- A shared cell does not imply shared numerical behavior: qualify support and fail closed at pathway × failure-unit grain. Keep neighboring mechanisms such as tropical-cyclone wind in a separately governed cell unless the pathway-splitting test proves otherwise.
- A required pathway contract or meaning change follows the schema-contract workflow, including a consumer migration, exact pin verification, and dual-read/rollback rule when needed.
- Repository presence does not promote a proposed artifact into the released package or runtime.
