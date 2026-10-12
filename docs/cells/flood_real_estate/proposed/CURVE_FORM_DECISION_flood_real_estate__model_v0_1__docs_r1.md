<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
scope: Step 5 (derive the response) for flood × real estate — the six proposed curve records, how values between published depths are computed, behaviour outside the published range, and the evidence for choosing straight lines over smooth fits.
-->

# Curve records and form — flood_real_estate model v0.1 / docs r1

Exact ordinates: [CURVE_ORDINATES](CURVE_ORDINATES_flood_real_estate__model_v0_1__docs_r1.csv) (177 rows).
Comparison metrics: [FORM_COMPARISON](FORM_COMPARISON_flood_real_estate__model_v0_1__docs_r1.csv).
Chart: [candidate curves](../previews/flood_real_estate_v0_1_candidate_curves.png).
Reproduce: `python scripts/reference_helpers/flood_real_estate_form_comparison.py <haz_fl_dept.csv> <out_dir>`
(reproduces the committed comparison CSV byte for byte).

## 1. The six proposed curve records

| curve_id | Reference building | Water type | Source | Published depths | Bands |
|---|---|---|---|---|---|
| `FRE_RES_FRESH_HAZUS_DF129` | `RE_RES_SFD_1S_SLAB` | freshwater | Hazus DF 129 (USACE-IWR) | −4 to 24 ft, every 1 ft | point only |
| `FRE_COM_FRESH_HAZUS_DF217` | `RE_COM_LOWRISE` | freshwater | Hazus DF 217 (Galveston, average retail) | −4 to 24 ft, every 1 ft | point only |
| `FRE_IND_FRESH_HAZUS_DF341` | `RE_IND_WAREHOUSE` | freshwater | Hazus DF 341 (Galveston, average wholesale) | −4 to 24 ft, every 1 ft | point only |
| `FRE_RES_COAST_NACCS_5A` | `RE_RES_SFD_1S_SLAB` | coastal surge | NACCS 5A (`RES1-1SNB`), Table 56 | −1, −0.5, 0, 0.5, 1, 2, 3, 5, 7, 10 ft | ML point; Min, Max bounds |
| `FRE_COM_COAST_NACCS_P2` | `RE_COM_LOWRISE` | coastal surge | NACCS Prototype 2 (`COM-ENG`), Table 25 | same ten depths | ML point; Min, Max bounds |
| `FRE_IND_COAST_NACCS_P3` | `RE_IND_WAREHOUSE` | coastal surge | NACCS Prototype 3 (`COM-PRE`), Table 35 | same ten depths | ML point; Min, Max bounds |

Axis: depth of water above the first finished floor, in feet. Output: damage as % of structure replacement cost.

## 2. Between published depths: straight lines

**Proposed (D-FRE-20): straight lines between published points.** Every published value is reproduced
exactly, and nothing is added between points that a source did not publish.

The Plymouth trial's fit catalogue was reproduced on all nine curves (six records, plus NACCS Min and Max).
LOOCV = leave-one-out error: hide one published point, rebuild the curve, measure the miss.

| Record (point curve) | LOOCV, straight lines | LOOCV, PCHIP | LOOCV, best smooth fit | Best smooth fit misses a published value by up to |
|---|---:|---:|---:|---:|
| House, freshwater (DF 129) | 0.85 | 0.57 | 0.91 (Weibull) | 2.7 pts |
| Commercial, freshwater (DF 217) | 0.84 | 0.65 | 1.51 (Richards) | 4.1 pts |
| Warehouse, freshwater (DF 341) | 0.64 | 0.65 | 0.97 (Richards) | 2.0 pts |
| House, coastal (NACCS 5A ML) | 2.38 | 2.01 | 3.41 (Weibull) | 4.6 pts |
| Commercial, coastal (NACCS P2 ML) | 3.21 | 3.45 | 3.69 (Weibull) | 5.2 pts |
| Warehouse, coastal (NACCS P3 ML) | 2.02 | 1.54 | 2.17 (Weibull) | 2.4 pts |

Units: damage percentage points. All forms pass the monotone and range checks on these six curves.

What the comparison shows:

1. **On every point curve, the best smooth fit predicts held-out points worse than straight lines**, and it
   moves published values by 2 to 5 points. On the NACCS bands it misses by up to 10 points (house Max).
2. **The Plymouth catalogue's own 10% rule** (adopt a smooth fit only if it beats the better straight-line form
   by at least 10%) picks a smooth fit for **none** of the six point curves; it does so only for two NACCS
   bounds (commercial Min, warehouse Max).
3. **PCHIP** (a smooth curve forced through every point) scores slightly better than straight lines on four of
   the six curves, by 0.2 to 0.5 points. That is small against the gap between libraries (more than 20 points
   at 4 ft; pressure test §3).

Why straight lines over PCHIP or a smooth formula:

```text
- reproduces every published value and invents no shape between points;
- matches how the source applies its own curves: Hazus estimates percent damage by interpolating "from the 1-foot
  depth increments shown in the Damage Function Library" (Hazus Flood Technical Manual 6.1 section 7.4 and
  section 8.4.1; same wording in 5.1 and, for essential facilities, 7.0); FEMA fits no formula. The manuals say
  "interpolated", not "linear", so straight lines are our reading of that practice. NACCS publishes tables and
  point-to-point charts and gives no interpolation rule;
- follows the method rule "choose the simplest form the evidence yields; don't manufacture a form the evidence
  can't support" (method/foundations/questions/04 §5); standard 06 lists an empirical lookup table as a
  source-native form;
- simplest for known-answer tests and for any consumer to reproduce.
```

How other cells choose (current artifacts, 2026-10-11). Curves taken from **published tables** use straight lines:
`flood_solar`, `flood_wind`, `wildfire_solar`, `wildfire_wind`. Curves **built by the team from scattered
evidence or fitted from a paper** use smooth forms: `hail_solar` (logistic), `strong_wind_solar` and
`wind_tornado_wind` (logistic variants), `tropical_cyclone_wind_wind` (Weibull), `tropical_cyclone_wind_solar`
(damage-state lognormal). The method doc calls the smooth sigmoid the "default working form" for derived
curves; these flood curves are adopted tables, so they sit with the first group.

Doc 06 (Hazard) refers to a "06-25 rule" making the anchored logistic the default. It was not found in this
repository; Hazard mentions of the anchored logistic are mostly archived or legacy. Owner to confirm whether it
applies.

The Plymouth trial (v0.4 onward) used the best smooth fit for every curve. That was a choice for an 11-building
submission; for a library curve, the catalogue's own evidence favours the published points.

## 3. Outside the published depths

| Water depth relative to the first floor | Result | Reason |
|---|---|---|
| Below the lowest published depth (Hazus −4 ft, NACCS −1 ft) | 0% | Every record is already 0% there; the water is below the level where the source records damage |
| Within the published range | Straight line between the two nearest published points | D-FRE-20 |
| Above the highest published depth (Hazus 24 ft, NACCS 10 ft) | Withheld, with a reason code | No extrapolation and no clamp, as in `flood_wind` (D-FRE-21) |
| Water type unknown | Withheld | D-FRE-05 |

The NACCS 10 ft ceiling matters for deep coastal surge; deeper water returns "withheld", not a number.

## 4. What is not decided here

```text
- reference-building attribute table and the $/m² value basis       step 6
- curve artifact JSON, capability declaration, known-answer tests   step 7
```
