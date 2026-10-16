<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-11
updated: 2026-10-16
status: draft
scope: Step 6 (connect value) for flood × real estate — the stated assumptions of each reference building, the first-floor-height choice, the value link, and the open options for a replacement cost per floor area.
-->

# Reference buildings and value link — flood_real_estate model v0.1 / docs r1

> **Model v0.2 note (2026-10-16):** this step document describes model v0.1. In model v0.2 the house, the
> warehouse and the new three-storey office use their FEMA Hazus record for coastal surge as well as freshwater
> (D-FRE-28; office DF 431, D-FRE-27); NACCS remains only for the retail record. See the
> [v0.2 dossier](flood_real_estate_curve_derivation_dossier__model_v0_2__docs_r1.md).

OSM supplies location and footprint, and rarely anything about construction (doc 06 §2). Every attribute below is
therefore an **assumption of the reference building**, stated once here and never presented as an observation.
Evidence: [NSI sample](NSI_SAMPLE_flood_real_estate__model_v0_1__docs_r1.csv) (FRE-S011),
[value crosswalk](VALUE_CROSSWALK_flood_real_estate__model_v0_1__docs_r1.csv),
[seven-step audit](SEVEN_STEP_AUDIT_flood_real_estate__model_v0_1__docs_r1.md).

## 1. Assumption table

| Attribute | `RE_RES_SFD_1S_SLAB` (house) | `RE_COM_LOWRISE` (commercial) | `RE_IND_WAREHOUSE` (warehouse) | Source |
|---|---|---|---|---|
| Platform type | Residential | Commercial | Industrial | doc 06 §3 |
| Hazus occupancy used by the curve | RES1 | COM1 (retail) | COM2 (wholesale / warehouse) | D-FRE-10, -16, -17 |
| NACCS prototype used by the curve | 5A | 2 (engineered) | 3 (non/pre-engineered) | D-FRE-14 |
| Stories | 1 | 1–3 (curves do not distinguish) | 1 | reviewer 2026-10-05; Hazus COM defaults cover low, mid and high rise |
| Foundation | slab-on-grade | slab-on-grade | slab-on-grade | reviewer; NACCS prototypes |
| Basement | none | none | none | reviewer |
| **First-floor height above grade** | **0.75 ft** | **0.25 ft** | **0.25 ft** | NSI 2026 defaults (§2) |
| Structure | wood frame | masonry or steel frame (NACCS 2: steel frame, precast infill) | pre-engineered steel frame | reviewer; NACCS |
| Roof cover | asphalt shingle | low-slope membrane | low-slope membrane or metal | reviewer (not used by flood curves; kept for hail and wind) |
| Opening protection | none | none | none | baseline, so shutters can be a later measure |
| Age / condition | not fixed; NACCS 5A "most likely" is 15–30 years, fair to good | not fixed | not fixed | NACCS (curve applicability only) |
| Floor area | not fixed by the curve; enters the value only | same | same | doc 06 §4 |

Roof cover and opening protection do not change any flood curve. They are recorded here so the same reference
buildings carry into the hail and wind cells unchanged.

## 2. First-floor height

The first-floor height turns water depth above grade into depth above the floor, which is what both libraries
read. It is one property of the building, so it is the same for freshwater and coastal water.

| Reference building | NACCS prototype (most likely) | NSI 2022 documentation | **NSI 2026 documentation and data** |
|---|---|---|---|
| House, slab | 1.0 ft | 0.5 ft | **0.75 ft** (documented; every slab RES1-1SNB record in three counties) |
| Commercial, slab | 0 ft | not stated | **0.25 ft** (not documented; 91–100% of slab COM1 / COM4 records in three counties) |
| Warehouse, slab | 1.0 ft | not stated | **0.25 ft** (not documented; ≥ 99.6% of slab COM2 / IND2 records in three counties) |

**Proposed (D-FRE-22): NSI 2026 defaults.** They are national, current (NSI 2026 Base), and based on a 2021 USACE
survey of first-floor heights ("generally align with median survey values"). The NACCS values describe the North
Atlantic prototype that each NACCS curve was built for. This supersedes D-FRE-15 (NACCS heights), which was written
before the NSI 2026 documentation was read.

What the change does at 2 ft of water above grade:

| Building | Depth above floor (NACCS FFH → NSI FFH) | Freshwater damage | Coastal (NACCS ML) damage |
|---|---|---|---|
| House | 1.0 → 1.25 ft | 23.0% → 25.2% | 18.0% → 20.5% |
| Commercial | 2.0 → 1.75 ft | 14.0% → 12.8% | 30.0% → 27.5% |
| Warehouse | 1.0 → 1.75 ft | 5.0% → 7.2% | 20.0% → 26.0% |

(Straight lines between published points, from the curve ordinates file.)

The warehouse is the most sensitive: 0.75 ft lower floor raises coastal damage at this depth by six points.

Notes:

```text
- NSI states only the residential defaults; the commercial and industrial 0.25 ft is read from NSI records
  (three counties, Massachusetts, Louisiana and Iowa) and is tier T3 until documented.
- Hazus rounds first-floor height to the nearest whole foot in its own runs (Hazus 6.1 TM §7.4). This cell
  uses the stated height without rounding.
- First-floor height is the main site condition for flood. Elevating a building later is a change to this one
  number (doc 06 resiliency ask).
```

## 3. Value link

```text
loss = DR(reference building, water type, depth above floor) × structure replacement cost new
```

- **Denominator:** replacement cost new of the structure. Excludes land, contents, site works and depreciation;
  not market or assessed value. This is the basis of both libraries (FRE-C001).
- **Allocation:** the single failure unit carries 100% of the structure replacement cost new. There is no
  sub-allocation at whole-building grain, and no fieldwork or support line to allocate.
- **NSI matches the denominator only through `fullrep`:** NSI `val_struct` is depreciated (NSI 2026: 1% per year
  for 20 years, then held at 80%) and must not be used.

## 4. Replacement cost per floor area — open

Scenario dollars need a cost per floor area for each reference building. **No source is selected in v0.1**
(`value_per_area` stays an open seam; scenario dollars withheld). Options:

| Option | What it is | Fit to the denominator | Limits |
|---|---|---|---|
| A. NSI 2026 `fullrep` | Replacement cost new by occupancy × floor area; national cost curve adjusted for local construction wages; RES1 also adjusted by tract income; August 2025 prices; cost per area falls with building size | Matches (not depreciated) | The national cost curve itself is not published in the documentation; values must be read from records |
| B. Hazus 7.0 Inventory Technical Manual | FEMA replacement cost per area by occupancy, used by Hazus | Matches (replacement cost) | Not yet read; the FEMA site needs a manual download |
| C. RSMeans | Commercial construction cost data | Matches | Licensed; cannot be redistributed |
| D. Team reference values | e.g. the $12M teaching warehouse in the 10-01 asset-modelling deck | Unknown basis | Not sourced; would need its own basis check |

For scale only, NSI `fullrep` per square foot in the three sampled counties (median over all records of the
occupancy; county wage levels differ):

| Occupancy | Nantucket MA | Plaquemines LA | Black Hawk IA |
|---|---:|---:|---:|
| RES1-1SNB (house) | $227 | $177 | $181 |
| COM1 (retail) | $218 | $191 | $195 |
| COM4 (office) | $312 | $270 | $293 |
| COM2 (warehouse) | $169 | $152 | $150 |
| IND2 (light industrial) | $224 | $189 | $196 |

These are illustrations, not a value basis. A basis needs a stated geography rule (national, or by county), a
reference floor area per building (cost per area depends on size), and a price year.
