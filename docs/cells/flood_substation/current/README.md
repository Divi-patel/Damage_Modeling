---
author: "owner-directed (Divy) · agent-implemented"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Standalone Substation Flood assembly screening, using existing hazard methods.
---

# Flood × Substation: assembly screening v1.0

Owner-selected first delivery: one canonical station, existing Pluvial/Riverine/Coastal hazard methods, both map resolutions, tagged zero contributions where unsupported. This is a separate standalone cell; it does not promote or loosen the existing `flood_wind` contract.

Read [derivation and seven-step audit](derivation.md), [metadata](metadata.md), [curve audit](curve_audit.csv) and [capability](flood_substation__model_v1_0__docs_r1__capability.json). The curve is the exact legacy Hazus table. Coastal reuse is explicitly T4 and depth-only. No intrinsic spread, component curves, saline/wave adjustment or >10 ft response is invented.

Annual metrics belong to Hazard and are conditional on the machine-declared probability, value, cap and coverage checks. Missing DR remains null; the owner's zero-with-tag convention belongs to the consumer's modeled-contribution projection. Complete grid rows are not complete physical risk coverage. National scientific/release identity remains Hazard-owned.


## Physical scope and coverage

```text
Flood × one canonical Substation
└── Fenced facility assembly: one mutually exclusive direct-loss atom
    ├── Yard and electrical equipment: implicit in the source assembly
    ├── Control/protection and civil works: implicit, no separate component DR
    └── Outside fence / land / interruption: excluded
```

| Bucket | v1 treatment | Update trigger |
|---|---|---|
| Primary nonzero | Whole-facility assembly `FW_HAZUS_GSU_SUBSTATION_ASSEMBLY`; direct repair cost divided by the same facility replacement cost | Qualified station/component evidence |
| Conditioner-only | No equipment-height or adaptation adjustment supported; source elevations are built into its table | Valid component response/elevation binding |
| Secondary equipment | No separate loss curve; adding one would overlap the assembly | Component inventory and disjoint cost shares |
| DR≈0 | No universal zero-damage equipment bucket; zero depth is the source-table zero | Different mechanism or demand |
| Out of scope | Salinity chemistry, waves, velocity/scour, debris, movable contents, interruption and outside-fence scope | Separate supported mechanism and value boundary |

The physical inventory is the selected 345/138 kV AIS reference, 150 × 178 m, two 336 MVA
transformers. It is a design reference, not a claim about average US stations. The source is
broader than that design and does not resolve its detailed equipment heights.

The x-axis is water depth above station grade in feet; the y-axis is direct physical loss
ratio. Select this standalone screening contract and Flood sub-peril explicitly. Exposure
comes from Hazard; value comes from the separately pinned same-station binding. A positive
depth beyond 10 ft is unavailable, not zero physical loss. No component response, capacity
scaling or equipment-elevation correction is implied.

## Audit workbook map and documented deviation

This inherited one-table release uses a CSV audit set in place of a new spreadsheet workbook.
The artifact's `source_workbook` field points to `curve_audit.csv`. No fit or multi-sheet
calculation is being added: all 11 source ordinates are copied exactly and verified against
the independently pinned predecessor artifact. This is the bounded deviation allowed by
Cell Package Standard §6; CSVs and JSON are inspectable and do not need spreadsheet macros.

| Question | Audit file |
|---|---|
| Exact source knots and resulting response | [curve_audit.csv](curve_audit.csv) |
| Source and limitation provenance | [sources.csv](sources.csv), [claims.csv](claims.csv) |
| Same-station denominator and excluded values | [value_crosswalk.csv](value_crosswalk.csv) |
| Executable examples and proof | [known_answers.json](known_answers.json), [validation.json](validation.json) |

Implementation uses the linear interpolant within the table only. The consumer installs exact
JSON bytes and validates SHA, schema and its separate annual construction. Component-first
research is deferred; its arrival, a changed canonical station/value, or materially better
whole-station evidence triggers a new binding or model version. The [basics set](../basics/README.md)
provides the first-reader explanation.
