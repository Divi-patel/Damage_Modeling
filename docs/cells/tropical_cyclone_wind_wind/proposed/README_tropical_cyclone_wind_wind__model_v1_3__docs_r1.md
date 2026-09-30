---
author: "owner-directed (Divy) · agent-drafted"
created: 2026-09-30
updated: 2026-09-30
status: active
---

# Hurricane Wind: physical tower-value binding

DD-G31 accepts retaining the Jaimes 3.3 MW / 100 m response as a screening proxy for the
canonical 5 MW / 100 m turbine, with the tower budget updated to the source-derived physical value.
This is a **MODEL_BEHAVIOR_CHANGE**, model v1.3/docs r1, because the admitted loss denominator changes.
The bundle-v3 and capability-v3 schemas, source records, curve parameters and input axis are unchanged.

| Quantity for the 100 MW reference | Preserved v1.2 | v1.3 binding |
|---|---:|---:|
| Full TIV | $140M | $162.3M |
| Covered tower | $22.4M | $27.6M |
| Tower share | 16% | 276/1623 = 17.005545% |
| Value withheld from this response | $117.6M | $134.7M |

The new budget is 100,000 kW × $276/kW from `Wind_Map:9` in the SHA-pinned value workbook.
Full physical TIV uses $1,623/kW. Installation and transport remain in full TIV; this tower response
does not receive an additional repair-support allocation. No DC/AC conversion or 5/3.3 multiplier applies.

The source paper's value denominator remains ambiguous. This narrow, owner-approved screening transfer
does not establish claim calibration or a general conversion from the source denominator to modern
replacement cost. Only the exact named physical tower binding is admitted; generic CWER, equipment-assembly
and whole-plant substitutions remain prohibited. The other 82.994455% is **withheld, not zero loss**.

The proposal pins its parent artifact, source workbook, canonical cost rows and resolved reference. Its
builder and validator are in `scripts/reference_helpers/`. The adjacent verification JSON records source
known answers, proxy known answers, negative identity checks, a 4,001-speed exact-response sweep and schema
validation. Hazard independently verifies the value identity and national caps/placement selections.
The current v1.2 package and registry remain intact until the successor's consumer and release gates close.
This proposal is not a completed recipient release or a change to the live dashboard.

For reproduction, run from Damage using an environment with the repository dependencies:

```sh
python scripts/reference_helpers/validate_tropical_cyclone_wind_wind_v1_3_value_binding.py
```

Hazard plan: `docs/plans/_cross_cutting/canonical_asset_profile/02_solar_wind_value_basis_and_delivery_v2.md`.
Owner acceptance: Hazard `docs/plans/_cross_cutting/conus_grid/decisions.md`, DD-G31.
