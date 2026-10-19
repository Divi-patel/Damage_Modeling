---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-18
updated: 2026-10-18
status: active
scope: Canonical conditional BESS response and annual-consumer requirements
---

# Flood × BESS: partial-property screening v1.0

The selected outdoor LFP reference now has a canonical conditional response
for active enclosure hardware and separate PCS. This promotes the tested v0.2
responses **without changing their numbers**. It permits Hazard to construct
annual screening metrics when the frequency, coupling, cap and missing-data
requirements in [capability.json](capability.json) pass. It does not assert
claims calibration, complete property coverage or a national result.

| Condition | Active enclosure hardware | Separate PCS |
|---|---|---|
| Freshwater | Replacement strictly above assumed 0.30 m entry | Original nine-knot inverter proxy after one entry subtraction; terminal replacement plateau |
| Saline | Replacement strictly above assumed 0.30 m entry | Same strict-entry replacement rule |
| Missing depth or unqualified condition | Withheld | Withheld |

The reference remains 100 MW / 400 MWh usable AC, 450 MWh installed DC, with
80 enclosures and 20 separate PCS. Covered value is **$82,510,403.40** within
**$109.8M** total property; **$27,289,596.60 remains unmodeled**. Costs use the
fixed real-2024 reference, not a current project quote.

Read [derivation](derivation.md), [input and output rules](metadata.md),
[values](value_binding.json), [known answers](known_answers.json),
[validation](validation.json) and [pins](consumption_pin.json). The
[Hazard proof](../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/07_annual_flood_proof.md)
contains annual examples and source limits.

Only one direct-inundation pathway is modeled. Other physical pathways,
autonomous failures, collector station/export, business interruption and the
unresolved property groups are not silently represented by these records.
No intrinsic spread or numerical IP/UL credit is invented.

## Promotion and rollback

Classification: `NEW_CELL_MODEL_RELEASE`, repository canonical model v1.0 /
docs r1, artifact and capability v2. Existing global schemas and every other
cell are unchanged. The existing CSV/JSON audit views serve as the small cell's
workbook; no fitted response requires a duplicate spreadsheet.

The prior v0.1/v0.2 proposals remain immutable, local-only and unindexed.
Annual consumers must pin the new canonical tuple and pass the declared gates.
Rollback means returning to local conditional testing, not using the old
local-only artifact as a silent annual fallback. No portable ZIP, cloud
publication, national BESS map or recipient selection is part of this release.

The [release record](RELEASE.md) lists changed files, validation, migration and
rollback; [MANIFEST.json](MANIFEST.json) hashes the repository payloads.
