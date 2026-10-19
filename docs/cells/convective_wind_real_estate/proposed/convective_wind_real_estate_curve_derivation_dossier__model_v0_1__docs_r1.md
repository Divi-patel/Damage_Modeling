<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-18
updated: 2026-10-19
status: draft
-->

# convective_wind_real_estate curve derivation dossier — model v0.1 / docs r1

How the six proposed records (three buildings × two pathways) are derived, what each number rests on, and what was
checked. Decisions: [decision log](DECISION_LOG_convective_wind_real_estate__model_v0_1__docs_r1.md). Scope:
[proposal README](README_convective_wind_real_estate__model_v0_1__docs_r1.md).

## 1. Scope, asset boundary, and failure mechanisms

The structure of three reference buildings (Hazard profiles r1) under convective wind. Two mechanisms, two pathways:

- **Straight-line wind** (`straight_line_convective`): wind pressure on roof, walls and openings from a downburst, gust
  front or derecho; windborne debris and rain entering through openings as they occur in the surveyed damage.
- **Tornado direct hit** (`tornado_direct_hit`): the same loads plus the rotation, pressure drop and dense debris of
  a tornado, as present in the EF damage surveys.

Out of scope: hurricane wind, hail, lightning, flooding, contents, loss of use (D-CWRE-13).

## 2. Failure-unit decomposition and coverage

One numeric unit, `CWRE_BUILDING_STRUCTURE`, at whole-building grain: the EF degrees of damage and the Hazus damage
states both describe the whole building. `CWRE_BUILDING_CONTENTS` is declared and withheld (not zero).

## 3. Hazard axis and local exposure bridge

Both pathways take a 3-second gust at 10 m in mph, each in its own field so a request cannot be priced on the wrong
pathway: `convective_gust_3s_10m_mph` (Hazard: ASCE 7-22 gust, Exposure C) and `tornado_gust_3s_10m_mph` (Hazard: EF
band midpoint gust). The EF speeds are 3-second gusts "estimated at the point of damage", which "vary with height and
exposure" (CWRE-S002); Damage applies no bridge and flags the difference (D-CWRE-05). An EF rating is never evaluated
as a speed (D-CWRE-15). No terrain class: the EF scale has none (D-CWRE-11).

## 4. Source register summary

| ID | Source | Role |
|---|---|---|
| CWRE-S001 | Texas Tech WSEC, *A Recommendation for an Enhanced Fujita Scale*, Rev 2 (2006) | Expected / lower / upper gust per degree of damage (FR12, MBS, LRB); method |
| CWRE-S002 | NOAA SPC EF scale pages (indicators 2, 17, 21) | Same tables as operated by the NWS; wind-speed basis |
| CWRE-S003 | FEMA Hazus 7.0 Hurricane Technical Manual | Damage-state definitions and the 0/2/10/50/100% loss-ratio correspondence |
| CWRE-S004 | Hazard reference profiles r1 | Building identities and budgets |
| CWRE-S005 | Hazard convective-wind layer (code and data) | Axis, range, frequency and severity for the check |
| CWRE-S006 | FEMA National Risk Index, Dec 2025 | Order-of-magnitude check |
| CWRE-S007 | Repository precedents (solar and turbine convective cells, failure modes) | Onset and pathway-separation precedent |
| CWRE-S008 | Station convective consumer binding | The documented alternative route |

## 5. Claim/parameter provenance map

| Number | Claims | Tier |
|---|---|---|
| Expected, lower and upper gust of each degree of damage | C001, C003–C005 | T3 (expert elicitation, not measurement) |
| Cost per Hazus damage state (2/10/50/100%) | C006 | T3 (FEMA expert judgment) |
| Which Hazus state each EF degree matches; the 1% and 5% points | C007–C010 | T4 judgment |
| Spread β from the bounds | C011 | T4 reading |
| Straight-line onset 96 mph | C013, C014, C016 | T4 |
| Straight-line use of tornado evidence | C018 | T4 transfer |
| Axis, range, EF midpoint bridge | C002, C012 | T2 range; T4 bridge |

## 6. Evidence pressure test

**EF tables.** The three tables were read from the SPC page images and independently from the report text
extraction; all 75 numbers agree. Every degree has LB < EXP < UB.

**Why not a published loss function.** No public convective (thunderstorm or tornado) building loss function by
building type was found. The EF scale is the only building-type-specific convective damage evidence; it gives
damage descriptions and gusts, not costs, so a cost step is unavoidable (C010).

**Costs.** The Hazus correspondence is FEMA's own (expert judgment, used for loss of use), and each EF description was
matched to the Hazus state tables by component (roof cover share, deck panels, openings, frame). Sensitivity
([SENSITIVITY](SENSITIVITY_convective_wind_real_estate__model_v0_1__docs_r1.csv)): halving or doubling the costs at
or below 5% moves damage at 120 mph by about 1 point or less; pricing the house "shifted off foundation" as Complete
raises it from 32% to 48% (straight-line) — the one cost choice that matters.

**Hurricane comparison (context).** In a working-session test (not reproduced in this package), the Hazus hurricane
building curves (open terrain) with an onset at 90% of the local design gust gave similar yearly losses for the house
and office (30× and 14× NRI against 29× and 13× here) and about half for the warehouse (16× against 36×), whose EF indicator fails columns and purlins near
117 mph. That reuse route is the documented alternative (D-CWRE-03).

## 7. Y-axis and row-level value crosswalk

y = repair cost of the structure / structure replacement cost new of the same building; one failure unit holds 100%
([value crosswalk](VALUE_CROSSWALK_convective_wind_real_estate__model_v0_1__docs_r1.csv)). Same value basis as the
flood and hurricane real-estate cells; scenario dollars withheld until the consumer qualifies each budget (D-CWRE-12).

## 8. Site-condition adapter and double-counting matrix

| Overlap | Rule |
|---|---|
| Straight-line vs tornado | Each event is routed to one pathway; separate axis fields enforce it. |
| Tornado vs hurricane | A tornado spawned by a tropical cyclone is priced in one cell only (consumer partition). |
| ASCE straight-line gust vs hurricane | Hazard's ASCE-based layer includes hurricane winds near the coast; the consumer must not price the same wind under both cells (Hazard-side item). |
| Wind vs flood vs hail on one building | Together at most 100% of structure value in one event (consumer). |
| Debris and rain ingress | Inside the EF observations; no separate pathway. |

## 9. Curve-form decision

Each degree of damage i has a causing gust that varies between buildings of the same type; the EF scale gives its
expected value and a range. Reading the range as a 90% interval of a lognormal gives βᵢ = ln(UBᵢ/LBᵢ)/3.29 (0.09–0.13).
The expected repair cost at gust v is then

```text
DR(v) = Σᵢ (cᵢ − cᵢ₋₁) · Φ( ln(v / EXPᵢ) / βᵢ )          (costs cᵢ made non-decreasing; c₀ = 0)
DR_SL(v) = max(0, (DR(v) − DR(96)) / (1 − DR(96)))      (straight-line onset, D-CWRE-09)
```

The expression is tabulated every 1 mph from 0 to 255 mph (6 decimals) by
`derive_convective_wind_real_estate_ef_curves.py`; the rounded table is the governed curve and runs as a bundle-v3
`piecewise_linear` record. A step curve at the expected speeds was rejected (jumps of 40–50 points at one gust); the
ordered-state lognormal record form allows only one β.

Resulting damage ratios:

| Building | Pathway | 100 mph | 120 mph | 140 mph | 160 mph |
|---|---|---|---|---|---|
| House (FR12) | straight-line | 2.0% | 31.8% | 83.4% | 98.9% |
| House (FR12) | tornado | 7.9% | 35.9% | 84.4% | 99.0% |
| Warehouse (MBS) | straight-line | 2.7% | 30.8% | 66.9% | 92.6% |
| Warehouse (MBS) | tornado | 9.7% | 35.7% | 69.2% | 93.1% |
| Office (LRB) | straight-line | 1.3% | 11.3% | 35.1% | 48.9% |
| Office (LRB) | tornado | 5.7% | 15.3% | 38.1% | 51.2% |

Chart: [previews/convective_wind_real_estate_v0_1_curves.png](../previews/convective_wind_real_estate_v0_1_curves.png).

## 10. Parameter derivation and tiers

See the [parameter tier table](PARAMETER_TIER_TABLE_convective_wind_real_estate__model_v0_1__docs_r1.csv) and the
[EF degree-of-damage table](EF_DEGREE_OF_DAMAGE_TABLE_convective_wind_real_estate__model_v0_1__docs_r1.csv) (speeds,
assigned Hazus state, cost and the reason for each assignment).

## 11. Seven-step audit

| Step | Outcome |
|---|---|
| 1. Asset and boundary | Three reference buildings (profiles r1); structure only. |
| 2. Failure units | One whole-building unit; contents withheld. |
| 3. Y-axis and value basis | Repair cost / structure replacement cost new. |
| 4. Value split | One row, 100% of structure value; components not itemized by the source. |
| 5. Allocation by unit and zone | Whole building; no zones. |
| 6. Site-condition adapter | Gust at 10 m open terrain as delivered; no terrain or height bridge; EF midpoint bridge flagged. |
| 7. Apply curves, reconcile or withhold | Numeric per building and pathway; above 255 mph, contents and unknown inputs withhold or fail. |

Outcome: complete at screening grade with T4 links stated (costs, spread, onset, straight-line transfer).

## 12. Derivation rationale

The EF scale says at what gust each kind of damage appears for each building type; FEMA's damage states say what
each kind of damage costs as a share of the building. Combining them gives an expected repair cost per gust for the
tornado pathway. Straight-line wind uses the same building response, because the envelope and frame resist the same
gust load, but starts at 96 mph: below that, frequent ordinary storm gusts would otherwise accumulate damage that
FEMA's loss records do not show (§13).

## 13. NRI check

Order-of-magnitude check of yearly building loss on Hazard's grid against FEMA's National Risk Index, Dec 2025
([results](NRI_CHECK_convective_wind_real_estate__model_v0_1__docs_r1.csv),
[receipt](NRI_CHECK_RECEIPT_convective_wind_real_estate__model_v0_1__docs_r1.json); script
`convective_wind_real_estate_nri_check.py`). Median cell, % of building value per year:

| Building | Straight-line, proposal (×NRI) | Straight-line, no onset (×NRI) | Straight-line, onset at 90% of local design gust (×NRI) | Tornado (×NRI) |
|---|---|---|---|---|
| House | 0.029% (27×) | 0.537% (500×) | 0.029% (29×) | 0.0006% (0.17×) |
| Warehouse | 0.037% (35×) | 0.488% (453×) | 0.036% (36×) | 0.0009% (0.26×) |
| Office | 0.014% (13×) | 0.400% (371×) | 0.013% (13×) | 0.0004% (0.11×) |

NRI medians: straight-line 0.0011%, tornado 0.0036% per year. Rank correlation with NRI: about 0.5 for straight-line
and 0.91 for tornado.

What it means:

- The onset removes 92–97% of the straight-line loss, mostly damage from gusts under 96 mph; Hazard counts 0.66
  straight-line events a year at or above 58 mph in the median cell. The fixed onset and a location-specific one give the same
  national result.
- Straight-line loss stays 13–35 times NRI. Likely contributors, not tuned: Hazard's straight-line frequency is
  extrapolated below the ASCE 10-year gust; ASCE maps near the coast include hurricane winds; NRI counts reported
  losses for all buildings in a county; the EF transfer may be conservative (D-CWRE-10).
- Tornado loss is 0.11–0.26 times NRI with the ranking almost identical; the gap is in Hazard's hit geometry
  (national median path sizes, e.g. an EF1 path of 2.4 km × 55 m), not the curve.

## 14. Capability and fail-closed decision

Conditional scalar damage ratio per pathway and building; scenario dollars, annual and tail metrics withheld
(consumer-owned); contents withheld; above-range withheld; unknown pathway, building, unit or a missing/invalid gust
fail closed. Promotion gate blocked.

## 15. Open seams and update triggers

- Foundation-shift cost: Extensive (50%) kept for now (JL, D-CWRE-07); repair-cost evidence by EF degree would settle it.
- A design gust per cell from Hazard would allow a location-specific onset.
- Hazard-side: straight-line frequency below the ASCE 10-year gust; tornado path geometry; ASCE/hurricane overlap.
- The reviewer may prefer the hurricane-reuse route (D-CWRE-03).
- Contents.

## 16. Validation/QC

[Validation report](VALIDATION_REPORT_convective_wind_real_estate__model_v0_1__docs_r1.md): validator, hand checks
and the Hazard loader probe.
