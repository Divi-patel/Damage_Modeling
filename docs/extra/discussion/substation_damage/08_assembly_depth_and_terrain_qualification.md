---
author: "owner-directed (Divy) · agent-researched"
created: 2026-10-16
updated: 2026-10-16
status: active
scope: Bounded source/claim review for the station assembly; research only, no canonical cell revision.
---

# Point-method precedent does not establish a whole-yard exposure rule

Hazard completed the agreed four-window resolution comparison and the remaining source/threshold pass.
The [qualification record](../../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/08_assembly_depth_qualification.md)
owns numerical results. This note owns source-to-response implications. **Later disposition:** the owner
accepted screening first; [the implemented conditional binding](../../../contracts/hazard_handoff/substation_flood_screening_v1/README.md)
records that decision, selected value and exact consumer proof. Annual permission stays withheld. The
evidence limits below are unchanged by the product decision.

## Evidence and claim ledger

| ID / source | Locator and access | Supported claim | Not established |
|---|---|---|---|
| SD-S021 / [FEMA Flood 6.1 manual](https://www.fema.gov/sites/default/files/documents/fema_hazus-flood-model-technical-manual-6-1.pdf) | §10.3, p.10-2; official indexed text, accessed 2026-10-16; direct PDF 403 | SD-C021: general utility methodology samples flood depth at facility coordinates. The page also lists substations as mapping-only | Geometric fence centre, heterogeneous-yard transfer, validation of our Pluvial physics, or current numerical endorsement of the legacy 2.1 curve |
| SD-S022 / [USGS vertical accuracy FAQ](https://www.usgs.gov/faqs/what-vertical-accuracy-3d-elevation-program-3dep-dems?items_per_page=6&page=1) | National 1/3-arc-second accuracy paragraph; official page accessed 2026-10-16 | SD-C022: as of 2022, national absolute vertical RMSE approximately 0.82 m; quality varies geographically | Local relative error, centimetre depression accuracy or a calibrated cutoff for this tile |
| SD-S023 / named tile capture | Hazard `data/flood/raw/substation_resolution/20261016_n49w099/manifest.json`; source and metadata hashes retained | SD-C023: the numerical comparison uses a specific source rather than an unspecified finer DEM | New complete source onboarding, observed inundation, built-pad or drainage representation |
| SD-S024 / executed threshold experiment | Hazard `data/flood/substation_pilots/20261016_threshold_r1/manifest.json`; 72 rows, same four fine windows | SD-C024: filtering shallow patches increases conditional-depth assembly audit loss in two controls while the centre stays dry | Any hypothesis is a calibrated loss, conservative bound, national prevalence estimate or admitted annual distribution |

SD-S021/022 are primary-source statements with the retrieval limits shown. SD-S023/024 are reproducible
internal evidence. Selecting a geometric-centre proxy, a cutoff or a value boundary remains engineering
judgment (T4); none of these source statements upgrades the inherited screening response's evidence grade.
The current artifact remains pinned to its existing source and version.

## Bounded retrieval record

Reviewed the current Flood/Wind dossier, source register, capability and exact evaluator, then official
FEMA indexed material and USGS metadata/accuracy documentation. Queries included:

- `Hazus flood substation "Table 7.9" "depth"`
- `"The depth of flooding at each Utility System Component"` restricted to `fema.gov`
- `"Hazus" "control room" "switchgear" flood depth`
- `site.usgs.gov 3DEP 1/3 arc second DEM vertical accuracy relative elevation hydrologic depression`

The official 2.1 and 6.1 Flood and 4.2.3 Inventory PDF requests returned 403. Official indexed 5.1/6.1/7.0
material corroborates facility-point extraction, but none supplies a recovered copy of the exact 2.1
PDF. The inherited SHA `476726f194ed7e0702e8d6b47ad62616c8ca78214e56e9efc848f3bd547ae669` is not
claimed as freshly verified. Third-party mirrors and unrelated facility examples were not promoted.
No source was located in this bounded search prescribing a fence-centre/mean/max rule for this partly
pondable station. This is a search-bounded negative result, not a universal absence claim. Stop retrieval
here for this checkpoint; another failed PDF retry does not resolve the product choice.

## Response and value implications

1. Source-native assembly curves remain legitimate reusable inventory. Component curves are required
   only when the desired output needs component-specific response or exposure, not because the station
   moved from a plant subsystem to a standalone asset.
2. A point calculation is a lower-detail screening representation. Do not infer entire-yard dryness,
   actual equipment loss or a conservative bound from it. Keep proxy zero and unknown whole-station loss
   distinguishable, including downstream Total handling.
3. The source's embedded equipment heights differ from our profile. No profile-height subtraction or
   elevation-intervention credit is justified by the unchanged assembly response.
4. Wet area cannot allocate repair value. Retaining only deeper patches can increase the conditional
   depth while reducing pondable area; applying that depth to every assembly dollar is not the selected
   transfer. The 31-row proposed $27.353M value crosswalk still requires explicit admission.
5. Better terrain support does not supply damage ordinates, equipment positions, hydraulic validation or
   annual permission. Component binding would help local height/value meaning, but would not cure DEM
   or drainage uncertainty by itself.

## Verdict and subsequent decision

The bounded investigation is complete. The owner subsequently accepted the labeled facility-point
screening scope; [the conditional handoff](../../../contracts/hazard_handoff/substation_flood_screening_v1/README.md)
records the selected value and consumer proof. Component-first modeling is deferred. Do not split the
assembly curve by cost share or portray the owner decision as scientific validation.

The current Wind-hosted annual prohibition stays in force. Hazard must qualify frequency, spatial support
and per-point tail bounds, followed by a governed Damage capability decision before annual output. The
source limitations established by this evidence note are unchanged.

Change class: **EVIDENCE_ONLY_NO_OUTPUT_CHANGE**, outside canonical cell packages. No cell model, docs,
schema or skill revision, new runtime Damage function, changed ordinate or annual permission is introduced.
