# templates

Copy these when creating or updating cells. Templates are intentionally strict so the output stays machine-checkable.

For new-asset scoping, use [TEMPLATE_ASSET_INTAKE_AND_REUSE.md](TEMPLATE_ASSET_INTAKE_AND_REUSE.md)
in the existing discussion or dossier before choosing cell identity. It is a research worksheet, not a
runtime schema or a required repeat step for every existing-cell change.

For a new or deeply re-researched cell, use this minimum set:

```text
TEMPLATE_NEW_CELL_README.md
TEMPLATE_CELL_DERIVATION_DOSSIER.md
TEMPLATE_CELL_METADATA_SPEC.md
TEMPLATE_CURVE_ARTIFACT.json
TEMPLATE_CAPABILITY_DECLARATION.json
TEMPLATE_SOURCE_REGISTER.csv
TEMPLATE_BOUNDED_EVIDENCE_SEARCH_LOG.md    when a negative-evidence claim is load-bearing
TEMPLATE_CLAIM_PARAMETER_REGISTER.csv
TEMPLATE_PARAMETER_TIER_TABLE.csv
TEMPLATE_VALUE_CROSSWALK.csv
TEMPLATE_LEGACY_EVIDENCE_INGESTION.md       when legacy material exists
TEMPLATE_SITE_CONDITION_ADAPTER.md          when site conditions matter
TEMPLATE_SEVEN_STEP_AUDIT.md
TEMPLATE_VALIDATION_REPORT.md
```

The templates do not require a numerical curve. A no-curve scaffold keeps `curve_records: []` and uses `NO_RUNTIME_CURVE` consistently.

For multi-pathway cells, preserve the `pathway_id`, `pathway_ids`, and `applicable_pathway_ids` fields/columns. Use `all_shared` only for genuinely shared asset/value facts. The curve/capability templates use placeholder schema labels because adopting required pathway fields in live artifacts is a separately governed schema-contract change; replace those labels only after that migration is classified and approved.
