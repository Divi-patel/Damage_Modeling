---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Owner-selected BESS wind local-test package v0.1; not canonical
---

# BESS Hurricane local candidate v0.1

The owner selected **full integrated replacement after major compromise**, with
repair retained as a sensitivity, on 2026-10-19 (BW-Q01). Conditional scalar
calculations are verified; Hazard source/reference coupling and annual use are
not yet qualified. This package is unreleased and absent from the current index.

| Surface | Inspect |
|---|---|
| Exact proposed curves / capability | [curve_artifact.json](curve_artifact.json), [capability.json](capability.json) |
| Reconciled value | [value_binding.json](value_binding.json), [ten-row crosswalk](value_crosswalk.csv) |
| Provenance / parameters | [sources](source_register.csv), [claims](claim_parameter_register.csv), [parameters](parameter_register.csv) |
| Reasoning / input rules | [derivation](derivation.md), [metadata](metadata.md) |
| Numerical proof / identity | [known answers](known_answers.json), [validation](validation.json), [exact hashes](consumption_pin.json) |
| Explicit local reader | [evaluate_local.py](evaluate_local.py); opt-in required |

Two enclosure records represent approved replacement and repair sensitivity;
one PCS record is an explicit related-electrical-equipment T4 proxy. Both
response hypotheses use the same source probability parameters. Three
resistance scenarios are unweighted alternatives, not uncertainty percentiles.

Source/claim CSVs are frozen proposal views of the linked research registers;
they are not a second evolving evidence authority. CSVs replace a workbook for
this small proposed package. JSON owns its numerical parameters and exact pins.
No `current/` folder or runtime-index row is created.

Build/validate from Damage root:

```bash
.venv/bin/python docs/extra/discussion/bess_damage/evidence/hurricane/r2/build_local_candidate.py
```

The builder exercises schema, independent-research parity, typed unavailable
states, opt-in, exact pins and tampered payloads. It is a proposal-authoring and
audit utility, never a Hazard production dependency. The previous
[research comparison](../../../../extra/discussion/bess_damage/07_hurricane_enclosure_candidate.md)
contains actual examples, the owner ruling and future work.
