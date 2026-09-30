# Decision log — tropical-cyclone wind × solar model v2.1

## Decision 1 — a screening curve must produce the requested screening output

Model v2.0 was technically careful but operationally incomplete: five units were numeric, five direct/civil
units were withheld, replacement support had no assembly rule, and full-plant DR and scenario loss were
prohibited. That is not an acceptable end-to-end screening product.

Model v2.1 therefore uses labeled Tier-4 engineering proxies where direct calibration is unavailable. Proxy
grade is carried in every record and output; it is not used as a reason to suppress the result.

## Decision 2 — preserve the correct v2.0 array work

The Perry compatibility record and the four fixed/tracker ordered-state records remain numerically unchanged.
V2.1 adds five site-facility records for foundation, power conversion/collection, GSU/substation, SCADA, and
civil infrastructure.

## Decision 3 — assemble a complete named physical value profile

The caller must explicitly request
`NLR_Q1_2025_UPV_PV_ONLY_2024_USD_PHYSICAL_V1`. It contains 877.7957023626668 2024 USD/kWdc of physical
replacement value. Every direct/civil dollar is attached to a numeric failure-unit DR. Replacement-support
value is allocated once using the value-weighted direct/civil DR.

The output reports:

- physical loss per kWdc;
- physical replacement DR;
- installed-capex physical loss fraction;
- scenario physical dollars when positive `capacity_kwdc` is supplied.

## Decision 4 — retain the real tier boundary

The damage cell still does not compute frequency, EAL, PML, VaR, TVaR, insurance, BI, or downtime. These are
not missing curve outputs; they require Hazard-tier frequency/aggregation or a separate disruption model.

## Decision 5 — keep compound mechanisms separate

V2.1 is tropical-cyclone **wind-only** physical damage. Rain ingress, debris, surge/flood, and tornado loss
remain separate pathways. Their indicators may be carried with a no-double-count acknowledgement, but they
do not silently modify this curve.

## Decision 6 — do not confuse the annual-metric gate with curve availability

Capability schema v3 requires `consumer_annual_metrics.status_before_promotion` to read
`withheld_noncanonical_proposal`. That field governs annual/tail metrics in the downstream consumer; it does
not withhold v2.1 event physical-damage outputs. The capability carries
`EVENT_PHYSICAL_DAMAGE_OUTPUTS_AVAILABLE_BEFORE_PROMOTION` to make that distinction machine-visible. A future
capability-schema revision should replace the promotion-timed name with a clearer consumer-readiness field.

## Decision 7 — promote the tested screening bytes without changing physics

The owner accepted the labeled screening result after the Everglades
current-STORM M0→M4 experiment passed `18 / 18` checks. Promotion changes
governance identity, package paths and the canonical damage-code ID, but not any
curve record, parameter, value composition, scenario calculation or numerical
output. The proposal remains immutable rollback evidence. The current package,
artifact index, changelog, publication manifest and Hazard registry become the
only canonical route.
