---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: BESS direct-inundation local candidate v0.2; not a canonical or annual release
---

# Flood BESS local candidate v0.2

BF-Q02 authorizes **replacement after saltwater entry** for local testing.
Freshwater retains every v0.1 supported response and continues the existing
replacement ceiling beyond the former 2.3 m test limit. The selected 0.30 m
entry and replacement policies remain explicit T4 engineering assumptions.

| Condition | Active enclosure hardware | Separate PCS |
|---|---|---|
| Freshwater | Binary replacement after entry | Original nine-knot FS_INV proxy; constant DR=1 after final knot |
| Saline | Binary replacement after entry | Binary replacement after entry |
| Unknown condition, missing/invalid depth or unsupported property | Withheld | Withheld |

For both binary responses, `d <= 0.30 m` gives zero for this direct-entry
pathway; `d > 0.30 m` gives DR=1. At 0.45 m one PCS costs $390,000 under the
freshwater proxy and $520,000 under the saline policy. At deeper water, costs
remain capped at the same hardware value. This is not a calibrated mean,
complete-plant bound or observed salinity response.

The denominator is unchanged: $72.1104M active enclosure hardware + $10.4M PCS;
$27.2896M remains explicitly unmodeled within the $109.8M reference. No new
component allocation, height credit, IP rating, labor surcharge, autonomous
failure frequency, wave/scour or inter-enclosure escalation is added.

Read [derivation](derivation.md), [metadata](metadata.md), [known answers](known_answers.json),
[values](value_binding.json) and [exact consumption pins](consumption_pin.json).
The [capability declaration](capability.json) still withholds ordinary runtime
and annual metrics. Only explicitly opted-in local tests may use this artifact.

## Change and migration

- Classification: `MODEL_BEHAVIOR_CHANGE`; local model v0.1 → v0.2, docs r1.
- Bundle/capability schemas remain v2; value binding remains local schema v1.
  Model-specific evaluation metadata identifies the local adapter contract v2.
  No global required field or emit semantics changes.
- One direct-inundation pathway. Fresh/saline water is an event conditioner,
  not a substitute for wave impact, scour or another physical pathway.
- The v0.1 folder/pin remains intact for reproducibility. The Hazard consumer
  loads either exact model with its matching policy ID; it never falls back.
- Current local configs select v0.2. Historical v0.1 proofs use the saved
  `verification/local_flood_inputs_v0_1.json` via `--config`. Rollback selects
  that exact configuration rather than replacing any old artifact bytes.
- Package remains unreleased/not included; canonical index and other cells
  are unchanged. Candidate upgrade is not a national or annual-use promotion.

From Damage: `.venv/bin/python scripts/reference_helpers/validate_bess_flood_candidate.py --version 0_2`.
JSON/CSV views serve as the small candidate's audit workbook; no duplicate XLSX
is required. Production evaluation and source coupling remain in Hazard code.

## Completed consumer proof

The [Coastal and freshwater proof](../../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/06_coastal_local_proof.md)
records 31,000 native Coastal checks, unchanged prior freshwater answers and
876 newly supported deep-water cases. Both candidate validators and 28 targeted
Hazard tests pass. [Validation](validation.json) records local scope; these checks
are not an independent scientific review or annual-use admission.
