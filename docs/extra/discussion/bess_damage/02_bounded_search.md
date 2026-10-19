<!--
author: owner-directed (Divy) · agent-researched
created: 2026-10-18
updated: 2026-10-18
status: done
scope: First BESS Flood public-source and local-library search; bounded negative evidence only
-->

# First bounded evidence search

**Claim boundary (BF-C06):** within this October 18, 2026 review of the named
local library and publicly accessible English sources, no directly usable
external-depth-to-repair-cost dataset for the selected outdoor LFP enclosure was
located. The Chen paper supplies a failure-probability form, not the required
same-unit repair endpoint. This is not universal absence or a final no-model
decision.

## Protocol

- Target: natural-flood inundation of the selected BESS enclosure, PCS and
  internal electrical equipment; source exposure → ingress/contact →
  repair/replacement state → same-unit physical cost.
- Local surfaces: ten-entry canonical artifact index, Flood Solar/Wind/Substation
  packages, shared electrical method and existing component-reuse review.
- External surfaces: web-indexed primary OEM, standards-body, public-laboratory,
  utility/government and research-publisher documents.
- Access: public English material only; no private claims, OEM service portals,
  paid reports, expert interviews or new physical tests.
- Role separation: siting, operational degradation, outage simulations and safety
  instructions may inform anatomy/mechanisms; they do not independently calibrate
  a physical damage curve. No general search snippet is a numerical authority.

## Queries and endpoint tests

| Query family / actual representative query | Result and disposition |
|---|---|
| `site.tesla.com Megapack emergency response guide flooding submerged battery` | BF-S03 original PDF retrieved; revision 2.8 supersedes search snippet's 2.7. Flood and damage-handling sections reviewed. No DR function. |
| `site.nema.org water damaged electrical equipment batteries lithium ion replace`; `site.nema.org "4.12" "Batteries" "Water-Damaged"` | BF-S02 retrieved despite web-reader failure; relevant table visually checked, sections read. Conditional equipment consequence evidence. |
| `site.sungrowpower.com energy storage flood water immersed battery replace` | Residential emergency manual/install results; not adopted as utility-LFP numerical evidence. The profile's utility datasheet gives anatomy/rating, not ingress fragility. |
| `battery energy storage system flood inundation depth damage curve lithium ion utility scale study` | Chen et al. BF-S04 retrieved in full; equation 28 and case assumptions reviewed visually/textually. Failure endpoint and domain problems prevent direct reuse. Unrelated flooded lead-acid chemistry and intentional immersion-cooling papers excluded. |
| `site.tesla.com OR site.sungrowpower.com "Megapack" "flood" "damage"` | Safety/handling guidance; no directly adopted depth–cost points. |
| `site.sandia.gov energy storage flooding battery damage inundation` | Saltwater-immersion and propagation testing program described; BF-L01 is a specific next-source lead, not a test result. |
| `site.energy.gov Tehachapi energy storage project flood 2015 battery final report`; `"Tehachapi" "flood" "report"`; `"Tehachapi" "Final" "2016" energy storage site:osti.gov` | BF-S05 full final report downloaded and term-searched. Only flood match in extracted text is gas fire-suppression terminology. No inundation loss calibration adopted; not a claim that the plant never experienced flooding. |
| `"battery" "flood" "energy storage" "damage" site:fm.com`; AEGIS BESS white-paper link follow-up | No adopted target curve. BF-L02 AEGIS PDF URL returned HTML through shell download; indexed guidance is siting-related. Retrieval limitation retained. |

## Re-entry leads, not a new broad search

| ID | Exact lead / question | Acceptance test and owner |
|---|---|---|
| BF-L01 | [Sandia safety/reliability program](https://energy.sandia.gov/programs/energy-storage/safety-and-reliability/): obtain the actual saltwater-immersion report with chemistry, enclosure state and duration | Must distinguish isolated cells from integrated equipment and failure from repair cost. Damage researcher. |
| BF-L02 | [AEGIS July 2025 paper](https://www.aegislink.com/content/dam/aegislink/resources/publications/public/LossControl/Lithium-Ion_BESS_White_Paper-July_2025.pdf): recover original full PDF only if it contains repair or failure-case evidence | Flood-elevation guidance alone does not set vulnerability. Damage researcher. |
| BF-L03 | Utility LFP OEM installation/service drawings and post-flood disposition for a separate-PCS enclosure comparable to r1 | Entry datum plus wetted/replaced unit and scope; no assumption that the published outer envelope describes internal vulnerable heights. Damage + Hazard profile owner. |
| BF-L04 | Configuration-matched external-initiation propagation report | Quantify consequence conditional on initiation; do not introduce all-cause annual fire rates into the geographic map. Damage researcher. |

Files and hashes are in [source capture receipt](evidence/source_captures.json).
Downloaded originals remain in gitignored `data/bess/raw_flood_review_r1/`;
their URLs and hashes travel with this review. No private or paid evidence was
searched. Repeat this bounded pass when a matched report, loss record or changed
reference architecture becomes available, not merely because a numerical result
is desired.


## Second bounded pass — targeted retrieval, 2026-10-18

Followed the existing repair-unit and immersion leads, not a new open-ended
literature review. [BF-S09–BF-S12](evidence/sources.csv) and their
[exact captures](evidence/r2/source_captures.json) record the resulting evidence.

| Targeted question / search family | Primary retrieval | Disposition |
|---|---|---|
| Utility LFP installation manual, internal PACK/rack/control arrangement and flood-related foundation/cable entry | Sungrow ST2752UX full system manual | Separate-PCS anatomy; no exact r1 entry height or repair-value curve |
| Battery pack immersion exploratory investigation and saltwater test results | NHTSA/Argonne DOT HS 813 136 | Adjacent observed degradation; reject direct BESS probability/DR fit and short-soak postmortem anchor |
| Sandia recommended abuse testing water immersion | SAND2017-6925 | Protocol only; no response dataset |
| Storage PCS installation, enclosure compartments and flooding | SMA MVPS-S2-SCS-US-B8-SH-en-11 | Conditional electrical analogy; no automatic numeric protection or whole-group replacement |

Search scope remains public primary evidence. Automotive tests were retained for
mechanism and test-design lessons, not promoted to utility LFP calibration.
The next retrieval must address the specific repair-unit/value or entry question
in [the candidate review](03_flood_candidate_pressure_test.md#6-next-bounded-step-and-future-work).

## Third bounded pass — repair scope and source costs, 2026-10-18

This pass follows the remaining denominator and service questions, not a search
for an arbitrary smooth curve. [BF-S13–BF-S15](evidence/sources.csv) and
[r3 captures](evidence/r3/source_captures.json) identify adopted sources.

| Actual query / retrieval family | Result and disposition |
|---|---|
| `NREL PVSCM 2024 storage battery cells battery packs model csv github`; `"PVSCM_2024" zip`; `site:nrel.gov battery storage cost pack balance system 2024 2025` | Original Q1-2024 archive obtained from the lab catalog. Four members inventoried; UPV text and unloaded Excel template inspected without macros. Use compatible direct-input shares only; current 2025 benchmark page is a different vintage. |
| `"battery energy storage" "flooded" "replace"`; `"PowerTitan" "flood" "replacement"`; `site:sungrowpower.com "battery" "water" "replacement" "PACK"` | Official SBS050 manual retrieved; printed p6 supplies adjacent LFP non-reuse guidance. No utility depth-to-repair curve. |
| `site:sungrowpower.com ST5015 system manual replacement PACK battery flooded`; `"ST5015UX" "System Manual" site:sungrowpower.com`; `ST5015UX 4H System Manual pdf sungrowpower`; `"ST5015UX" "PACK replacement"`; `"ST5015UX-2H_ST5015UX-4H-SEN-Ver10" -site:scribd.com` | OEM datasheets and a third-party-indexed manual lead located. The matched full service manual was not recovered from a primary endpoint. Do not use the indexed PACK-replacement snippet to infer exact unit counts, elevations or costs. Retain title ST5015UX-2H_ST5015UX-4H-SEN-Ver10-202311 as a future service-document lead. |
| `site:deyeess.com "GE-F256" manual pdf`; `"GE-F256" "Flood" site:deyeess.com`; `"GE-F256" "water-soaked"`; `site:deyeinverter.com "GE-F256" manual` | Official product page links V03 and V01 manuals. Web reader size limit and direct HTTP403 prevented primary PDF retrieval, including one user-agent retry. Third-party full-text mirrors were not adopted as a numerical source. This is an access limit, not absence of guidance. |
| `"Ocracoke" "battery" "Dorian"` | Government/cooperative narratives describe elevated battery installation and diesel restoration. They do not demonstrate an immersed battery surviving without damage. No zero-loss anchor adopted. |

The official PowerKeeper product page also advertises flood resistance for a
different modular C&I configuration. No matched test report was recovered and
no advertised depth or numerical protection credit was transferred. Equipment
specificity matters in both directions: no automatic floodproofing and no
automatic universal destruction threshold.

Exact unadopted leads for a future targeted pass:

- Deye product: https://deyeess.com/product/ge-f128-ge-f240-ge-f256/
- Blocked V03 PDF: https://deyeess.com/wp-content/uploads/2026/05/Deye-ESS-User-Manual-GE-F256-BC-2-A3-EUEN-V03.pdf
- PowerKeeper product: https://official-overseas-aks-na.sungrowpower.com/mal/en/products/c-i-energy-storage-system/powerkeeper?tab=2
- Ocracoke government narrative: https://www.resilienceexchange.nc.gov/identify-actions/success-stories/ocracoke-island-electric-cooperatives-microgrid

**Checkpoint:** a sourced cost allocation is now available. A matched utility
depth-to-affected-module/service mapping still is not. Resolve
[BF-Q01's explicit policy choice](04_grouped_repair_and_value.md) rather than
restart a broad search or silently insert a central damage estimate.
