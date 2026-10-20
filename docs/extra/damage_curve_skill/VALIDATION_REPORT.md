# Curation guidance verification — 2026-10-18

## 2026-10-18 — BESS test-evidence interpretation update

This local `SKILL_REVISION` adds post-test treatment, intervention censoring and
repair-endpoint checks to the existing evidence guide. It changes no numerical
cell, runtime schema, indexed artifact or consumer pin.

Executed against this working tree:

- Bundle validator: PASS, 106 files. Governance self-tests: PASS, 8 cases.
- Installed skill-creator quick validation: valid skill.
- BESS candidate audit: 52 known-answer checks; independent temporary-directory
  rerun byte-identical across three CSVs, JSON receipt and PNG figure.
- Deliberately modified temporary reference: rejected before writing outputs.
- Eight original PDF hashes verified; source/claim/parameter IDs and rectangular
  CSVs checked. Existing source curve, evaluator, runtime index and Pluvial code
  retain their prior audit hashes.

Scientific limit: these checks validate audit behavior and documentation
integrity, not the unqualified BESS repair hypotheses. Neither a battery curve
nor the PCS target binding has been admitted. See the BESS candidate review in
`docs/extra/discussion/bess_damage/03_flood_candidate_pressure_test.md`.


**Scope:** owner-directed `SKILL_REVISION`; local authoring only. Added bounded
curation and actionable future-research guidance, linked from the entrypoint,
new-cell workflow and design-guide index. Existing cell artifacts, curve parameters,
capabilities, runtime schemas and consumer pins were not edited by this change.

- Bundle structural validation: PASS, 106 files.
- Existing governance classifier self-tests: PASS, 8 cases.
- Reviewed the new guide's three examples against the current admission rules:
  usable assembly with optional refinement; propagation evidence without annual
  rate; supported transformer with unsupported battery coverage. All retain the
  difference between current admissibility and future improvement.
- This is same-author scenario review, not an independent behavioral test or a
  demonstrated BESS numerical model. Existing unrelated local work is preserved.
- The [manifest](MANIFEST.md) is regenerated for the current local bundle; it does not
  publish that bundle or change its numerical release status.

Historical verification follows unchanged.

---

# Validation report — damage_curve_skill revision 0.8

**Date:** 2026-10-16 · **Status:** PASS · **Skill status:** controlled-use

## Change and version decision

`inside_repo`, `SKILL_REVISION` 0.7 → 0.8. Adds reviewable reuse progress and source-access distinctions;
corrects the curve-spread versus annual-distribution explanation. The associated Substation research
lives outside current cells. No cell model/docs, runtime schema, canonical artifact, package release or
consumer pin changes. This is local authoring, not an uploaded skill or approved numerical release.

## Executed checks

| Check | Result | Meaning |
|---|---|---|
| `tools/validate_skill_bundle.py docs/extra/damage_curve_skill` | PASS, 105 files | Existing bundle/parse/compile/template controls |
| `tools/run_self_tests.py` | PASS, 8 cases | Existing classifier/version/gate behavior retained |
| Installed skill-creator `scripts/quick_validate.py` | Skill is valid | Frontmatter/basic skill validity |
| Substation reuse review | PASS, 93 cases, bad SHA rejected, 31 value rows | Exact existing response reproduced; all cost rows accounted |
| Independent output-directory rerun | Byte-identical JSON and CSV | Deterministic review outputs |
| Scoped Markdown review | PASS, 20 files / 103 local links; 8 new files' stamps and all fences checked | Navigation and document integrity |
| Skill manifest regeneration/verification | PASS, all non-manifest files | Exact size/hash inventory; manifest excludes itself |

## Concrete application and limits

The [Substation review](../discussion/substation_damage/01_assembly_reuse_review.md) exercises the intake
against a real existing source assembly and pinned Hazard reference. Its
[receipt](../discussion/substation_damage/verification/review_receipt.json) separates numerical pass from
unresolved geometry, denominator and annual-use qualifications. Manual walkthroughs checked that:

- +0.3 m floor height and +1 m transformer-control cabinet are not proof of the source's +3 ft switchgear assumption;
- filtering a whole-assembly budget does not establish a compatible denominator;
- stale reference-helper proposal metadata does not change current canonical authority;
- a deterministic DR can feed annual hazard variation while an explicit annual-use prohibition still binds;
- failed fresh retrieval preserves inherited evidence but cannot qualify new transfer claims;
- the owner's request for explanation is not proxy acceptance.

These are direct review checks, not independent-agent validation, claims calibration, component-curve
research or runtime admission. The eight automated skill cases validate classification, not research
judgment. No numerical cell files or runtime contracts changed.

## Historical validation — revision 0.7

The following report records the earlier checkpoint and its then-current checks.

### Revision 0.7 report

**Date:** 2026-10-15 · **Status:** PASS · **Skill status:** controlled-use

## Change and version decision

This is an `inside_repo`, process-only `SKILL_REVISION` 0.6 → 0.7. The linked Real Estate discussion/plan
work is `DOCS_ONLY`. Package release, cell model/docs revisions, runtime schemas, numerical artifacts,
consumer pins and outputs are unchanged. No cell or shared-response runtime admission occurs here.

The skill adds conditional illustrative-asset intake, a worksheet, explicit reuse qualification and
asset-appropriate value prompts. It also clarifies source-native assembly grain without making a whole
asset the default response. Existing CSV columns are preserved.

## Automated checks

Executed from `damage_modeling` using its `.venv/bin/python`:

| Check | Result | What it establishes |
|---|---|---|
| `tools/validate_skill_bundle.py docs/extra/damage_curve_skill` | PASS, 105 files | Bundle structure, parse/compile checks, existing CSV/template/governance controls |
| `tools/run_self_tests.py` | PASS, 8 cases | Existing change-classification/version/gate behavior retained |
| Installed skill-creator `scripts/quick_validate.py docs/extra/damage_curve_skill` | Skill is valid | Frontmatter/name/basic skill validity |
| Documentation scan across the two workstreams | 22 files, 103 local links, 7 new documents' metadata/fences checked | Local destinations and required stamps present; not scientific correctness |
| SHA-256 before/after scan | 1,835 files unchanged | Hazard `drivers/`, `perils/`, `shared/` and Damage `docs/cells/`, `docs/contracts/`, `scripts/reference_helpers/` retain inspected bytes; bytecode excluded |
| `git diff --check` in both repositories | PASS | No whitespace errors in tracked diffs |
| Skill manifest regeneration and hash readback | PASS | Every skill file except the self-excluded manifest has a matching size/hash |

The eight automated governance cases are existing tests. They do not simulate research behavior or prove
building response support. No numerical suite was rerun because no runtime, contract or cell files changed.

## Manual scenario walkthrough

Reviewed the new instructions against concrete cases, with the results below. This was a direct review,
not an independent-agent test or a completed cell-research application.

| Case | Result of applying the instructions |
|---|---|
| Warehouse/office compatible roof, differing area | Candidate intrinsic reuse; separate local exposure/value and other building responses |
| Same cover, different deck/attachments or wind basis | Numeric reuse remains unqualified; evidence/vocabulary may still transfer |
| House illustration includes loss-of-use insurance value | That value cannot enter the building-only physical repair denominator |
| Three-story office selected but input twin is retail | Missing office facts remain a research task; no relabeling of retail defaults |
| Whole-building flood assembly plus included interior components | Keep source grain and representation exclusivity; no duplicate loss |
| Shared candidate has equal numbers but is non-runtime | No shared runtime load or implied promotion; cell-local adoption remains governed |
| Existing Solar/Wind scope and capacity units already settled | Skip redundant new-asset intake; retain established units, artifacts and gates |

The [Real Estate flow review](../discussion/real_estate_conus/02_flow_and_reuse_review.md) records the
implementation evidence and research dispositions. Next validation is actual bounded building research,
followed by cell KATs and the integrated Hazard proof once a response and interface are qualified.

## Historical record

The following revision-0.6 report is retained as history; its commands and current-version statements
refer to that earlier checkpoint.

## Historical validation — revision 0.6

**Date:** 2026-07-11

**Status:** PASS
**Skill status:** controlled-use

## Change and version decision

```yaml
operating_mode: inside_repo
change_scope: evergreen_skill_process_only
skill_revision: 0.5 -> 0.6
damage_library_change_class: not_applicable_by_skill_change_alone
damage_library_package_release: unchanged
cell_model_versions: unchanged
cell_documentation_revisions: unchanged_by_this_skill_update
schema_artifact_version: unchanged_by_this_skill_update
runtime_outputs_can_change: false
controlled_example_cell: wind_tornado_wind
controlled_example_target: proposed model v2.0 / docs r1
```

Revision 0.6 codifies a reusable multi-pathway cell-rebuild workflow. It does not modify or promote a live cell, schema, package, artifact index, or consumer pin. A real `wind_tornado_wind` rebuild must record separate `MODEL_BEHAVIOR_CHANGE` and `SCHEMA_CONTRACT_CHANGE` events and keep the current v1.0 runtime pinned until the proposed v2.0 package and Hazard migration fixture pass.

## Checks

| Check | Result |
|---|---|
| OpenAI skill quick validator | PASS |
| Bundle structure, exactly one `SKILL.md`, JSON parse, and Python compile | PASS — 103 files |
| Required rigorous and multi-pathway guide/example/template presence | PASS |
| Source, claim, value, and parameter CSV template headers | PASS — pathway fields required |
| CSV template row widths / rectangularity | PASS |
| Atomic model/lifecycle/promotion/review/documentation/package fields | PASS |
| First-class pathway contract markers | PASS |
| Pathway-specific axis/evidence/record/capability/KAT guidance | PASS |
| Partial-pathway fail-closed and neighboring hurricane boundary | PASS |
| Consumer migration and exact model/docs/schema/SHA pin checks | PASS |
| Governance classifier self-tests | PASS — 8 cases |
| Multi-pathway behavior-change gate subset test | PASS |
| Required-pathway schema-change gate subset test | PASS |
| `agents/openai.yaml` name/default-prompt alignment | PASS |
| JSON syntax for templates, capability registry, and governance tests | PASS |
| Git whitespace/error check for the skill diff | PASS |
| Accidental `src/` directory check | PASS — absent |
| Manifest inventory and SHA256 verification | PASS — self-entry intentionally excluded |

## Bundle validation output

```json
{
  "status": "PASS",
  "file_count": 103
}
```

The validator checks the pathway-aware exact headers for:

```text
TEMPLATE_SOURCE_REGISTER.csv              -> pathway_ids
TEMPLATE_CLAIM_PARAMETER_REGISTER.csv     -> pathway_id
TEMPLATE_VALUE_CROSSWALK.csv              -> applicable_pathway_ids
TEMPLATE_PARAMETER_TIER_TABLE.csv         -> pathway_id
```

It also requires the curve template to expose `pathways`, `hazard_axes_by_pathway`, and `pathway_unit_support`, and requires the splitting guide to contain first-class identity, one-cell/separate-cell, partial fail-closed, hurricane-boundary, and consumer markers.

## Governance self-test output

```json
{
  "status": "PASS",
  "cases": 8
}
```

The added cases verify:

```text
wind_tornado_wind_multi_pathway_model_revamp
  -> MODEL_BEHAVIOR_CHANGE, major model bump, pathway architecture/evidence/support/KAT,
     cross-pathway negative, neighboring-cell, and consumer migration/pin gates.

required_pathway_id_schema_contract
  -> SCHEMA_CONTRACT_CHANGE, schema bump, compatibility/migration/schema validation,
     pathway support, negative-test, neighboring-cell, and consumer migration/pin gates.
```

## Contract decisions validated

```text
- pathway_id is explicit and required for a multi-pathway runtime request;
- pathway identity is not a boolean, selector, conditioner, exposure, alias, or intensity inference;
- each pathway owns its axis/bridge, evidence disposition, curve records, support matrix, and KATs;
- unsupported pathway × failure-unit pairs emit no number and use a stable reason code;
- straight_line_convective and tornado_direct_hit may share one wind-turbine substrate;
- tropical_cyclone_wind remains a separately governed neighboring cell/workstream;
- current artifacts stay canonical during research; consumer cutover requires an exact
  cell-model/docs/schema/SHA pin, integration fixture, and rollback rule.
```

## Commands

```bash
PYTHONPATH="$TMPDIR/damage-skill-quick-validate-deps" /usr/bin/python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" docs/extra/damage_curve_skill
python3 docs/extra/damage_curve_skill/tools/validate_skill_bundle.py docs/extra/damage_curve_skill
python3 docs/extra/damage_curve_skill/tools/run_self_tests.py
python3 -m json.tool docs/extra/damage_curve_skill/templates/TEMPLATE_CURVE_ARTIFACT.json
python3 -m json.tool docs/extra/damage_curve_skill/templates/TEMPLATE_CAPABILITY_DECLARATION.json
python3 -m json.tool docs/extra/damage_curve_skill/registries/CAPABILITY_DECLARATION_REQUIRED_FIELDS.json
python3 -m json.tool docs/extra/damage_curve_skill/tests/governance_test_cases.json
git diff --check -- docs/extra/damage_curve_skill
```

The quick validator required PyYAML, which was installed only into a temporary `$TMPDIR` validation target because the default Python environment did not provide it. No repository dependency was added.

`MANIFEST.md` omits its own row because a file cannot carry a stable SHA256 of itself. Every other skill file, including this report, is inventoried and hash-verified.
