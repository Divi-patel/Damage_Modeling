<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
scope: Step 4 (judge evidence) for flood × real estate — what each verified candidate curve can and cannot support for each reference building and water type, the three open curve choices, cross-source consistency, and what stays withheld.
-->

# Evidence pressure test — flood_real_estate model v0.1 / docs r1

Inputs: [source verification](SOURCE_VERIFICATION_flood_real_estate__model_v0_1__docs_r1.md),
[source register](SOURCE_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv),
[claim register](CLAIM_PARAMETER_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv). Parameter tiers:
[PARAMETER_TIER_TABLE](PARAMETER_TIER_TABLE_flood_real_estate__model_v0_1__docs_r1.csv).

All selections below are **proposed** (JL, 2026-10-11) and need owner review before any curve record is
promoted.

## 1. The chain each curve must support

```text
water level at the building
  -> depth above the first finished floor          (axis bridge: depth above grade − first-floor height)
  -> whole-building structure damage ratio          (published depth-damage ordinate)
  -> × structure replacement cost new               (value link, step 6)
```

| Link | Freshwater (Hazus defaults) | Coastal surge (NACCS) |
|---|---|---|
| Axis: depth above first finished floor | Supported (FRE-C001) | Supported (FRE-C001) |
| Ordinate: % of structure value | Supported; verified against two independent chains (FRE-C002–C004) | Supported; 90/90 published knots verified (FRE-C005) |
| Reference-building match | By Hazus occupancy and stories / basement | By NACCS prototype description (FRE-C007, C008) |
| First-floor height | Not given by Hazus; NSI 2026 defaults (D-FRE-22, step 6; replaces D-FRE-15) | NSI 2026 defaults; the prototype height is the recorded alternative |
| Value denominator | Structure replacement value (Hazus convention) | Structure value (NACCS convention) |
| Calibration to observed losses | None verified (class averages; EGM lineage for the house) | Expert panel; own verification found 5A low against FEMA estimates (FRE-C009) |

No load-bearing link is missing for either water type. The chain is complete at **screening grade**:
published, expert- or class-based curves for a reference building, not calibrated to observed losses for that
building.

## 2. The three open choices

### A. Commercial, freshwater — DF 217 (retail) or DF 431 (office)?

| | DF 217 — COM1 "Average of 47 Retail classes" | DF 431 — COM4 "Average prof/tech services" |
|---|---|---|
| Damage at 1 / 4 / 8 ft | 9% / 18% / 30% | 11% / 28% / 44% |
| Breadth | Average of 47 classes | Average of one class group |
| Fit to the reference building | "small low-rise retail **or** office" (reviewer); retail listed first | Same |

**Proposed: DF 217 (retail).** The reference building must have one occupancy so the curve and the value basis
match. Retail is listed first in the reviewer's definition, and DF 217 averages the widest set of classes. Office (DF 431)
becomes a second commercial profile later, alongside the "more profiles" path in doc 06 (D-FRE-16).

### B. Warehouse, freshwater — DF 341 (wholesale / warehouse) or DF 559 (light industrial)?

| | DF 341 — COM2 "Average of 22 wholesale/warehouse classes" | DF 559 — IND2 "Average of 14 Light Industrial classes" |
|---|---|---|
| Damage at 1 / 4 / 8 ft | 5% / 13% / 25% | 9% / 22% / 35% |
| Fit to the reference building | Warehouse use: the 10-01 deck's warehouse | Light manufacturing |

**Proposed: DF 341 (wholesale / warehouse).** The reference building is a warehouse, and Hazus files warehouses
under COM2; the platform's "Industrial" label does not change the occupancy (D-FRE-10). Light industrial (DF 559)
becomes a second industrial profile later (D-FRE-17).

### C. Coastal surge — NACCS, or FEMA's coastal defaults?

| | NACCS 2015 (current proposal) | FEMA Hazus 7.0 coastal defaults |
|---|---|---|
| House | `RES1-1SNB`, inundation only, Min / ML / Max; about 38% at 4 ft | DF 658 (BCAR 2011), coastal A and V, assumes waves ≥ 1.5 ft destroy walls; 12% at the floor, 50% at 2 ft, **100% from 4 ft** (FRE-C020) |
| Commercial / warehouse | `COM-ENG` / `COM-PRE`, inundation only | Same as freshwater (DF 217 / DF 341); FEMA states no well-documented coastal curve exists |
| Fit to our pathway split | Still water only; NACCS publishes wave and erosion tables separately | DF 658 likely mixes wave damage into the still-water curve |
| Data in hand | Yes, verified | Yes since 2026-10-11, from the Hazus 6.1 extract (FRE-S010); the extract's 550 shared curves match exactly (FRE-C018) |
| Geography | North Atlantic coast (expert panel) | National default |

**Proposed: keep NACCS for coastal surge (D-FRE-18).** It is the only source in hand with coastal curves for all
three buildings, it keeps waves out of the still-water pathway, and its data is verified. DF 658's shape (total loss
from 4 ft) is a wave-zone curve; placing it in the still-water pathway would count wave damage that this cell defers. Two limits travel with
it: it was built for the North Atlantic coast, and its own verification found the no-basement house curve low.
FEMA's position stays recorded as the alternative (FRE-C013).

## 3. Cross-source consistency check

At 4 ft above the first floor (NACCS values interpolated between its 3 ft and 5 ft knots):

| Reference building | Freshwater (proposed Hazus) | Coastal surge (NACCS ML; Min–Max) |
|---|---|---|
| House | 47% (DF 129) | 38% (25–53%) |
| Commercial | 18% (DF 217) | 38% (31–46%) |
| Warehouse | 13% (DF 341) | 40% (24–60%) |

Two findings:

1. **For the house, coastal reads lower than freshwater**, the opposite of what saltwater surge should do. This
   matches NACCS's own warning that its no-basement house curve is low against FEMA damage estimates (FRE-C009).
2. **For commercial and warehouse, the Galveston class averages read two to three times lower than NACCS.** The
   Hazus class curves for warehouses alone range from about 1% to 62% at 4 ft, so the low reading may reflect the
   Galveston source rather than freshwater physics (FRE-C011).

Neither finding breaks the chain; both say the two libraries were built differently and neither is calibrated
for these buildings. Consequences:

```text
- each record carries its library and water type; the two are never blended or averaged;
- the gap is a named open seam with an update trigger: a comparison against NFIP claims;
- no adjustment factor is applied now (an unreviewed uplift would be a second, unversioned model).
```

## 4. What stays withheld

```text
- unknown water type                 -> withhold (no fallback to either library)        D-FRE-05
- NACCS depths outside −1 to 10 ft    -> withhold (no extrapolation, no clamp)           step 5
- Hazus depths outside −4 to 24 ft    -> withhold                                          step 5
- NACCS values at unpublished depths  -> never used                                        D-FRE-13
- Min / Max as a probability spread   -> not offered (it is a building-variant band)       FRE-S004
- EGM standard deviation as spread    -> not offered in v0.1                               FRE-C004
- wave / velocity damage              -> deferred pathway                                  D-FRE-06
- mould / long duration (NACCS Max)   -> not a v0.1 conditioner                            FRE-C010
- scenario dollars                    -> withheld until the value basis exists             step 6
```

## 5. Verdict

The evidence supports a **screening-grade proposed curve set**: three reference buildings × two water types, six
curve records, all at tier T2 with stated transfer limits. Steps 5–7 can proceed. Promotion beyond `proposed`
needs owner acceptance of the three choices above and of the scope decisions (D-FRE-01 to D-FRE-18).
