---
author: owner-directed (Divy) · agent-researched
created: 2026-10-19
updated: 2026-10-19
status: done
scope: First bounded external-Wildfire BESS demand and repair-evidence search
---

# Search boundary and disposition

Cutoff 2026-10-19. Target chain: external Wildfire → local outdoor-LFP equipment
exposure → physical state → same-unit repair/replacement cost. Deliverable: first
screening candidate, not CFD, electrochemistry or all-cause fire-frequency study.

Surfaces: current Damage index and Wildfire Solar/Wind evidence; Substation FSim
source/response/annual implementation; pinned BESS profile/cost audit; primary
USFS, Tesla, Sungrow, UL, DOE, CFA and NEMA publications. Manufacturer summaries
are primary for their own statements, not independent generic calibration.

Exact query families:

- `site.nrel.gov battery energy storage wildfire external fire enclosure thermal radiation`
- `site.energy.gov battery energy storage wildfire external fire safety`
- `site.tesla.com Megapack external fire wildfire emergency response guide`
- `site.sungrowpower.com PowerTitan external fire test wildfire`
- `site.ul.com UL 9540A external fire exposure wildfire thermal runaway test`
- `site.fs.usda.gov RDS-2016-0034-3 burn probability flame length six classes`
- `site.nema.org evaluating fire heat damaged electrical equipment replacement guide`
- `site.cfa.vic.gov.au Victorian Big Battery fire investigation report 2021 adjacent megapack thermal roof external`
- `site.nrel.gov wildfire energy storage enclosure damage curve`

A secondary-news discovery query returned leads; none was adopted as evidence.
Dispatch/PSPS studies, residential/EV numerical transfers, unnamed summaries,
Reddit, inferred standards clauses and unread/paywalled reports were excluded
from numerical adoption. This pass does not exhaust every OEM/insurer/journal.

| Link | Retained | Not supplied |
|---|---|---|
| Hazard | Pinned FSim and USFS definitions | Equipment dose/duration/joint fire footprint |
| Electrical response | Exact existing ordinal tables, T4 | Target-specific BESS calibration |
| Battery mechanism | Tesla local-heat/handling guidance | Class threshold, failure odds, repair bill |
| Protected targets | Sungrow reported neighbors and inspected layout | Universal immunity, economic DR, full underlying test report |
| Test scope | UL internal initiation and adjacent exposures | Landscape burnover protocol/economic curve |
| Propagation | CFA observed spread | Wildfire initiation or a denominator for fitting probability |
| Controls | DOE design guidance | Fence/gravel/suppression coefficient |
| Costs | Related budget allocation/PCS value | Repair feasibility or event-state probability |

Access: web fetching rejected Sungrow PDF size and redirected Tesla PDF. Existing
Tesla bytes were reused, reading rev2.8 directly. USFS/Sungrow PDFs were retrieved
from primary origins in memory, hashed, extracted and selected pages inspected.
ENOSPC prevented full-PDF retention. Mersen 2016 NEMA PDF and current guide-body
requests returned403; the readable announcement is metadata/discovery only.
No purchase, private access, contact or form submission occurred.

Disk recovery removed only verified temporary duplicates, then one redundant
downloaded Hurricane tar after checking all 727 retained extracted members and
the exact immutable GCS generation/size. Original sources, extracted packages
and cloud originals remain. [Exact recovery](../../../../../../../Hazard_modeling/docs/plans/_cross_cutting/bess_conus/verification/wildfire_disk_recovery.json).

Checkpoint: no matched class-to-enclosure economic curve admitted within this
search. Stop the broad search. Next: cost policy BWF-Q01, explicit ordinal
candidate and bounded source/response proof. A T4 hypothesis may be qualified;
it must not become source-observed ignition odds or a calibrated mean. Reopen
targeted research on matched exposure/test/inspection/BOM evidence or access to
the complete manufacturer report.
