---
author: owner-directed (Divy) · agent-drafted
created: 2026-10-19
updated: 2026-10-19
status: active
scope: Exact lookup for proposed BESS wind v0.1
---

# Local candidate reference

| Coordinate | Value |
|---|---|
| Cell / pathway | `tropical_cyclone_wind_bess` / `tropical_cyclone_wind` |
| Model / docs | proposed v0.1 / r1 |
| Bundle / capability / emit schemas | Existing v3 / v3 / v2; unchanged |
| Numerical units | `BESS_INTEGRATED_ENCLOSURE`, `BESS_SEPARATE_PCS` |
| Mean response | `sum(exact-state probability × same-unit cost fraction)` |
| Demand domain | Declared comparable normalized pressure ratio 0–2; no extrapolation |
| Probability parameters | Inherited T4 beta 0.35; central medians 0.90/1.25/1.65; unweighted alternatives retained |
| Value | 80 × $1.05M + 20 × $520k = $94.4M candidate hardware; full TIV $109.8M fixed2024 |
| Missing risk | $15.4M property plus unquantified mechanisms/source gaps; never assumed safe |
| Capability | Conditional local scalar response only; canonical and annual use withheld |

Exact ordinate/state parameters: [curve JSON](../proposed/local_candidate_v0_1/curve_artifact.json).
Exact hashes: [consumption pin](../proposed/local_candidate_v0_1/consumption_pin.json).
Sources and claims: [package](../proposed/local_candidate_v0_1/README.md).
Inputs/withholding and example call: [metadata](../proposed/local_candidate_v0_1/metadata.md).
Checks: [validation](../proposed/local_candidate_v0_1/validation.json) and
[known answers](../proposed/local_candidate_v0_1/known_answers.json).

For the uniform-demand event fixture, sum 80 enclosure mean costs and 20 PCS
mean costs once. At pressure ratio 1 under the inherited central skeleton the
selected policy gives approximately $28.172M, or 25.66% of full TIV. This is not
a PML, an annual mean, an observed damage anchor or a joint failure distribution.

Update triggers: matched wind/anchorage tests replace synthetic probabilities;
service/BOM evidence revises repair states; value splits allow residual-property
extension; a qualified Hazard annual distribution/cap proof permits a separate
capability review. [Version history](../VERSION_REGISTRY.md) owns promotion status.
