---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: done
scope: Repository-only BESS Flood v1.0 release manifest and changed-file record
---

# Repository release: model v1.0 / docs r1

Classification: `NEW_CELL_MODEL_RELEASE`. The conditional response/value arrays
are identical to local v0.2. Annual capability now permits a validated consumer
under explicit common-event, unit-cap and coverage requirements. The cell is
repository canonical; portable library v2.5 is unchanged and no ZIP is produced.

## Changed files and roles

| Files | Purpose |
|---|---|
| `current/curve_artifact.json`, `capability.json`, `value_binding.json`, `consumption_pin.json` | New canonical tuple, conditional annual requirements and exact runtime hashes |
| `current/known_answers.json`, `value_crosswalk.csv` | Unchanged numerical examples and same-budget partition |
| `current/README.md`, `derivation.md`, `metadata.md` | Scope, seven-step audit, source/claim references and consumer rules |
| `current/validation.json`, `RELEASE.md`, `MANIFEST.json` | Validation result, changed-file record, payload manifest |
| Cell `README.md`, `basics/`, `VERSION_REGISTRY.md`, `CHANGELOG.json` | Current-reader navigation and release history |
| `docs/contracts/machine_readable_artifact_index.json` | Adds exactly one BESS tuple; other rows unchanged |
| `scripts/reference_helpers/validate_bess_flood_release.py` | Schema, pin, source/claim, index, predecessor and value checks |
| BESS plan, decisions and research README | Current checkpoint and BD-D10 annual qualification |

## Validation and migration

[Validation](validation.json) records the 29 annual cases, independent numerical
replay and known inherited Hazard integration failure. The schema/contract
validator passes. This is same-author review using independent numerical
methods; no external peer review is claimed.

Old local v0.1/v0.2 files remain byte-identical. Existing Solar/Wind/Substation
artifacts, schemas and portable packages are unchanged. Consumers must choose
the new exact v1.0 pin; tests reject v0.2 for annual use. There is no dual-read
annual fallback. Rollback returns to local conditional testing and withholds
annual use, as described in the [current overview](README.md).

The [manifest](MANIFEST.json) hashes this directory's payloads except itself.
The consumption pin remains the authority for runtime JSON. No cloud or national
publication, dashboard selection or complete-property claim accompanies this
repository release. Coastal severity includes the existing hurricane-origin
surge catalog only; wind and autonomous battery events are outside this cell.
