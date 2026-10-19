# Validation report — damage_curve_skill revision 0.6

## 2026-10-18 — BESS test-evidence interpretation update

This local `SKILL_REVISION` adds post-test treatment, intervention censoring and
repair-endpoint checks to the existing evidence guide. It changes no numerical
cell, runtime schema, indexed artifact or consumer pin.

Executed against the working tree, including pre-existing local skill authoring:

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
