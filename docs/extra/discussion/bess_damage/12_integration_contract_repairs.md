---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: settled
scope: Validator, current-pin metadata and guide/test inventory repairs; no numerical model, schema or artifact-pin change
---

# Current-contract maintenance after BESS Wildfire admission

**The inherited runtime-validator failure is resolved.** The owner authorized
this repair before the next Wildfire placement canary. The subsequent broad
suite also exposed stale publisher expectations and missing current request
guides; those were classified as inventory/documentation drift and repaired
without changing Damage responses.

## Disposition

| Finding | Resolution | What remains enforced |
|---|---|---|
| Flood BESS uses `NO_INTRINSIC_DAMAGE_SPREAD`; the v2 validator demanded only `CURVE_INTRINSIC_SPREAD_NOT_CARRIED` | Recognize those two exact existing spellings; also explicitly require `curve_intrinsic_spread=not_carried` and the existing annual uncertainty limitation | Flag alone cannot override contradictory/withheld capability. Missing and lookalike flags reject. No input mutation or schema change. |
| Hurricane BESS changelog lacks the current pin already present in the index | Add `tropical_cyclone_wind_bess@model_v1_0__docs_r1`; update the historical authoring helper to produce/check that field | Runtime index and every curve/value/capability payload stay byte-identical. This repairs routing metadata, not a new model/docs release. |
| Publisher tests assume eight cells and five KAT attachments | Use current-index cell/KAT membership and exact artifact/KAT hashes as the independent contract oracle | Every current cell must plan cleanly; missing/extra cells or KAT files and wrong hashes still fail. |
| Four current cells have no request-guide entry | Add concise exact-pin guides for `flood_substation`, `flood_bess`, `tropical_cyclone_wind_bess`, `wildfire_bess`; index them and retain explicit completeness checks | Guides link canonical axis, same-unit value, known answers, fail-closed behavior and annual-use boundaries; they do not author curves. |

Classification is repository validation/routing maintenance plus documentation
completion. No damage-code curve form, parameter, selector, exposure logic,
value mapping, output meaning or consumer pin changes. No library/schema/model
version bump or canonical artifact repinning is warranted. No portable package
or scientific publication is issued. Existing proposals and receipts remain
historical evidence, including the original failing-validator receipt.

## Verification

[Shared repair receipt](evidence/integration_repairs/checks.json) records:

- **19 Damage tests pass**, including both accepted flags, rejection controls,
  changelog mismatch refusal, all thirteen current request-guide pins/links,
  publisher file plans and the existing executable Hurricane request example.
- `validate_runtime_contracts.py` passes **13 indexed artifacts** and its original
  Hail/Wildfire known answers; seven v3 artifacts carry 28 curve records.
- The BESS Hurricane and Wildfire release validators pass existing schemas,
  exact prior/current response/value parity and consumption pins.
- Every tracked cell file is unchanged except the one changelog. The canonical
  artifact index and all curve/value/capability JSONs remain unchanged.
- Hazard closes its public-API gate with **325 passing tests**; a 45-row station
  rebuild, all 13,085 overlap decisions, source slices and Total controls retain
  exact numerical identity. Five original national Parquet pins still verify.

[Hazard's repair record](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/21_integration_repairs.md)
owns its code/wheel and before/after witnesses. The repaired validator reads
current artifacts; it never rewrites them to make a check pass. Existing cell
model/documentation pins and scientific payloads remain the same.

## Publication boundary and next step

The [guide index](../../guides/README.md) is now complete for all current cells.
The next science task is Hazard's Wildfire placement canary. No numerical
recalculation of published national results follows from this maintenance.

Offline file plans do not establish registry/publication readiness. The Damage
publisher's `_tech_class` currently supports Solar/Wind only and rejects BESS
and Substation. Hazard BR-28 retains asset-class/registry mapping qualification
for the later formal delivery checkpoint; no guessed mapping, provider upload
or database write is introduced here. The current Hazard BESS consumer uses
its installed, exact-pin Damage payloads independently of that future path.
