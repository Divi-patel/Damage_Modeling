---
author: owner-directed (JL) · agent-drafted
created: 2026-10-19
updated: 2026-10-19
status: draft
---

# Damage-curve catalogue — hand-written entries

One JSON file per cell (or per consumer binding) feeds
[`../CATALOGUE.md`](../CATALOGUE.md). The builder
`scripts/reference_helpers/build_damage_curve_catalogue.py` reads these files plus each cell's own curve file, and
`validate_damage_curve_catalogue.py` fails if an entry no longer matches its cell. Edit these files, never the
generated catalogue.

## What goes here and what the builder reads itself

| From the cell's curve file (builder, automatic) | From this entry (hand-written) |
|---|---|
| status (in the runtime artifact index → live), model and docs version, number of curve records | rows (part or building, curves, variants, shape and cost tiers, notes), plain input line, not covered, out of scope, next version, how to use, method, key sources, our judgment, checks, open items, files |

## Fields

| Field | Required | Meaning |
|---|---|---|
| `entry_id` | yes | File name without `.json`; normally the cell ID |
| `kind` | yes | `cell` (a cell with its own curves), `binding` (reuses another cell's curve) or `gap` (no curve yet) |
| `asset`, `hazard` | yes | Catalogue labels, e.g. `Solar farm`, `Flood` |
| `artifact` | cell, binding | Path of the curve file (or `binding.json`) the entry describes |
| `artifact_sha256` | cell, binding | SHA-256 of that file when the entry was last reviewed; the validator flags a change |
| `reviewed_on`, `read_by` | yes | Date and who read the cell (e.g. `JL, from the cell's own tier table`) |
| `input` | cell, binding | One plain line: what the hazard input is, its unit and range |
| `not_covered` | yes | Parts that are in the asset's value but have no curve (list; `[]` if none) |
| `out_of_scope` | yes | Things outside the asset's value or handled elsewhere (list) |
| `missing_mechanisms` | no | Kinds of damage a covered part's curve does not include (list) |
| `next_version` | no | A newer proposal waiting beside the live version, one line |
| `how_to_use` | cell, binding | `share_of` (what the damage ratio is a share of), `outputs` (single event, scenario dollars, yearly loss: allowed / conditional / withheld, with the condition) and `conditions` (list) |
| `method` | cell, binding | `type` (`adopted`, `fitted`, `built_from_references`, `reused`) and `summary` (one line; for `reused`, the reason and a link to the binding's justification) |
| `key_sources` | cell, binding | 3–5 short citations; `sources_from` says `register` (copied from the cell's source register) or `write-up` (extracted by hand from the cell's derivation write-up) |
| `judgment` | cell, binding | The T4 items, one plain line each |
| `checks` | yes | List of `{kind: curve|result, name, link}`; `[]` means "no outside check yet" |
| `open_items` | no | Unresolved questions (list) |
| `files` | cell, binding | Links: `write_up`, `decisions`, `validation`, `notebooks` |
| `rows` | cell, binding | One per part or building: `part`, `curves` (IDs), `variants` (text, or `none`), `shape` and `cost` (tier codes `T1`–`T4`, with a short `shape_basis` / `cost_basis`), `notes` (list of `{type, text}`) |
| `bindings` | no | Consumer bindings that are part of this cell (e.g. its value binding), so they need no entry of their own |
| `reason` | gap | Why there is no curve yet |

**Shape and cost.** *Shape* is what sets how damage rises with the hazard; *cost* is what turns that damage into a
share of value. Each is given the tier its source carries in the cell's own tier table (the parameter rows for curve
points or curve shape → shape; cost ratios, value denominators or cost mappings → cost). Where a source table already
gives damage as a share of value (e.g. Hazus loss ratios), shape and cost share that tier.

**Note types** (at most two per row, short): `reused_from`, `not_a_hazard_profile`, `opt_in_only`, `key_assumption`,
`known_bias`.

**Scope.** One entry per cell at its current best version (the live one; the proposal if nothing is live).
Superseded versions are left out. A newer proposal beside a live version goes in `next_version`.
