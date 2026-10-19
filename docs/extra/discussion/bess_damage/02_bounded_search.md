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
