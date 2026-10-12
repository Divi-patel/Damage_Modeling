<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
scope: Step 6 (connect value) for tropical-cyclone wind × real estate — the wind attributes stated for each reference building, the terrain contract, how future resiliency measures map onto the same records, and the value link shared with flood_real_estate.
-->

# Reference buildings and value link — tropical_cyclone_wind_real_estate model v0.1 / docs r1

The three reference buildings are the ones defined in `flood_real_estate` (TCRE-S006), with the same IDs. This note
adds only what wind needs. Every attribute is an **assumption of the reference building**, never an observation
(OSM almost never tags roof or connection details; doc 06 §2).
Evidence: [variant sensitivity](VARIANT_SENSITIVITY_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
[value crosswalk](VALUE_CROSSWALK_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv),
[seven-step audit](SEVEN_STEP_AUDIT_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.md).

## 1. Wind attributes

| Attribute | `RE_RES_SFD_1S_SLAB` (house) | `RE_COM_LOWRISE` (commercial) | `RE_IND_WAREHOUSE` (warehouse) | Basis |
|---|---|---|---|---|
| Hazus building type | WSF1 (CONUS) | SECBL (identical to MECBL) | SPMBL | JL 2026-10-12; TCRE-C006–C008 |
| Stories / size used by the type | 1 story | 1–2 stories (a 3-story building would be SECBM) | **> 50,000 ft²** floor area | Hazus type definitions |
| Roof shape | gable | flat (implicit in type) | metal-building roof (implicit) | most common (Table C-2) |
| Roof cover | asphalt shingle | **BUR** (built-up membrane) | metal-building roof system | reference building; BUR is the most common Hazus membrane (TCRE-C022) |
| Secondary water resistance | no | — | — | most common |
| Roof-deck attachment | 6d nails @ 6"/12" | standard metal deck | standard metal deck | most common |
| Roof-deck age | — | — | old | most common |
| Roof-to-wall connection | toe-nail | — | — | most common |
| Garage door | none | — | — | most common |
| Window area | — | low | — | most common |
| Windborne-debris environment | (inside the WSF1 curve) | **B** — varies by direction | — | most common |
| Opening protection (shutters) | **none** | **none** | **none** | reference building (baseline for later measures) |
| Terrain | **required input** | **required input** | **required input** | JL 2026-10-12 (§2) |

"Most common" = the highest all-region average weight in Hazus 7.0 Table C-2 (TCRE-C010). Each value is a named
field in the curve record, so it can be read and later changed.

## 2. Terrain contract

The consumer must send one of five Hazus terrain classes for the building's location:

| `hazus_terrain_class` | Surface roughness z0 | Typical setting |
|---|---|---|
| `open` | 0.03 m | open fields, airports, waterfront |
| `light_suburban` | 0.15 m | scattered buildings |
| `suburban` | 0.35 m | typical suburb |
| `light_trees` | 0.70 m | suburb with many trees |
| `trees` | 1.00 m | wooded |

Rules:

```text
- no default: a missing terrain class is an error (TERRAIN_CLASS_REQUIRED); an unknown value is an error;
- no interpolation between classes in Damage (the source gives no rule; TCRE-C005);
- the gust stays the open-terrain gust: terrain is applied once, by choosing the record, never also by
  lowering the gust (Hazard applies no roughness today; TCRE-C020);
- mapping a site roughness to a class (Hazus uses NLCD land cover averaged by census tract, TM §4.3.4) is a
  consumer rule — an open seam for Hazard;
- open terrain is not a safe default for the commercial building: its light-suburban curve is higher (TCRE-C024).
```

## 3. Future resiliency measures (not built in v0.1)

Because the Hazus characteristics are explicit, a later measure is a change of one field to a value that already
exists in the source. Measured effects at 140 mph, open terrain (TCRE-C019):

| Building | Measure → field change | Building loss: reference → with measure |
|---|---|---|
| House | shutters (`shutters: no → yes`, garage none) | 77.9% → 47.7% |
| House | roof-to-wall straps (`toe-nail → strap`) | 77.9% → 72.4% |
| House | re-nail roof deck (`6d @ 6"/12" → 8d @ 6"/6"`) | 77.9% → 69.4% |
| House | secondary water resistance (`no → yes`) | 77.9% → 73.9% |
| House | all four together | 77.9% → 6.8% |
| Commercial | shutters | 31.3% → 12.7% |
| Warehouse | shutters | 88.2% → 35.1% |
| Warehouse | superior metal-deck attachment | **not usable** — source anomaly (TCRE-C016) |

v0.1 publishes only the reference values. A request that sends a different characteristic value is withheld
(`WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED`) rather than silently priced as the reference (D-TCRE-19).

## 4. Value link

```text
loss = DR(reference building, terrain class, gust) × structure replacement cost new
```

- **Denominator:** structure replacement cost new, identical to `flood_real_estate` (D-TCRE-09). The Hazus building
  loss ratio is defined over total building replacement cost and capped at 100% (TCRE-C004). The Hazus default
  residence value includes slab site preparation; that small boundary difference is recorded, not adjusted.
- **Allocation:** one failure unit, 100% of structure replacement cost new.
- **Per-area cost:** the same open seam as `flood_real_estate` (its reference-buildings note §4, options A–D). No
  source is selected; scenario dollars stay withheld.
- **Floor area matters twice for the warehouse:** it picks the Hazus size class (> 50,000 ft² → SPMBL) and it
  scales the dollars. When JL fixes the reference floor area, both must use the same number (D-TCRE-16).
- **Same building, two perils:** a storm can cause wind (this cell) and surge or rain flooding (`flood_real_estate`)
  on the same building. The consumer must keep the combined damage at or below 100% of structure value
  (D-TCRE-11); neither cell can do this alone.
