---
author: "owner-directed (Divy) · agent-implemented"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Standalone Substation Flood assembly screening, using existing hazard methods.
---

# Derivation, scope and seven-step audit

**Change classification:** NEW_CELL_MODEL_RELEASE, model v1.0/docs r1; bundle/capability schema v3 unchanged; portable package remains unreleased. The existing `flood_wind` model and annual withholding are unchanged. This reuses qualified assembly evidence rather than undertaking deferred component research.

| Audit step | Decision / evidence |
|---|---|
| 1. Asset boundary | Existing 150×178 m 345/138 kV AIS reference, two 336 MVA transformers; hypothetical whole fenced station |
| 2. Failure unit | One mutually exclusive source assembly; component systems remain anatomy, never extra curves |
| 3. Denominator | Direct repair/replacement ratio of the same assembly, not outage or full power-plant TIV |
| 4. Value rows | Existing 31-row reviewed binding/crosswalk is inherited byte-for-byte |
| 5. Allocation | $27,353,236.37 fenced assembly; $3,061,823.44 outside/unmodeled; no invented component shares |
| 6. Site adapter | Facility-centre grade depth in ft; no equipment-height subtraction, area multiplier or protection credit |
| 7. Curve and annual use | Exact Table7.9 knots, linear interpolation on 0–10ft; missing/deeper demand remains null. Annual permission is conditional on the downstream consumer proof |

**Source pressure test.** FEMA Hazus-MH2.1 Table7.9 provides identical ESSL/ESSM/ESSH whole-assembly ratios [0,2,4,6,7,8,9,10,12,14,15]% at 0…10ft. The source embeds control-room/switchgear elevation assumptions. The inherited flood_wind dossier records source PDF SHA `476726f194ed7e0702e8d6b47ad62616c8ca78214e56e9efc848f3bd547ae669` and the current Hazus7 disabled-electric-loss warning. No inference of component fragility or current enabled FEMA implementation is made. Existing reviewed source evidence is reused; no new component-calibration search was needed for this scoped change.

**Coastal transfer (SUB-A02, Tier4).** For the first relative grid, apply the same legacy depth-response proxy to a Coastal facility depth within its tabulated range. This is an explicit engineering transfer, not evidence that fresh and saline water cause equal actual damage. Salinity/contamination corrosion, wave loading, scour and debris remain unquantified scope. The numerical output is a depth-only screening index expressed on the station replacement-value basis. It must not be called complete surge loss or a scientifically proved lower bound on real damage. Hazard/source-support zero contributions are an algebraic partial-model convention, not empirical assurance.

**Rare depth and caps.** Do not extend the table beyond10ft or assume its15% endpoint is a physical vulnerable-value ceiling. Above-domain draws are unknown-response contributions with a tag. The consumer retains their probability mass. Coastal annual occurrence sums are bounded by the station replacement value once; inland retains its existing single annual-maximum object. Use the current CONUS EAL-sum/tail-max composite with its existing non-joint meaning. Cross-hazard Total admission remains separate.

**Update triggers:** qualified larger-depth or coastal economic response; equipment-local curves and elevations; observed replacement value; improved hazard fields. None is required to produce the owner-selected initial screening grid. The metadata flags travel with every output.

