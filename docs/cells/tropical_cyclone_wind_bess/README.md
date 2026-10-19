---
author: owner-directed (Divy) · agent-implemented
created: 2026-10-19
updated: 2026-10-19
status: active
scope: BESS Hurricane-wind cell entry; proposed local-test candidate only
---

# Tropical-cyclone wind × BESS

**Proposed model v0.1 / docs r1: local testing only.** BW-Q01 selects integrated
enclosure replacement after major structural compromise, with repair retained
as a sensitivity. This is not a current runtime release, a calibrated model,
an annual-risk result or a BESS national wind map.

Start with [the physical explanation](basics/README.md),
[curation reasoning](basics/HOW_THE_MODEL_IS_BUILT.md) and
[exact reference](basics/MODEL_REFERENCE.md). The
[local package](proposed/local_candidate_v0_1/README.md) owns the proposed JSON,
exact pins, value crosswalk and conditional validation.

```text
tropical-cyclone wind × standalone outdoor LFP BESS
├─ integrated battery enclosure — primary conditional response
├─ separate PCS — related-equipment T4 proxy
├─ unit-MV/shared electrical, civil, fieldwork — unbound, not zero
└─ surge/rain flood, convective wind/tornado, autonomous failures — separate scopes
```

The included plant boundary and $109.8M fixed-2024-dollar TIV are unchanged.
Candidate enclosure/PCS property is $94.4M; remaining $15.4M has no wind response
here. No additional component loss is charged inside the integrated cabinet.
No equipment is declared DR≈0. Fences, walls, burial, vegetation, suppression,
storm kits and height receive no numeric protection credit. No conditioner-only
equipment is used to silently alter this response.

The axis is declared comparable local pressure demand/reference ratio, valid
0–2. The local candidate does not choose a national wind-reference policy or
convert a product wind label into resistance. Demand, value and uncertainty
semantics are in [metadata](proposed/local_candidate_v0_1/metadata.md).

Derivation: [candidate dossier](proposed/local_candidate_v0_1/derivation.md).
Audit views: CSV state costs, source/claim/parameter registers and the
[research comparison](../../extra/discussion/bess_damage/07_hurricane_enclosure_candidate.md).
The CSVs replace a workbook for this small local proposal; runtime input is JSON.

The reusable ordered-state primitive is exercised through an explicit-opt-in
local reader. It is not a production consumer. Hazard must separately qualify
wind-reference/exposure coupling, annual frequency/caps/tails and national
support before promotion. See [version history](VERSION_REGISTRY.md).
