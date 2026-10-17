---
author: "owner-directed (Divy) · agent-qualified and implemented"
created: 2026-10-16
updated: 2026-10-16
status: active
---

# Standalone Substation — Hurricane wind screening binding

This consumer binding reuses the canonical **tropical_cyclone_wind_solar model v2.1 / docs r2**
`PV_GSU_SUBSTATION` failure-unit response for the selected standalone station. The curve is already
separate from the Solar array. Its repository address does not require inventing a Solar plant or
converting the station into MW. The GSU-to-transmission-yard transfer remains **Tier 4 expert judgment**.

The owner selected assembly screening and deferred component research. This change supplies target,
exposure, value and annual-consumer facts; it adds no intrinsic numerical response, cell, selector or
shared-component library. Source model/docs/schema versions, capability and package release remain
unchanged. This is the consumer-binding path in the existing illustrative-intake/reuse guide, not a
claim that the canonical source is calibrated for every substation type.

## Source and handoff

- [binding.json](binding.json): exact machine contract and complete 31-row value ledger.
- [value_crosswalk.csv](value_crosswalk.csv): review export of that ledger, not an independent owner.
- [validation.json](validation.json): exact source/binding/resource hash and accounting checks.
- [Canonical source cell](../../../cells/tropical_cyclone_wind_solar/README.md): numerical authority,
  including source/claim records and ordered-state evidence. Artifact SHA:
  `2fbc34fbf8f91df408fe1b3c8d01d260d013119cbcba594b6a9a60044cd2113e`.
- [Hazard qualification and pilot](../../../../../Hazard_modeling/docs/plans/_cross_cutting/substation_conus/17_hurricane_wind_qualification.md):
  frequency, spatial coupling, annual metrics, numerical checks and national execution status.

Hazard installs byte-identical JSON resources and pins both hashes. It uses its installed evaluator;
there is no cross-repository runtime import. Recheck this handoff from the Damage root with:

```bash
python3 scripts/reference_helpers/validate_substation_hurricane_binding.py
```

## Seven-step qualification

| Step | Selected interpretation and evidence | Limit |
|---|---|---|
| 1. Asset/boundary | One 345/138 kV outdoor AIS, two 336 MVA transformers, 150 × 178 m fence; exact Hazard profile SHA | Canonical hypothetical design, not observed ownership or engineering certification |
| 2. Failure unit | One `PV_GSU_SUBSTATION` assembly, curve `TCWS21_GSU_SUBSTATION_SCREENING_T4_ORDERED_STATES` | No inferred independent transformer, switchgear, control-house or civil fragilities |
| 3. Numerator/denominator | Direct physical repair/replacement ratio × same-station fenced installed-cost proxy | Not BI, revenue, insured interest or a fraction of Solar plant cost |
| 4. Value partition | 27 fenced rows = $27,353,236.37; external road and three support allowances = $3,061,823.44 | Full $30,415,059.81 reference budget is not the loss denominator |
| 5. Physical value | Apply the assembly once; row IDs reconcile exactly with the existing station ledger | Fenced civil/site membership is T4 interpretation; bookkeeping detail does not imply component-specific vulnerability |
| 6. Demand bridge | Squared ratio of event and reference-design 3-second gusts at declared 10 m/Exposure C; parent ASCE MRI300 reference | Regional screening design policy, not observed station capacity; no equipment-height or resilience credit |
| 7. Curve/annual permission | Exact ordered-state response, domain 0–2; canonical capability permits consumer annual construction after frequency/coupling/value/cap qualification | Out-of-domain stays unavailable; frequency and annual tails are Hazard responsibilities |

## Demand and response

```text
STORM 10-minute sustained wind
    × (1 / 0.88) × 1.20 → event 3-second gust
    → (event gust / reference design gust)²
    → unchanged canonical station DR → DR × fenced station value
```

The input is a **pressure ratio**, not an unsquared speed ratio. At event gust 120 mph and design
gust 100 mph the source input is 1.44. Both gusts must use the same duration/unit/exposure convention.
An event/design ratio above √2 is outside this response's supported domain; it must not be clamped.

The response has ordered state costs `[0, 0.08, 0.35, 1]`, lognormal dispersion 0.35 and central
pressure-ratio medians `[0.95, 1.30, 1.70]`. Lower/upper resistance use the artifact's 0.8/1.25 median
factors. These are **three unweighted sensitivity scenarios**, not confidence bounds, scenario
probabilities or observed damage states. Hazard evaluates the canonical JSON; these numbers are
explanatory, not a second editable model.

The regional design policy changes assumed resistance across the map. This product compares one
station configuration under the same reference-design policy, not identical 100-mph hardware installed
everywhere. Changing that policy changes risk and requires a new governed consumer run.

## Value membership and applicability

The selected denominator preserves the Flood station's physical and value identity. MTEP24 table
amounts are used as published, with no second inflation uplift and no claim of 2026 replacement prices.
Equipment, fixed control building, cable/trench and fenced related civil works form one assembly.
Civil/site costs remain the weakest membership transfer: inclusion is a declared facility-value proxy,
not evidence that every dollar has the same component-level response. External road and support are
unmodeled, not immune. The crosswalk rationale IDs are the existing station-accounting IDs.

Do not add component losses on top of this assembly. A future component response must replace the
overlapping accounting scope and be requalified for this station before rerunning consumers.

## Allowed claim and remaining work

Allowed: relative direct-wind screening contribution and downstream capped annual metrics under the
declared source, spatial population, design, value and missing-tail rules. Hazard's pilot validates this
consumer implementation; it does not empirically validate the T4 response.

Rain, surge, debris, tornado, component heights, resilience credit, engineering adequacy, observed-site
risk, complete physical risk and portfolio Total are outside this handoff. Flood owns its separately
modeled water mechanisms. The source native wind field is 0.1°; a 0.05° reporting cell adds no finer wind
physics. A zero resolved contribution does not establish immunity or fill missing source/response tails.
The national grid, publication, dashboard adoption and Total remain separate Hazard checkpoints.
