---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Owner-selected local Wildfire BESS conditional candidate v0.1; not canonical
---

# BESS Wildfire local candidate v0.1

BWF-Q01: **“Test full replacement; retain repair sensitivities (Recommended)”**,
owner, 2026-10-19. This selects the consequence of battery compromise for local
tests, not the class-response calibration, annual risk or national delivery.

The proposed categorical enclosure response uses a new explicit T4 transfer of
existing electrical ordinal mean-response weights. An alternate heavy-equipment
shape and two serviceable-hardware repair hypotheses remain separate unweighted
sensitivities. The separate PCS uses a related electrical proxy. These are not
measured BESS fragilities, ignition probabilities or confidence bounds.

| Inspect | File |
|---|---|
| Reasoning and seven-step/site audit | [derivation](derivation.md) |
| Required inputs, no numeric fallback | [metadata](metadata.md) |
| Curve/capability and exact pins | [artifact](curve_artifact.json), [capability](capability.json), [pin](consumption_pin.json) |
| Same-unit value and complete row reconciliation | [values](value_binding.json), [crosswalk](value_crosswalk.csv) |
| Sources, claims, parameter assumptions | [sources](source_register.csv), [claims](claim_parameter_register.csv), [parameters](parameter_register.csv) |
| Independent numerical checks | [known answers](known_answers.json), [comparisons](conditional_comparisons.csv), [validation](validation.json) |
| Explicit local audit reader | [evaluate_local.py](evaluate_local.py); not a production import |

Proposed model v0.1/docs r1 is noncanonical, unreleased and not in the runtime
index. Existing bundle/capability v3 schemas are unchanged. Candidate hardware
is $94.4M of $109.8M full TIV; remaining $15.4M is unbound, not assigned zero.
Annual metrics, source coupling and full-property claims remain unqualified.

Rebuild/validate from Damage root:

```bash
.venv/bin/python docs/extra/discussion/bess_damage/evidence/wildfire/r2/build_local_candidate.py
```

The source/claim CSVs are frozen proposal views of the authoritative research
registers. CSVs replace a workbook for this small proposal; they are not runtime
inputs. Hazard production consumes exact numerical JSON through its own peril
API, never this authoring/audit helper. The source/shape sensitivities are not
combined into an inferred damage distribution.
