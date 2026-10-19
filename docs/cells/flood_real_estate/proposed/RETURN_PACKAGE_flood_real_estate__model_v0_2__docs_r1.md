<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# Return package for Hazard — flood × real estate, model v0.2

The Damage return for the flood pathway of the three Hazard reference profiles r1, in the fields the profile
handoff asks for: one card per profile (§2–§4) and one worked example (§5). Everything here is a **noncanonical
proposal** (model v0.2 / docs r1, promotion gate blocked); nothing is admitted at runtime.

## 1. Summary

| Profile | Freshwater (riverine, pluvial) | Coastal surge (still water) | Wave / velocity |
|---|---|---|---|
| `re_house_1s_wood_slab` | `FRE_RES_HAZUS_DF129` — exact match | same record — qualified proxy | unavailable (withheld, not zero) |
| `re_warehouse_1s_steel_slab` | `FRE_IND_HAZUS_DF341` — exact match | same record — qualified proxy | unavailable |
| `re_office_3s_slab` | `FRE_OFF_HAZUS_DF431` — qualified proxy | same record — qualified proxy | unavailable |

Shared by all three cards:

| Item | Content |
|---|---|
| Profile pin | Hazard reference profiles **r1**, `aamani-ai/Hazard_Modeling` commit `8b0d61c88fbcf85daa1c098516cee22398cdb524`, `docs/plans/_cross_cutting/real_estate_conus/reference_candidates.yml` (git blob `a74fb72b0a2edce593b5505e0fd8852f4c0253f8`); source FRE-S013 |
| Damage artifact | `flood_real_estate` model v0.2 / docs r1, [`flood_real_estate__model_v0_2__docs_r1__curve_artifact.json`](flood_real_estate__model_v0_2__docs_r1__curve_artifact.json), sha256 `99fe3f1f6430caada7943a4a83fe74a2f94895c8c454d7789fda97fabfafe9af`, branch `cell/flood-real-estate` of `aamani-ai/Damage_Modeling` (package built at commit `6c00944`) |
| Pathway, unit | `flood_inundation_contact`, failure unit `FRE_BUILDING_STRUCTURE` (contents unit withheld) |
| Demand | `flood_depth_above_first_floor_ft` (ft above the first finished floor), the source-native axis read by the common v3 loader. Hazard converts from grade once with the profile's first-floor height; a floor-relative value is never shifted again. The reference evaluator also accepts `flood_depth_above_grade_ft` |
| Dry and domain | Depth above grade ≤ 0 → 0 (D-FRE-24): **Hazard applies this when it sends floor-relative depth** (the loader returns 5.5% for a dry slab house otherwise). Domain −4 to 24 ft above the floor; below → 0; above → withheld `ABOVE_SOURCE_VALID_RANGE` |
| Conditioner | `flood_water_type` (event state, Hazard-owned) required; freshwater and coastal surge give the same record; `unknown` → withheld `FLOOD_WATER_TYPE_UNKNOWN`. Wave-exposed (V-zone) damage is not in this pathway |
| Output | Conditional failure-unit damage ratio (expected repair/replacement fraction of structure value) for one event; not a damage-state probability; no frequency, annual metric or downtime |
| Uncertainty | Point value only: no sampleable spread. Recorded biases are epistemic statements (§2–§4), not bands |
| Value | Source denominator: Hazus structure replacement value. Covered: foundation/floor, frame, roof, walls/openings, fixed services, interiors **as one source-native assembly**. Excluded: contents, land, site works, BI, process equipment. Covered fraction of the profile budget **not stated by the source** (Hazus does not itemize "structure"); not set to 1.0 here — Hazard's value-qualification call. Overlap: no component response may be added for the same pathway and event |
| Consumer probe | Hazard `damage_loader.py` (main `509bf435`) routes all three profiles for both water types and matches the reference evaluator ([validation report v0.2](VALIDATION_REPORT_flood_real_estate__model_v0_2__docs_r1.md) §4) |
| Reproduce | `python scripts/reference_helpers/build_flood_real_estate_v0_2_package.py`; `python scripts/reference_helpers/validate_flood_real_estate_v0_2_package.py` (33/33); one call: `python scripts/reference_helpers/flood_real_estate_curve_eval.py docs/cells/flood_real_estate/proposed/flood_real_estate__model_v0_2__docs_r1__curve_artifact.json '{"pathway_id":"flood_inundation_contact","reference_building_id":"RE_IND_WAREHOUSE","flood_water_type":"freshwater_riverine_or_pluvial","flood_depth_above_first_floor_ft":2}'` |
| Missing profile detail | **None changes curve selection.** First-floor height and the office's three storeys matter and are already declared |

## 2. Card — `re_house_1s_wood_slab`

| Field | Content |
|---|---|
| Profile pin | r1 @ `8b0d61c8` (shared, §1) |
| Applicability | **Freshwater: exact match** — Hazus RES1, one storey, no basement are the keys the source selects on; class average. **Coastal: qualified proxy** — a riverine curve for coastal still water (FEMA's own coastal-A house default, DF 658, includes waves and is not used for still water) |
| Evidence | FRE-S002 Hazus 7.0 Flood TM Table 5-2, pp. 5-3 to 5-6 (default DF 129, unchanged since 5.1); ordinates FRE-S003 / FRE-S010, identical in both; NFIP claims FRE-S012 (FRE-C026, C027, C029, C030, C031). Extracted (% of structure value, ft above floor): −1 → 3, 0 → 13, 1 → 23, 2 → 32, 4 → 47, 8 → 67, 12 → 77, 24 → 84 |
| Physical / value mapping | Selector `RE_RES_SFD_1S_SLAB`, first-floor height 0.75 ft (NSI 2026 documented default; profile value). Budget $405,000; covered fraction not stated by the source (§1) |
| Response contract | Shared (§1). Record `FRE_RES_HAZUS_DF129`, straight lines between 29 published points |
| Uncertainty | Point only. Known biases: 9–12 points below NFIP claims at 0–2 ft above the floor (mostly a floor-height effect: 3 points with the floor at grade); coastal claims are about the same as freshwater claims at the same depth |
| Tests | 42 house-specific known-answer tests (every knot, both water types for interior, bridge, dry, below/above range, unknown water, contents withheld, floor-height override) plus 12 shared contract errors; all pass |
| Deliverable | Shared (§1); NACCS 5A kept as a recorded alternative (D-FRE-28) |

## 3. Card — `re_warehouse_1s_steel_slab`

| Field | Content |
|---|---|
| Profile pin | r1 @ `8b0d61c8` |
| Applicability | **Freshwater: exact match** — Hazus COM2 (wholesale trade / warehouse), no basement; class average of 22 wholesale/warehouse classes. **Coastal: qualified proxy** — FEMA assigns DF 341 to COM2 in coastal A and V zones; little claims evidence (below) |
| Evidence | FRE-S002 Table 5-2 (default DF 341); FRE-S003 / FRE-S010 ordinates; FRE-S010 `flBldgStructDmgFinal` (coastal assignment); NFIP FRE-S012 (FRE-C026, C037). Extracted: 0 → 0, 1 → 5, 2 → 8, 4 → 13, 8 → 25, 12 → 41, 24 → 73 |
| Physical / value mapping | Selector `RE_IND_WAREHOUSE`, first-floor height 0.25 ft (NSI records, three counties, T3; profile value). Budget $11.0M; covered fraction not stated by the source |
| Response contract | Shared (§1). Record `FRE_IND_HAZUS_DF341` |
| Uncertainty | Point only. Freshwater: 2–8 points below 365 NFIP warehouse claims under 3 ft. Coastal: on 14 coastal warehouse claims at 1–3 ft (mean 14%) DF 341 reads 7% — likely low. Most floor-height-sensitive building: at 2 ft above grade, 7% at 0.25 ft vs 0% at 2 ft |
| Tests | 40 warehouse-specific known-answer tests plus the shared contract errors; all pass |
| Deliverable | Shared (§1); NACCS prototype 3 kept as a recorded alternative. Worked example: §5 |

## 4. Card — `re_office_3s_slab`

| Field | Content |
|---|---|
| Profile pin | r1 @ `8b0d61c8` |
| Applicability | **Freshwater and coastal: qualified proxy** — Hazus DF 431 is FEMA's default for COM4 at every height class and in riverine, coastal A and coastal V zones (FRE-C033); the office (COM4, low-rise, no basement) matches those keys, but the Galveston class average is not height-specific. A new selector, not the retail record (D-FRE-27) |
| Evidence | FRE-S002 / FRE-S010 (default assignment), DF 431 ordinates identical in FRE-S003, FRE-S005, FRE-S010 (FRE-C032); NFIP business claims by floors (FRE-C034, C035); alternatives rejected (FRE-C036). Extracted: 0 → 2, 1 → 11, 2 → 16, 4 → 28, 8 → 44, 12 → 57, 24 → 80. Research: [office flood research](OFFICE_FLOOD_RESEARCH_flood_real_estate__model_v0_1__docs_r1.md) |
| Physical / value mapping | Selector `RE_COM_OFFICE_3S_SLAB`, first-floor height 0.25 ft. Budget $10.8M; whole-building ratio, **not allocated by floor area**. Elevator pit and ground-floor controls inside the assembly; rooftop HVAC never reached within the curve's range |
| Response contract | Shared (§1). Record `FRE_OFF_HAZUS_DF431` |
| Uncertainty | Point only. **Known height bias:** about ×1.6 the NFIP three-or-more-floor business claims at shallow depth (6.3% claims vs 9.8% curve, 228 claims); the NFIP ratio (about 0.75 for two floors, 0.5 for three or more) is a stated sensitivity, not a factor. Coastal: within 2–5 points of multi-floor coastal claims |
| Tests | 40 office-specific known-answer tests plus the shared contract errors (including a profile ID sent as a selector); all pass |
| Deliverable | Shared (§1); NACCS prototype 2 recorded as the rejected coastal alternative |

## 5. Worked example — warehouse, from source to number

How the warehouse flood response was reached, for reuse on the next profile or peril.

**1. Target.** One-storey, 100,000 ft² pre-engineered steel warehouse on a slab, first floor 0.25 ft above grade,
no dock pits, 4,000 ft² office fitout, building scope only (profile r1).

**2. Sources considered.**

| Source | What it offers | Kept? |
|---|---|---|
| Hazus DF 341 (COM2, average of 22 wholesale/warehouse classes, USACE Galveston) | FEMA's default for warehouses, all zones | **Yes** |
| Hazus DF 559 (IND2, light industrial average) | A manufacturing building, not storage | No: different occupancy (D-FRE-17) |
| Individual Hazus warehouse classes | Range from about 1% to 62% at 4 ft | No: no basis to pick one; the average is the default |
| NACCS prototype 3 (one-storey steel or light-metal, slab) | Purpose-built coastal curve with low/high bounds | No for v0.2: about twice the few coastal claims; kept as alternative (D-FRE-28) |
| NFIP claims (FRE-S012) | Paid losses for one-floor business and warehouse buildings | As a check, not a fit |

**3. Verification.** DF 341 ordinates were checked in three carriers (Pollack compilation, go-consequences, the
Hazus 6.1 extract); the default assignment in Hazus 5.1, 6.1 and 7.0 manuals and the 6.1 default table.

**4. Applicability.** Every key FEMA selects on (occupancy COM2, no basement) matches; size, steel frame, fitout
and equipment heights are not keys. Freshwater: exact match. Coastal: FEMA applies the same default in coastal
zones; qualified because coastal warehouse claims are few.

**5. From depth to number.** A cell reports 2.0 ft of river water above grade:

```text
depth above floor = 2.0 − 0.25 (profile first-floor height)      = 1.75 ft
DR = 5% + 0.75 × (8% − 5%)      (straight line between 1 and 2 ft) = 7.25%
dollars (if Hazard qualifies the full budget) = 0.0725 × $11.0M    = $797,500
```

Same depth of coastal surge: the same record and the same 7.25% (v0.1 gave 26% with NACCS prototype 3).
At 12 ft above grade: 40% (v0.1 withheld; NACCS ends at 10 ft). Dry ground: 0.

**6. What the evidence says about the number.** On 365 freshwater warehouse claims under 3 ft the curve is 2–8
points low; on 14 coastal claims at 1–3 ft it is about half the claims. Floor height moves the result more than
the curve choice: at 2 ft above grade the warehouse reads 8% with the floor at grade and 0% with a 2 ft floor.

**7. Unresolved limits.** Coastal evidence is thin (likely low); the 0.25 ft floor height is a three-county NSI
default (T3); the covered fraction of the $11.0M budget is not itemized by the source; wave-exposed sites need the
deferred wave pathway; contents and stock are excluded.
