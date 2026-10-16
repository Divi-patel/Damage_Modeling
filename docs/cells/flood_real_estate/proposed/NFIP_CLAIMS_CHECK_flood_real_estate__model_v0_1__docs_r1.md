<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# NFIP claims check — flood_real_estate model v0.1 / docs r1

A comparison of the proposed curves with paid NFIP flood claims for buildings like the three reference
buildings. **It is a check, not a calibration: no curve, record or decision changes here.** It fills the
"calibration against observed losses" item left open in the
[validation report §5](VALIDATION_REPORT_flood_real_estate__model_v0_1__docs_r1.md) and is the evidence named by the
revisit trigger of D-FRE-18 (coastal source) in the [decision log](DECISION_LOG_flood_real_estate__model_v0_1__docs_r1.md).
The coastal decision itself stays open.

## 1. Data

Source FRE-S012: OpenFEMA NFIP Redacted Claims, `NfipClaims` v3, retrieved 2026-10-16 by
[`flood_real_estate_nfip_claims_check.py`](../../../../scripts/reference_helpers/flood_real_estate_nfip_claims_check.py).
Filters, record counts and checksums: [pull manifest](NFIP_CLAIMS_PULL_MANIFEST_flood_real_estate__model_v0_1__docs_r1.json).

| Pull | Filter (all: one floor, slab foundation, exterior water depth > 0) | Records |
|---|---|---|
| house | single-family (occupancy 1 or 11), building damage > 0 | 95,435 |
| non-residential | occupancy 4, 6 or 18, building damage > 0 | 10,180 |
| house, zero damage | single-family, building damage = 0 (sensitivity only) | 1,006 |

Nearly all records with an exterior water depth are losses from 2016 on (all but 103), so the sample is
effectively 2016–2026. It is concentrated on the Gulf coast: **95% of the house claims are from TX, LA, MS, AL
or FL (59% Florida) and 0.7% from the Northeast**, where NACCS was developed.

## 2. Method

| Step | Rule |
|---|---|
| Analogue | House: single-family, building description 1 or blank → `RE_RES_SFD_1S_SLAB`. Commercial: occupancy 6 or 18, description 1, 8 or blank → `RE_COM_LOWRISE` (retail record). Warehouse: description 5 → `RE_IND_WAREHOUSE` |
| Water type | Cause of damage 1 (tidal overflow) → coastal surge; 2 (river overflow) or 4 (rainfall) → freshwater. V zones excluded: the still-water curves do not cover wave damage (D-FRE-06) |
| Damage ratio | building damage amount / building replacement cost, clipped to 0–1; claims without a replacement cost dropped |
| Depth | exterior depth above grade (inches) / 12, minus the reference first-floor height (0.75 / 0.25 / 0.25 ft) |
| Comparison | claims mean vs the curve evaluated at each claim's depth, averaged over the same claims, per depth band; bands with fewer than 20 claims dropped |

67,241 claims fall in the reported bands ([band table](NFIP_CLAIMS_COMPARISON_flood_real_estate__model_v0_1__docs_r1.csv),
[sensitivity table](NFIP_CLAIMS_SENSITIVITY_flood_real_estate__model_v0_1__docs_r1.csv),
[chart](../previews/flood_real_estate_v0_1_nfip_claims_check.png)).

## 3. Results

Curve minus claims mean, in damage-ratio points (negative = curve below claims):

| Analogue, water | 0–0.5 ft | 0.5–1 | 1–2 | 2–3 | 3–4 | 4–5 | 5–6 | Claims |
|---|---|---|---|---|---|---|---|---|
| House, freshwater (FEMA DF 129) | −11 | −12 | −9 | −5 | −1 | +1 | +5 | 42,527 |
| House, coastal (NACCS 5A) | **−23** | **−18** | **−13** | −8 | −6 | −5 | −4 | 17,462 |
| House, coastal, *if FEMA DF 129 were used* | −12 | −11 | −8 | −2 | +2 | +5 | +6 | same |
| Commercial, freshwater (FEMA DF 217) | −6 | −5 | −3 | −3 | −3 | −2 | −3 | 5,753 |
| Commercial, coastal (NACCS prototype 2) | −3 | 0 | **+6** | **+10** | **+11** | **+12** | **+11** | 1,134 |
| Commercial, coastal, *if FEMA DF 217 were used* | −8 | −8 | −7 | −7 | −8 | −8 | −10 | same |
| Warehouse, freshwater (FEMA DF 341) | −8 | −6 | −2 | −2 | | | | 365 |

1. **Freshwater curves are reasonable.** The house is within about 5 points at 2–6 ft and commercial within about
   6 points at 0–10 ft (FRE-C026). All three sit below the claims at the shallowest depths.
2. **NACCS understates the coastal house** by 12–23 points in the first 2 ft, where 72% of the coastal house claims
   fall; the claims sit near the NACCS upper bound (FRE-C027).
3. **NACCS overstates coastal commercial** by 6–12 points from 1 ft up (FRE-C028).
4. **FEMA curves on the coastal claims** (FRE-C029): closer than NACCS for the house; for commercial about as far
   from the claims as NACCS, on the other side (below rather than above).
5. **Coastal vs freshwater claims** (FRE-C030): for the house analogue they match at the same depth (within 5
   points); for the commercial analogue coastal claims run 2–11 points higher.
6. **Warehouse:** 365 freshwater claims, all under 3 ft, and too few coastal claims (25) to compare.

## 4. Sensitivity (house)

| Variant | Effect on the claims mean |
|---|---|
| Add the 1,006 zero-damage claims | under 1 point |
| Settled at replacement cost only / actual cash value only | up to 2 points either way |
| First-floor height 0 / 0.25 / 0.75 / 1 ft, claims 0.5–2.0 ft above grade (freshwater) | curve −3 / −6 / −10 / −13 points vs claims |

The shallow-depth gap is mostly a floor-height question (FRE-C031): with the floor at grade, the freshwater
curve is within 3 points of the claims. The reference 0.75 ft is an NSI default, not an observation, and NFIP does
not report each building's floor height in this dataset. Under-representation of buildings that flooded without
a claim cannot be tested from claims data.

## 5. Limits

- Claims are insured, paid losses for buildings that resemble the references; they are not the reference
  buildings. The commercial analogue is a mix of one-floor business occupancies, not the three-story office target.
- Building damage is the adjuster's assessed amount for the claim and replacement cost is the policy's value; neither
  is exactly replacement-cost-new repair cost.
- The sample is mostly Florida, Texas and Louisiana. It cannot test NACCS in its own region (North Atlantic).
- The comparison is by band means, not claim-by-claim fit; no curve is refit to it.

## 6. Reproduce

```bash
python scripts/reference_helpers/flood_real_estate_nfip_claims_check.py fetch
python scripts/reference_helpers/flood_real_estate_nfip_claims_check.py compare
```

`fetch` downloads about 60 MB into the gitignored `build/nfip_claims/`; `compare` rewrites the two CSVs, the
manifest and the chart. A rerun on 2026-10-16 reproduced the 2026-10-12 exploratory run exactly (same record counts
and band values). A newer pull will change counts as FEMA adds claims.
