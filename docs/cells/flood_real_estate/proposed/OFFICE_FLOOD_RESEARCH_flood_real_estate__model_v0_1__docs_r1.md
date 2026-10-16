<!--
author: owner-directed (JL) · agent-drafted
created: 2026-10-16
updated: 2026-10-16
status: draft
-->

# Office flood research — flood_real_estate model v0.1 / docs r1

Research for the new office target `re_office_3s_slab` (Hazard reference profiles r1, FRE-S013): a 54,000 ft²
three-storey office, braced steel frame with composite floors, slab, no basement, first floor 0.25 ft above grade,
one traction elevator with a 4 ft pit, rooftop HVAC. **Evidence only: no record is added and no decision is taken
here.** The proposal and the open choice are in §6.

## 1. Questions

1. Which freshwater curve fits a three-storey office, and does a whole-building curve fit three storeys?
2. Which coastal curve, if any?
3. Are the elevator pit and the rooftop equipment covered?

## 2. Candidates considered

Structure curves for offices in the Hazus library (FRE-S003, FRE-S010; ordinates at depth above the first floor):

| Curve | Source | 0 ft | 1 | 2 | 3 | 4 | 6 | 10 | Use |
|---|---|---|---|---|---|---|---|---|---|
| **DF 431** Average Prof/Tech Services | USACE Galveston | 2% | 11 | 16 | 22 | 28 | 38 | 50 | **FEMA default for COM4** |
| DF 438 Big Office Commercial | USACE Galveston | 0 | 12 | 14 | 17 | 19 | 27 | 45 | alternative |
| DF 463 Professional, fresh water | USACE St. Paul | 5 | 12 | 17 | 20 | 21 | 22 | 31 | regional; flat above 4 ft |
| DF 466 Office Building | USACE Wilmington | 26 | 35 | 41 | 48 | 55 | 66 | 83 | regional |
| DF 444–462 accounting, legal, real-estate offices | USACE New Orleans | 0 | 16–43 | 34–64 | 65–100 | 80–100 | 90–100 | 92–100 | by water type and duration |
| NACCS prototype 2 (engineered commercial) | USACE NACCS 2015 | | | | | | | | coastal; two storeys (FRE-C008) |

DF 431 is the same at every knot in three independent copies: the Pollack compilation (FRE-S001/S003), USACE
go-consequences (FRE-S005; also checked by Hazard's office source check) and FEMA's Hazus 6.1 extract (FRE-S010)
(FRE-C032).

## 3. What FEMA itself assigns

FEMA's default table (Hazus 6.1 `flBldgStructDmgFinal`, matching Hazus 7.0 Tables 5-2 to 5-4) assigns **DF 431 to
COM4 at every height class (low-rise under 4 storeys, mid-rise 4–7, high-rise over 7), with or without basement,
and for riverine, coastal A and coastal V hazards alike** (FRE-C033). The three-storey office is COM4 low-rise
without basement, so DF 431 matches every key FEMA selects on. FEMA does not adjust commercial curves for height,
and the Galveston source does not state the height of the buildings behind the average.

## 4. Does damage fall with more storeys? NFIP claims

Business occupancies (NFIP 4, 6, 18), slab, by number of floors; damage ratio = building damage / building
replacement cost; depth above a 0.25 ft floor; bands with at least 15 claims
([by-storeys table](NFIP_CLAIMS_BY_STOREYS_flood_real_estate__model_v0_1__docs_r1.csv), FRE-C034):

| Water | Floors | Claims | Claims mean | DF 431 on the same claims | NACCS P2 on the same claims |
|---|---|---|---|---|---|
| Freshwater | 1 | 6,529 | 14.4% | 13.7% | |
| Freshwater | 2 | 1,628 | 11.3% | 14.4% | |
| Freshwater | 3 or more | 228 | 6.3% | 9.8% | |
| Coastal surge | 1 | 1,325 | 20.3% | 16.5% | 26.0% |
| Coastal surge | 2 | 454 | 12.5% | 14.3% | 23.4% |
| Coastal surge | 3 or more | 46 | 5.9% | 10.6% | 19.2% |

- **Yes, damage as a share of the building falls with height.** At the same depth band, two-floor buildings show
  about 0.75 of the one-floor ratio (freshwater; 0.67 coastal), and three-or-more-floor buildings about 0.5
  (freshwater, three bands up to 3 ft). This is not one-third: ground-floor services, finishes and the structure
  carry more than their floor-area share.
- **DF 431 fits one-floor business claims** (13.7% vs 14.4%) and **overstates three-or-more-floor claims by about
  3.5 points (×1.6)** at the shallow depths where they exist.
- **Coastal:** on two-floor and taller claims DF 431 is within 2–5 points; NACCS prototype 2 is 11–13 points above
  (×1.9–3.3) (FRE-C035).
- DF 438 is close to DF 431 on these claims (within 2–3 points); DF 466 is 21–34 points above every group, and the
  New Orleans curves reach 65–100% by 3 ft (FRE-C036).

Limits: NFIP floors code 3 means "three or more", so it mixes three-storey and high-rise buildings; the
three-or-more sample is small (228 freshwater, 46 coastal) and limited to under 3 ft; occupancies are all
business uses, not offices only; the claims are mostly Gulf states (FRE-S012).

## 5. Elevator pit and rooftop equipment

| Item | Finding |
|---|---|
| Elevator pit (4 ft below the floor) and ground-floor controls (0.5 ft above the floor) | Wetted as soon as water is above the floor. DF 431 is a whole-building class average and does not say whether elevators are in the averaged buildings. No source curve for elevator flood damage was found. Treated as inside the assembly, not added separately (overlap rule); a small share of building value |
| Rooftop HVAC (roof at 39 ft) | Never reached within the curve's range (24 ft). The class average may include ground-level HVAC, so DF 431 may slightly overstate services damage for this building |
| Upper floors (13 ft, 26 ft) | Reached only above 13 ft of water; the whole-building curve already spreads damage over the building, which is the source of the height question in §4 |

## 6. Proposal (open for decision)

**Freshwater.** Options:

| Option | What | For | Against |
|---|---|---|---|
| **A. DF 431 as published (recommended)** | FEMA's default for this exact class | Matches FEMA's own selection keys; adopted, not derived; three verified copies | Likely conservative for three storeys: about ×1.6 the claims at shallow depth |
| B. DF 438 | Another Galveston office curve | Name fits a large office | Not FEMA's default; fits the claims no better |
| C. DF 431 × a storey factor (about 0.5–0.6) | Scale by the NFIP ratio | Closer to multi-floor claims | A derived curve from a small, mixed sample; changes the method from adopted to calibrated |

Option A with the height bias recorded and the option-C factor kept as a stated sensitivity is the recommendation:
it keeps the cell adopted and FEMA-consistent, and the bias is visible rather than hidden.

**Coastal.** FEMA assigns DF 431 to COM4 in coastal zones too (§3), and it is closer to multi-floor coastal claims
than NACCS prototype 2, which is a two-storey North Atlantic prototype and runs about twice the claims. Proposed:
**DF 431 for the office in coastal surge**, NACCS prototype 2 as the recorded alternative. This belongs with the
coastal decision for all three buildings (D-FRE-18), so it is decided there.

**Elevator and rooftop equipment.** No separate response; inside the assembly (§5).

## 7. What changes in the package once decided

A new selector `RE_COM_OFFICE_3S_SLAB` (first-floor height 0.25 ft) with its record(s), DF 431 ordinates in the
governed ordinates CSV, known-answer tests, and the office rows of the profile binding changed from unavailable.
