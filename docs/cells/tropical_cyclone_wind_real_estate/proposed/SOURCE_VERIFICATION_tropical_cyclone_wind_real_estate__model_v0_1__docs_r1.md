<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-12
updated: 2026-10-12
status: draft
scope: Step 3 (research and extract evidence) for tropical-cyclone wind × real estate — where the candidate curves come from, how the working copy was checked against the manual and an independent copy, and what the checks changed.
-->

# Source verification — tropical_cyclone_wind_real_estate model v0.1 / docs r1

Registers: [sources](SOURCE_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv) (TCRE-S001–S009) ·
[claims](CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_real_estate__model_v0_1__docs_r1.csv) (TCRE-C001–C023).

## 1. Chain of copies

The Hazus hurricane manual describes the method but **does not print the loss tables**; they live only in the
Hazus software database. Two separate extractions of that database exist publicly:

```text
Hazus 6.1 software database ──(FEMA Hazus team export)──► HazusWindDamFunctions_Hazus61.xlsx ──► OS-Climate public mirror (TCRE-S002)
Hazus 5.1 software database ──(SimCenter extraction)──► DLML "Hazus Hurricane Methodology v5.1" loss_repair.csv (TCRE-S003)
Hazus 7.0 Hurricane Technical Manual (TCRE-S001) ── method, axis, mechanisms, building types, characteristic weights
```

The extract's sheet names (`huDamLossFun`, `huListOfWindBldgTypes`, `huTerrain` …) are the Hazus database table
names. The mirror's ETag equals the downloaded file's MD5, so the download is intact.

## 2. What was checked

| Check | Against | Result |
|---|---|---|
| Axis of the loss functions | Manual §4.3 p. 4-81; §5.5.1.3 p. 5-173; SimCenter `Demand-Type` | **Peak gust at 10 m in open terrain, mph** — the same quantity Hazard delivers (TCRE-C001, C020). |
| What the loss functions contain | Manual §2.1 p. 2-4; §6.1; §8.1.4.1 | **Wind pressure + windborne debris + rainwater penetration, combined.** Tree fall is a separate additive term for small residential buildings only (TCRE-C002, C003). |
| Denominator | Manual §8.1.2 p. 8-4; §8.1.7.2 p. 8-25 | Repair cost over **total building replacement cost**, capped at 100%; commercial losses include repair (1.25) and overhead-and-profit (1.20) factors (TCRE-C004). |
| Building-type definitions | Manual Table C-1, §9.1 | WSF1 = wood single-family 1 story; SECBL/MECBL = steel/masonry engineered commercial 1–2 stories; SPMBL = pre-engineered metal building > 50,000 ft² (TCRE-C006–C009). |
| Building-loss ordinates, all 1,840 curves of WSF1 (CONUS), SECBL, MECBL, SPMBL, SPMBM × 5 terrains × 41 speeds | SimCenter Hazus 5.1 copy (TCRE-S003) | **Identical, zero difference** (TCRE-C011). Also shows the functions did not change from Hazus 5.1 to 6.1. |
| Version currency (Hazus 7.0) | Manual §9.7 pp. 9-49 to 9-50 | The 6.1 and 7.0 hurricane updates were to the **mapping schemes** (49 regions, NSI-based weights), not the loss functions. The 7.0 database itself was not opened (TCRE-C012). |
| Default characteristic weights | Manual Table C-2 vs the extract's mapping sheets | The extract's mapping sheets carry the **12 old regions**; current weights come from the 7.0 manual (TCRE-C013). |
| Internal quality of the extract | All 30,580 building-loss rows | About half dip somewhere as wind rises (largest 0.10); 525 WSF1 values exceed 1.0 by ≤ 0.000052 — simulation noise (TCRE-C015). The 15 selected records are clean (TCRE-C014). |
| Metal-building family | Duplicate search + manual Tables 5-76/5-77 | **Anomaly:** the SPMB "superior deck" rows are copies of other size classes' rows. The selected warehouse row is unaffected and moves in the directions the manual reports (TCRE-C016, C017). |

## 3. What the checks changed

1. **The pathway includes debris and rain ingress** (D-TCRE-04 confirmed by TCRE-C002). In FEMA's words, the
   functions predict "the combined effects of wind pressure, windborne debris, and rainfall acting on a structure".
2. **Tree fall is deferred, not hidden.** For the house only, Hazus adds tree damage on top of the base curve,
   using tree height, type and density. The base record excludes it, so there is no double count (D-TCRE-13).
3. **Terrain becomes a required selector** with the five Hazus classes and no interpolation; the manual gives no
   rule for combining classes (TCRE-C005; D-TCRE-06 as decided by JL).
4. **The commercial frame question disappears.** SECBL and MECBL are numerically identical, so "masonry or steel"
   gives the same curve (TCRE-C007).
5. **The warehouse needs a floor-area assumption** (> 50,000 ft² for SPMBL), and the SPMB superior-deck rows are
   excluded from any future measure until FEMA explains them (TCRE-C008, C016; D-TCRE-16).
6. **Defaults come from the manual, not the extract** (TCRE-C013).

## 4. Candidate curves after verification (JL decisions, 2026-10-12)

| Reference building | Hazus type | Characteristics (most common, Table C-2) | wbID | Terrain records |
|---|---|---|---|---|
| `RE_RES_SFD_1S_SLAB` | WSF1 (CONUS) | gable roof · no secondary water resistance · 6d nails @ 6"/12" · toe-nailed roof-to-wall · no garage · no shutters · shingle | 6 | 5 (open … trees) |
| `RE_COM_LOWRISE` | SECBL (= MECBL) | built-up roof (BUR) · low window area · debris environment B (varies by direction) · standard metal deck · no shutters | 1812 | 5 |
| `RE_IND_WAREHOUSE` | SPMBL | old roof deck · standard metal deck · no shutters | 1729 | 5 |

Extraction and cross-check are reproducible:

```bash
python scripts/reference_helpers/extract_tropical_cyclone_wind_real_estate_hazus_ordinates.py \
    <HazusWindDamFunctions_Hazus61.xlsx> <simcenter loss_repair.csv>
```

## 5. Bounded search record

| Looked for | Where | Found |
|---|---|---|
| Printed Hazus hurricane loss tables | Hazus 7.0 TM full text (700 pp.) | None; method, figures and damage-state tables only |
| Independent copy of the loss functions | physrisk docs; NHERI SimCenter DLML (GitHub tree at `869423b`) | SimCenter Hazus 5.1 `original` dataset (used); SimCenter `coupled` dataset is a recalibration (not used) |
| Existing building or Hazus hurricane material in the library | Damage `main` @ `02eba9b` (all cells) | None |
| Legacy real-estate wind arrays | `hazard_analysis` local copy @ `9bc9c30` | Two arrays, rejected (TCRE-C023) |
| Rule for intermediate terrain roughness | Hazus 7.0 TM full-text search ("interpolat", roughness sections) | None stated |
