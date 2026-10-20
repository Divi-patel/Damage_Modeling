# Value crosswalk guide

The damage library emits DRs; scenario loss needs a value basis.

## Allowed basis labels

```text
installed_TIV
physical_replaceable_value
failure_unit_value
exposed_failure_unit_value
insured_value
gross_claim
net_claim_after_deductible
business_interruption
unknown
```

## Required crosswalk table

| Source location/row | Failure unit | Value bucket | Value + declared unit (amount/share/area/count/capacity) | Financial class | Role in loss | Direct denominator? | Allocation/double-count rule | Status |
|---|---|---|---:|---|---|---:|---|---|

Use `../templates/TEMPLATE_VALUE_CROSSWALK.csv` for a row-level machine-readable view.

## Asset-appropriate quantities

Use the quantity that matches the physical subject: USD per m² of floor, roof or wall (name which),
USD per item, USD per MW/kW, a total budget or a dimensionless share. Preserve source currency, price year,
location/cost basis and repair scope in the source register/crosswalk notes. Do not convert between floor,
roof and wall area without the profile geometry. Do not invent capacity for a building.

The CSV already separates `value` and `unit`; these prompts add no runtime schema fields. Existing
Solar/Wind $/MW or $/kW crosswalks retain their units. Property market value, land, insurance limits,
physical repair/replacement, movable contents and business interruption are separate bases/scopes.

## Rule

Do not use published claims or benchmark numbers as if they were M3 physical-damage grain until they are classified:

```text
module-only hardware
module + replacement fieldwork
whole physical plant
installed TIV
insured gross claim
net claim after deductible
includes BI/downtime
unknown
```

## Practical use

The value workbook is not validation evidence. It is a denominator and comparability layer. It helps answer:

```text
Can this external $/MW number be compared to a module-only damage curve?
Does it include labor/fieldwork beyond hardware cap?
Does it exceed installed TIV or only failure-unit value?
```

## Reconciliation and overestimation controls

```text
- Map every material source row; do not crosswalk only the convenient rows.
- Split mixed rows or mark them unresolved.
- Separate direct vulnerable hardware from civil/support/logistics.
- Allocate support, mobilization, site management, rental, and inspection once
  after damaged failure units are known; do not give those rows an independent DR.
- Separate protected/exposed or applicable/inapplicable value before applying a pathway.
- Unknown at-risk or attack fractions do not default to one.
- Label arithmetic on a broader denominator as a pressure test, not an estimate,
  unless the curve y-axis and allocation rules support that denominator.
```

The crosswalk must include a reconciliation equation and unresolved difference. A cell cannot emit scenario loss merely because a whole-site installed-cost number exists.

For a multi-pathway cell, map each value row to `applicable_pathway_ids` (or `all_shared`) and keep event exposure separate from value identity. Sharing a value ledger does not authorize one pathway's exposed fraction or DR to be reused by another, and the same row may not be charged twice when compound event records overlap.
