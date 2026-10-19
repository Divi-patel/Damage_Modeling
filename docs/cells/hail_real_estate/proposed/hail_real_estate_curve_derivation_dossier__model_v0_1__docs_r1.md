<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-18
status: draft
-->

# hail_real_estate curve derivation dossier — model v0.1 / docs r1

How the hail × real estate curves were derived, from evidence to tabulated records. Decisions are D-HRE-… in the
[decision log](DECISION_LOG_hail_real_estate__model_v0_1__docs_r1.md); claims HRE-C… and sources HRE-S… are in the
registers.

## 1. Scope, asset boundary, and failure mechanisms

The assets are the three Hazard reference buildings r1 (HRE-C012), each with a roof cover that is 10 years old.
Hail damages a building in four ways:

| Mechanism | Parts | Treatment |
|---|---|---|
| Puncture, fracture or rupture of the roof cover; opened seams | shingles, TPO membrane, steel panels | **priced** (roof cover unit) |
| Cracked or holed cladding; broken glazing | vinyl siding; windows | **priced, Tier-4** (walls and windows unit) |
| Bent fins or punctured coils on outdoor equipment | AC condenser, rooftop units | withheld, not zero |
| Dents that leave function intact | metal roof, metal walls, overhead doors, gutters | excluded (cosmetic, D-HRE-05) |

Consequential rain entry and interior damage after a breach, deck punctures by giant hail, and cumulative damage
from repeated small hail are not priced (D-HRE-13).

## 2. Failure-unit decomposition and coverage

| Unit | Treatment | Share of structure value (house / warehouse / office) |
|---|---|---|
| `HRE_ROOF_COVER` | primary_nonzero | 3.75% / 12% / 2.7% |
| `HRE_WALLS_AND_WINDOWS` | secondary_conditional (Tier-4, acknowledgement required) | 6.07% / 0.57% / 5.34% |
| `HRE_EXPOSED_EQUIPMENT` | withheld | not allocated |
| `HRE_BUILDING_CONTENTS` | withheld | separate value |

Each unit's damage ratio is a fraction of its own value. The building-level ratio is Σ unit DR × share (D-HRE-06).
The units do not overlap. The rest of the structure (frame, deck, foundation, interiors) has no hail mechanism priced.

## 3. Hazard axis and local exposure bridge

Hazard's hail chain sends, for each native radar pixel (about 1 km),
`mesh_diameter_mm = MESH75 = 15.096 × ((raw MESH / 2.54)²)^0.206`, capped at 203.2 mm. Pixels with raw MESH below
25.4 mm get zero damage. Larger footprints are area-weighted over pixels, and a cell maximum is prohibited
(HRE-C013; S008).

- **MESH75 floor.** MESH75 at the 25.4 mm threshold is **38.98 mm**, so every event pixel arrives at 1.53 in or
  more. With raw MESH capped at 203.2 mm, MESH75 tops out at about 92 mm.
- **What Damage does with it.** Damage takes the field as delivered and reads it as the largest hailstone at the
  building. The roof thresholds are in that unit (largest stones observed or launched).
- **No bridge in Damage.** No conversion is made here. The dependence of building loss on MESH75 is a Hazard-side
  item (§13, D-HRE-16).

## 4. Source register summary

A bounded search covered FEMA (Hazus, P-2055), IBHS, AMS conference preprints, NHESS, Frontiers, IIBEC, Professional
Roofing, engineering-firm briefs and the repository's own hail cells.

**What was not found:**

- No published US building hail vulnerability curve exists; Hazus has no hail model.
- No lab or field threshold exists for vinyl siding or building glazing.
- Some sources were blocked: the claims study by Brown et al. 2015 (WCAS 7:197-210) and the IBHS DFW 2011 member
  report were paywalled, and the FM Global data sheet 1-34 and FM Approvals pages returned access errors. They are
  recorded as leads, not used.

| ID | Source | Role |
|---|---|---|
| HRE-S001 | Marshall et al. (Haag), AMS 2002: lab and field hail thresholds | house roof band |
| HRE-S002 | Morrison (Haag), Professional Roofing 2009: low-slope thresholds | office band; warehouse onset |
| HRE-S003 | Kestner & Kennedy, CLM 2016 (Haag 2010 metal rupture ≥ 2.5 in) | warehouse onset; cosmetic exclusion |
| HRE-S004 | Olson (SGH) 2026 topic brief | cross-check; no wall/window rating |
| HRE-S005 | Bhawalkar et al., IIBEC 2017: heat-aged TPO ice-ball tests | office low case |
| HRE-S006 | FEMA Hazus 7.0 Hurricane TM, cost ratios and repair factors | roof cost shares |
| HRE-S007 | Hazard reference profiles r1 | selectors, geometry, budgets |
| HRE-S008 | Hazard hail pipeline (MESH75, per-pixel rule) | axis |
| HRE-S009 | Schmid et al. 2024 NHESS: Swiss radar-to-claims building curve | cross-check only |
| HRE-S010 | Meisenzahl et al. 2025 (IBHS): sub-severe hail on shingles | limitation |
| HRE-S011 | Ezold (Vertex) 2018, citing IMECE2007-41518: hail fin damage | equipment withheld |
| HRE-S012 | FEMA NRI Dec 2025 (Hazard extract) | NRI check |
| HRE-S013 | Smith, IIBEC Interface 2013: steep-slope threshold table | corroboration |
| HRE-S014 | hail_wind legacy audit (this repository) | legacy rejection |
| HRE-S015 | Hazard generic damage loader | consumer probe |

## 5. Claim/parameter provenance map

| Parameter | Value | Claims | Tier |
|---|---|---|---|
| house roof band | 1.25–2.0 in | C001, C002 | T3 |
| office roof band | 1.0–2.0 in | C004, C006, C007 | T3 |
| warehouse roof band | 2.5 in (onset) – 3.5 in (full) | C005, C021 | T3 / T4 |
| house roof share | 3.75% | C008, C009 | T2/T3 |
| office roof share | 2.7% | C010 | T2/T3 |
| warehouse roof share | 12% (9–15%) | C011, C022 | T4 |
| walls and windows | sizes, hail-facing shares, unit costs | C006, C023 | T4 |
| band reading | onset 5%, full 95% | C020 | T4 |
| axis | MESH75 as delivered | C013 | T4 |

## 6. Evidence pressure test

| Question | Answer |
|---|---|
| Do lab thresholds overstate damage? | Yes, somewhat: freezer ice is harder than natural hail, and impacts were square-on (S001 p. 2). The adopted band therefore sits at or above the lab points: 36% at 1.5 in, where 60% of lab impacts damaged aged laminated shingles. |
| Does one damaged hit mean a new roof? | Insurance and Hazus practice replace the whole cover at a low damaged share; Hazus uses 0.5% for asphalt roofing (HRE-C009). Once the size is in the band, hits are numerous, so the replacement probability follows the material band. |
| Is the shingle type right? | The profile says only "asphalt shingle". Laminated is assumed; 3-tab moves the house onset to 1.0 in (high case: +42% yearly loss in the NRI check). |
| Is the TPO attachment right? | Not stated. An adhered membrane on a cover board resists 2 in ice balls (S005), which is the low case (−72% yearly loss). A mechanically attached membrane over soft insulation sits at the bottom of the Haag range. |
| Is the warehouse roof ever damaged? | Rarely. Under MESH75, inputs above 63.5 mm need raw MESH above about 83 mm. Counting cosmetic denting would make warehouse loss similar to the house's (D-HRE-05 alternative). |
| Is the Swiss curve contradicted? | No, it measures something different. Its 0.05% MDR at 60 mm averages over all buildings in a pixel, and only 5% of them claim; per claiming building that is about 1%. Swiss stock has tile roofs and blinds (HRE-C014). |
| Are walls and windows evidenced? | No public threshold exists (S004). The unit is Tier-4 and gated by an acknowledgement. |

## 7. Y-axis and row-level value crosswalk

`failure_unit_damage_ratio` = repair or replacement cost ÷ replacement cost of the same unit. Each unit's share of
structure replacement cost new comes from the
[value crosswalk](VALUE_CROSSWALK_hail_real_estate__model_v0_1__docs_r1.csv):

- **House roof:** Hazus 3% × 1.25. This implies about $685 per 100 ft² square on the $405,000 budget.
- **Office roof:** Hazus (1.1% + 0.7%) × 1.25 × 1.20. This implies about $16.20/ft² of roof.
- **Warehouse roof:** judgment, 100,347 ft² × about $13.15/ft² ÷ $11.0M.
- **Walls and windows:** the profile's areas × judgment unit costs ÷ the budget.

The denominator is shared with the other real-estate cells, and scenario dollars are withheld (D-HRE-15).

## 8. Site-condition adapter and double-counting matrix

| Pair | Rule |
|---|---|
| roof cover × walls and windows | disjoint parts; add after multiplying by shares |
| hail × wind (same storm) | separate cells; consumer keeps the total at or below 100% of structure value; a roof cover replaced for hail cannot also be replaced for wind in the same event (consumer) |
| hail × flood | separate cells; same 100% rule |
| equipment, contents | withheld; never zero |
| roof age, shingle type, TPO attachment | fixed by the profile and assumptions (no conditioner in v0.1) |

## 9. Curve-form decision

For each part p, with onset o and full f in mm:

```text
median m = sqrt(o * f)        beta = ln(f / o) / (2 * 1.645)
P_p(D)   = Phi( ln(D / m) / beta )                       (onset = 5%, full = 95%)
DR_unit(D) = sum_p (v_p / V_unit) * e_p * P_p(D)          (v_p = part share, e_p = hail-facing share)
```

| Record | Parts (onset–full, hail-facing share) | Median, β | Ceiling |
|---|---|---|---|
| `HRE_RES_ROOF_ASPHALT_SHINGLE_LAMINATED` | shingles 1.25–2.0 in, 1 | 40.2 mm, 0.143 | 1 |
| `HRE_IND_ROOF_STANDING_SEAM_STEEL` | steel panels 2.5–3.5 in, 1 | 75.1 mm, 0.102 | 1 |
| `HRE_OFF_ROOF_TPO_MEMBRANE_AND_INSULATION` | TPO 1.0–2.0 in, 1 | 35.9 mm, 0.211 | 1 |
| `HRE_RES_WALLS_WINDOWS_T4` | siding 1.25–2.0 in, 0.5; windows 1.5–2.5 in, 0.25 | — | 0.364 |
| `HRE_IND_WINDOWS_T4` | windows 1.5–2.5 in, 0.25 | 49.2 mm, 0.155 | 0.25 |
| `HRE_OFF_WINDOWS_T4` | windows 1.5–2.5 in, 0.25 | 49.2 mm, 0.155 | 0.25 |

The curves are tabulated at 205 knots (0–203 mm every 1 mm, plus 203.2 mm) and rounded to 6 decimals. The rounded
table is the governed curve. The largest difference between the table and the exact expression is 0.0011, on the
house roof near 33.5 mm.

**Rejected forms:**

- A step at the threshold, which jumps from 0 to 1.
- A straight ramp from onset to full, which has kinks and no tails.
- A logistic as in hail × solar, which is not the convective cell's reading of bounds.

## 10. Parameter derivation and tiers

All parameters are in the
[parameter tier table](PARAMETER_TIER_TABLE_hail_real_estate__model_v0_1__docs_r1.csv) and the
[component fragility table](COMPONENT_FRAGILITY_TABLE_hail_real_estate__model_v0_1__docs_r1.csv), which is the
governed input.

## 11. Seven-step audit

| Step | Result |
|---|---|
| 1. Mechanism | Hail impact breaks roof covers, siding and glass. Cosmetic denting is separated out. |
| 2. Axis | Hazard's MESH75 diameter, as delivered; the floor at 38.98 mm is recorded. |
| 3. Failure unit | Roof cover; walls and windows (Tier-4); equipment and contents withheld. |
| 4. Value | Unit-own denominator plus shares of structure replacement cost new; shared with the other real-estate cells. |
| 5. Evidence | Roof thresholds T3 (Haag, two independent write-ups); house and office costs T2/T3 (Hazus); warehouse cost and walls/windows T4. |
| 6. Uncertainty | Point values; low/high cases and band readings in SENSITIVITY; not sampleable. |
| 7. Fail-closed | Above 203.2 mm withholds; negative is an error; walls need the acknowledgement; withheld units are never zero. |

## 12. Derivation rationale

The cell follows JL's choices: roof-cover curves from material thresholds (D-HRE-01), real damage only (D-HRE-05),
parts on their own value with a share (D-HRE-06), a separate Tier-4 walls-and-windows unit (D-HRE-04), and a central
curve with the range in SENSITIVITY (D-HRE-12).

Building-level damage per event (central), as % of structure replacement cost new:

| Hail size | 1 in | 1.25 in | 1.5 in | 38.98 mm (MESH75 floor) | 1.75 in | 2 in | 2.5 in | 3 in | 3.5 in |
|---|---|---|---|---|---|---|---|---|---|
| House roof | 0.00 | 0.19 | 1.34 | 1.56 | 2.85 | 3.56 | 3.75 | 3.75 | 3.75 |
| House roof + walls/windows | 0.00 | 0.26 | 1.87 | 2.19 | 4.12 | 5.36 | 5.92 | 5.96 | 5.96 |
| Warehouse roof | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.60 | 6.66 | 11.40 |
| Office roof | 0.13 | 0.75 | 1.65 | 1.76 | 2.28 | 2.57 | 2.69 | 2.70 | 2.70 |
| Office roof + windows | 0.13 | 0.76 | 1.71 | 1.85 | 2.62 | 3.34 | 3.96 | 4.03 | 4.03 |

## 13. NRI check

This is an order-of-magnitude and ranking check, not a calibration
([NRI_CHECK](NRI_CHECK_hail_real_estate__model_v0_1__docs_r1.csv); inputs pinned in the
[receipt](NRI_CHECK_RECEIPT_hail_real_estate__model_v0_1__docs_r1.json)).

**Method.**

- Hazard's raw MRMS daily evidence covers 2,071 days (2020-10-14 to 2026-06-15) on 12,374 QC-eligible cells with an
  NRI value.
- For each severe cell-day, the raw-MESH distribution over its severe pixels is rebuilt from the five values Hazard
  keeps (25.4 mm, p50, p90, p95, maximum).
- Hazard's per-pixel rule (MESH75, then the curve) is applied to a building at a random pixel, and the result is
  summed per year.
- This uses the raw record, not Hazard's pooled M1 model.

| Building, variant | Ours, median %/yr | Ours ÷ NRI (median; p10–p90) | Rank corr. |
|---|---|---|---|
| House, roof (central) | 0.112 | 73 (9–650) | 0.70 |
| House, roof + walls/windows | 0.162 | 105 (13–950) | 0.69 |
| House, roof, Hazard Version-1 size transform (raw × 25.4/35.56) | 0.0012 | 1.2 (0–35) | 0.57 |
| Warehouse, roof (central) | 0.0000 (p90 0.0024) | 0.01 | 0.50 |
| Warehouse, roof, cosmetic denting counted (not adopted) | 0.111 | 75 (7–710) | 0.67 |
| Office, roof (central) | 0.099 | 64 (9–560) | 0.70 |
| Office, roof low (adhered on cover board, membrane only) | 0.028 | 18 (2–170) | 0.68 |
| NRI hail building EAL rate | median 0.0014 | — | — |

**Readings.**

- **Point frequency.** Point severe-hail frequency (raw MESH ≥ 25.4 mm at a pixel) is 0.047 days a year in the
  median cell and 0.30 in the Plains (TX, OK, KS, NE, CO, SD).
- **House roof replacement rate.** The central house roof is replaced on average 0.030 times a year in the median
  cell (once in about 33 years), and 0.20 times a year in the median Plains cell (once in about 5 years).
- **Ours vs NRI.** Our yearly loss is one to two orders of magnitude above NRI, with a similar ranking (0.70). NRI is
  built from reported loss records. Its national hail building loss on Hazard's grid sums to about $0.67B a year on
  $13.2T of exposure. US insured severe-convective-storm losses were about $54B in 2023 (85% of $64B globally;
  HRE-S010 citing Swiss Re), so NRI is a floor, not a target.
- **The MESH75 floor dominates.** Under Hazard's earlier Version-1 transform, the house would sit at NRI's level
  (1.2×). Under MESH75 it is 73×. The transform choice moves building loss by a factor of about 90, far more than any
  Damage-side choice. This is the main Hazard-side item.

**Hazard-side items for the reviewer:**

1. **MESH75 floor.** Every severe pixel enters damage at 38.98 mm or more, at or above the shingle and TPO onsets.
   Building yearly loss depends mostly on this transform.
2. **Point frequency.** It rests on the raw radar record (5.7 years). MRMS MESH over-detects severe hail (S009
   reports a large false-alarm ratio for the Swiss equivalent).
3. **Footprint.** A building is much smaller than the plant footprints the hail × solar coupling was designed for.
   The per-pixel rule applies unchanged.

## 14. Capability and fail-closed decision

- **Supported:** a conditional scalar DR per unit (`scalar_mean`).
- **Withheld:** scenario dollars (until the consumer qualifies the budget); annual and tail metrics (consumer-owned);
  equipment and contents (withheld, not zero).
- **Errors:** missing or unknown pathway, building or unit; missing or invalid axis; a negative diameter; walls
  without or with a wrong acknowledgement.
- **Withhold:** above 203.2 mm.

## 15. Open seams and update triggers

- **Profile details.** Shingle type, TPO attachment and cover board, and metal panel gauge and coating are not in the
  profile. The low and high cases cover them.
- **Warehouse roof share.** 12% is judgment; a published metal-roof rate would replace it.
- **Walls and windows.** The whole unit is Tier-4.
- **Not modelled.** Interior leakage after a breach, and cumulative small hail.
- **Hazard items (§13).** The MESH75 floor, point frequency, footprint.
- **Value.** Consumer value qualification, shared with the other real-estate cells.

## 16. Validation/QC

See the [validation report](VALIDATION_REPORT_hail_real_estate__model_v0_1__docs_r1.md): validator checks, hand
checks, the Hazard loader probe and what is not validated.
