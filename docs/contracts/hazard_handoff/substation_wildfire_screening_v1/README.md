---
author: "owner-directed (Divy) · agent-qualified"
created: 2026-10-17
updated: 2026-10-17
status: active
scope: Standalone station binding to the unchanged canonical Solar Wildfire electrical-equipment response; partial physical value only.
---

# Substation Wildfire — electrical assembly screening binding

Use canonical `wildfire_solar` model v1.0 / docs r3 `WSV1_MV_EQUIPMENT_THERMAL` for the
selected station's transformer/switchgear equipment. This is one Tier-4 assembly transfer, not new
component fragilities or a complete-station fire curve. [binding.json](binding.json) owns the machine
contract; [value_crosswalk.csv](value_crosswalk.csv) is its review export. Hazard installs byte-identical
source/binding resources and owns native source sampling, annual calculation and spatial mixtures.

**Change classification:** inside_repo; consumer binding under the illustrative intake/reuse guide.
No intrinsic Damage response, source model/docs/schema, canonical cell capability or package release
changes. This adds a target value/exposure binding, with its own schema v1. Existing Solar/Wind behavior
is unchanged. The same exact FSim states return the same canonical failure-unit DRs.

## Seven-step qualification

| Step | Binding and reasoning | Limit |
|---|---|---|
| Asset | One 345/138 kV AIS station, two 336 MVA autotransformers, 150 × 178 m fence; exact profile SHA | Hypothetical reference, not surveyed ownership |
| Failure unit | One transformer/switchgear electrical assembly | No whole-station or independent equipment fragility claim |
| Numerator/denominator | Physical repair/replacement DR × bound electrical replacement proxy | No revenue, BI, insurance or capacity surrogate |
| Value partition | Eight equipment rows: $13,025,357; remaining fenced value $14,327,879.37 withheld | Full fenced TIV stays $27,353,236.37 for cross-hazard %TIV comparisons |
| Value allocation | Breakers, disconnects, voltage transformers, arresters and main transformers; installed source row amounts once | MV-to-HV and instrument/protection-equipment membership are explicit T4 engineering transfers; no extra repair-support uplift |
| Exposure | Existing FSim categorical state at the facility reference point; local attack integrated in source response | No extra contact, perimeter, gravel, firebreak, firewall or enclosure credit; no thermal-duration bridge |
| Capability | Source permits consumer annual metrics after frequency/class/value/cap and aggregation proof | Wind's separate withheld annual capability is not used; unsupported station value stays withheld |

Source numerical authority: [canonical cell](../../../cells/wildfire_solar/README.md), especially its
`ORDINATE_TABLE` and `VALUE_LINKAGE` under current/. Transformer/switchgear DRs for the six source-native
classes are 0.001, 0.006, 0.03, 0.12, 0.35 and 0.70. Zero is the no-event control. Absolute ordinates
are T4, not measured failure probabilities; class states cannot be interpolated or treated as heat flux.
The source direct-equipment denominator supports retaining equipment rows; it does not justify applying
these ordinates to control buildings, cables, foundations, metal supports or site works.

The chosen electrical grouping is intentionally coarse. It does not resolve tank/oil versus breaker or
instrument behavior, nor add new evidence for that split. Its future replacement trigger is a qualified
station-specific electrical or component model. For this delivery, one source response is applied once
to the declared assembly; no child losses are added on top. The remaining 52.38% of fenced TIV is a
response gap, not immunity. The external $3,061,823.44 road/support budget is outside the common fenced
reference, consistent with the other station hazards.

## Annual consumer boundary

Hazard samples the existing native FSim capture at admitted alternative station locations. BP and class
probabilities remain separate. Its source burnable-pixel rule and ooze/zero/missing tags remain explicit.
Annual losses cap at $13,025,357, while %TIV divides by the full fenced station value. Spatial aggregation
mixes alternative station annual distributions; it does not add locations as a portfolio or average tails.

Allowed use is a relative Wildfire electrical-equipment screening contribution after the consumer proof.
Complete station loss, observed-site engineering, pricing, claims calibration, resilience benefit and
portfolio Total are outside this binding. No new component research is required for this bounded reuse.

[Hazard work and proof](../../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/20_wildfire_native_grid.md)
records source pins, tests, pilot, cloud execution and remaining checkpoints. Recheck source/value/install
identity with `python scripts/reference_helpers/validate_substation_wildfire_binding.py`.
