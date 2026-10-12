<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-11
status: draft
scope: Step 3 (research and extract evidence) for flood × real estate — where each candidate curve comes from, how far the working copies were checked against originals or independent copies, and what the checks changed.
-->

# Source verification — flood_real_estate model v0.1 / docs r1

Registers: [sources](SOURCE_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv) (FRE-S001–S009) ·
[claims](CLAIM_PARAMETER_REGISTER_flood_real_estate__model_v0_1__docs_r1.csv) (FRE-C001–C012).

## 1. Chain of copies

The working tables (Plymouth branch and GCS) are byte-identical to the Zenodo compilation (FRE-S001). That
compilation is itself secondary:

```text
Hazus 5.1 software DDF library ──► CRAN `hazus` R package ──► Pollack 2023 (haz_fl_dept.csv) ──► Plymouth / GCS
Hazus 5.1 Technical Manual Table 5-2 ──(hand copy)──► Pollack 2023 (riverine_ids.csv)
NACCS 2015 report tables ──(hand coded)──► Pollack 2023 (naccs_ddfs.csv)
```

Every value was therefore checked against an original or an independent copy where one could be reached.

## 2. What was checked

| Check | Against | Result |
|---|---|---|
| NACCS inundation-structure knots for 5A, Prototype 2 and Prototype 3 (Min / ML / Max) | Report Tables 56, 25, 35 (FRE-S004) | **90 of 90 values match** (FRE-C005) |
| NACCS values at 4, 6, 8, 9 ft | Report | **Not published.** The compiled file repeats the previous knot, which understates damage between knots (FRE-C006). Only the ten published knots are used. |
| Hazus DF 217, 431, 341, 559 | USACE `go-consequences` HEC-FIA Galveston curves (FRE-S005), an independent distribution | **Identical at every depth** (29, 29, 29 and 26 points; FRE-C003) |
| Hazus DF 129 | USACE EGM curve in `go-consequences` (FRE-S006) | Equals the **rounded EGM means** from −2 to +16 ft; EGM also gives a standard deviation per depth (FRE-C004) |
| Hazus default list (Table 5-2) | Hazus Flood Technical Manual 5.1, 6.1 and 7.0 (FRE-S002; downloaded manually) | **Identical in all three editions** for every type we use: DF 129, 217, 431, 341, 559 (and 209 for hotels). Pollack's copy is correct and still current; cite Hazus 7.0 (FRE-C002). |
| Hazus coastal defaults (Tables 5-3, 5-4) | Hazus 7.0 | Only RES1 (and RES2, RES3A) have coastal-specific curves; commercial and industrial use the riverine defaults for coastal water. The coastal house default is DF 658 (BCAR 2011), which is **not in our working copy** (FRE-C013, FRE-C014). |
| NSI first-floor-height defaults | NSI technical documentation (FRE-S009) | **Pending.** Not yet accessed. |

## 3. What the checks changed

1. **The NACCS knot set is the ten published depths only:** −1, −0.5, 0, 0.5, 1, 2, 3, 5, 7, 10 ft. Values in
   between come from the step-5 form decision, never from the compiled file.
2. **The coastal curve for the commercial reference building is `COM-ENG`, not `COM-PRE`.** NACCS Prototype 2
   (Commercial Engineered) is steel frame with precast infill on a slab, finished floor at grade, which matches a
   steel-framed low-rise commercial building. Prototype 3 (Non/Pre-Engineered) is a one-story steel or light-metal
   building on a slab with the finished floor 1 ft above grade, which matches the warehouse (FRE-C008). If the
   commercial reference building is defined as masonry, Prototype 3 is closer.
3. **Sourced first-floor-height defaults now exist for two buildings:**

   | Reference building | NACCS prototype (most likely) | First-floor height |
   |---|---|---|
   | `RE_RES_SFD_1S_SLAB` | 5A: 1 story, wood frame, slab, 15–30 years | **1 ft** (Table 55) |
   | `RE_IND_WAREHOUSE` | 3: 1 story, steel or light metal, slab | **1 ft** (Table 34) |
   | `RE_COM_LOWRISE` | 2: 2 stories, steel frame, precast infill, slab | **0 ft** (Table 24) |

   NACCS 5A is an exact description of the reviewer's reference house. These remain reference-building assumptions,
   cross-checked later against NSI.
4. **A known low-bias warning for the house.** NACCS reports that its no-basement residential inundation curves
   (5A, 5B) came out **lower than FEMA substantial-damage estimates** in its own verification, and advises users
   to review that before selecting them (FRE-C009). Recorded as a caveat for coastal results on the house.
5. **Regional limit for commercial and industrial freshwater curves.** DF 217, 431, 341 and 559 are class
   averages from one USACE district (Galveston) (FRE-C011).
6. **The freshwater defaults are confirmed and current.** Table 5-2 is unchanged from Hazus 5.1 to 7.0 for all
   our building types.
7. **The coastal choice (D-FRE-05) is now an open step-4 question.** FEMA's own coastal position differs from our
   proposal:

   | Reference building | Our proposal (coastal surge) | FEMA Hazus 7.0 coastal default |
   |---|---|---|
   | House | NACCS `RES1-1SNB` (inundation only) | DF 658, BCAR 2011, coastal A or V, built assuming waves ≥ 1.5 ft destroy walls; not in our data |
   | Commercial | NACCS `COM-ENG` | Same as riverine: DF 217 / 431 |
   | Warehouse | NACCS `COM-PRE` | Same as riverine: DF 559 / 341 |

   FEMA also states that well-documented coastal curves exist only for single-family homes. NACCS is the only
   source in hand with commercial coastal inundation curves; DF 658 may already include wave effects that this
   cell keeps in the deferred wave pathway.

## 4. Still open for step 3

```text
- NSI foundation-height defaults (FRE-S009)
- identify the exact EGM document behind DF 129 (likely EGM 01-03)
- DF 658 ordinates, only if step 4 selects the FEMA coastal house default
```

None of these blocks step 4. Each is recorded as `pending` or `defer` in the registers.
