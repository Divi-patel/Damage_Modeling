"""Build docs/cells/CATALOGUE.md from the hand-written entries in docs/cells/catalogue/.

The entries carry the curated content (rows, tiers, scope, how to use, sources, checks). This script adds what it can
read from the repository itself (status from the runtime artifact index, model and docs version, curve-record count)
and writes one Markdown page. Standard library only.

    python3 scripts/reference_helpers/build_damage_curve_catalogue.py          # write CATALOGUE.md
    python3 scripts/reference_helpers/build_damage_curve_catalogue.py --check  # fail if CATALOGUE.md is stale
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELLS = ROOT / "docs" / "cells"
ENTRIES = CELLS / "catalogue"
OUT = CELLS / "CATALOGUE.md"
INDEX = ROOT / "docs" / "contracts" / "machine_readable_artifact_index.json"

ASSET_ORDER = ["Solar farm", "Wind farm", "Real estate", "Substation", "Battery storage"]
HAZARD_ORDER = ["Hail", "Flood", "Hurricane wind", "Convective wind", "Wildfire"]
TIERS = {
    "T1": ("Claims or field calibrated", "Fitted to insurance claims or field damage surveys of the same kind of asset."),
    "T2": ("Public lab, standard or physics", "Taken from a published standard, a public model such as FEMA Hazus, lab tests or physics."),
    "T3": ("Engineering proxy or adjacent evidence", "Borrowed from a similar asset or a related study, with an engineering step to make it fit."),
    "T4": ("Placeholder or expert judgment", "Our own judgment where no source gives the number; visible, never a silent default."),
}
NOTE_LABELS = {
    "reused_from": "Reused from",
    "not_a_hazard_profile": "Not a Hazard profile",
    "opt_in_only": "Opt-in only",
    "key_assumption": "Key assumption",
    "known_bias": "Known bias",
}
METHOD_LABELS = {
    "adopted": "Adopted as published",
    "fitted": "Fitted to data",
    "built_from_references": "Built from references",
    "reused": "Reused from another cell",
}
STATUS_LABELS = {
    "live": "Live",
    "proposal": "Proposal",
    "reused": "Reused",
    "gap": "Gap",
}
OUTPUT_LABELS = [("single_event", "Single event"), ("scenario_dollars", "Scenario dollars"), ("yearly_loss", "Yearly loss")]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_entries() -> list[dict]:
    entries = []
    for path in sorted(ENTRIES.glob("*.json")):
        entry = load_json(path)
        entry["_file"] = path.name
        entries.append(entry)
    return entries


def live_index() -> dict:
    return {a["cell_id"]: a for a in load_json(INDEX)["artifacts"]}


def curve_records(artifact: dict) -> list[dict]:
    """Numeric curve records: top-level curve_records[] or pathways[].curve_records[] (both formats in use)."""
    records = list(artifact.get("curve_records") or [])
    for pathway in artifact.get("pathways") or []:
        records.extend(pathway.get("curve_records") or [])
    return [r for r in records if isinstance(r, dict) and isinstance(r.get("curve_id"), str)]


def facts(entry: dict, index: dict) -> dict:
    """What the repository itself says about the entry."""
    kind = entry["kind"]
    if kind == "gap":
        return {"status": "gap", "version": "", "records": 0}
    path = ROOT / entry["artifact"]
    data = load_json(path)
    if kind == "binding":
        return {"status": "reused", "version": data.get("binding_id", ""), "records": 0}
    live = index.get(data.get("cell_id"))
    is_live = live is not None and live["path"] == entry["artifact"]
    version = f'{data.get("semantic_damage_model_version", "")}, {data.get("documentation_revision", "")}'.strip(", ")
    return {"status": "live" if is_live else "proposal", "version": version, "records": len(curve_records(data))}


def link(path: str, text: str | None = None) -> str:
    rel = os.path.relpath(ROOT / path, OUT.parent)
    return f"[{text or Path(path).name}]({rel})"


def tier_span(rows: list[dict], key: str) -> str:
    tiers = sorted({r[key] for r in rows if r.get(key)})
    if not tiers:
        return "–"
    return tiers[0] if len(tiers) == 1 else f"{tiers[0]}–{tiers[-1]}"


def ordered(values, order):
    return sorted(values, key=lambda v: (order.index(v) if v in order else len(order), v))


def anchor(entry: dict) -> str:
    return entry["entry_id"].replace("_", "-")


def cell_title(entry: dict) -> str:
    return f'{entry["asset"]} × {entry["hazard"]}'


def esc(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def render(entries: list[dict], index: dict) -> str:
    info = {e["entry_id"]: facts(e, index) for e in entries}
    dates = sorted(e["reviewed_on"] for e in entries)
    out: list[str] = []
    w = out.append

    w("---")
    w("author: owner-directed (JL) · agent-drafted")
    w(f"created: 2026-10-19")
    w(f"updated: {dates[-1] if dates else '2026-10-19'}")
    w("status: draft")
    w("---")
    w("")
    w("# Damage-curve catalogue")
    w("")
    w("<!-- Generated by scripts/reference_helpers/build_damage_curve_catalogue.py from docs/cells/catalogue/*.json."
      " Do not edit by hand; edit the entry and rebuild. -->")
    w("")
    counts = {s: sum(1 for i in info.values() if i["status"] == s) for s in STATUS_LABELS}
    w(f'Every damage curve in this repository, by asset and hazard: {counts["live"]} live cells, '
      f'{counts["proposal"]} proposals, {counts["reused"]} reused bindings and {counts["gap"]} gaps. '
      "Older versions that a newer one replaced are left out. Each entry was drafted by an agent from the cell's own "
      "files and has not yet been read by the cell owner or the reviewer.")
    w("")

    # How to read
    w("## How to read this catalogue")
    w("")
    w("**Status.**")
    w("")
    w("| Status | Meaning |")
    w("|---|---|")
    w("| Live | In the runtime artifact index (`docs/contracts/machine_readable_artifact_index.json`); the platform can call it |")
    w("| Proposal | Built and validated in the repository but not in the runtime index; waiting for review |")
    w("| Reused | No curve of its own; a consumer binding prices this asset with another cell's curve |")
    w("| Gap | No curve yet |")
    w("")
    w("**Evidence tiers.** Each curve gets two tiers from the cell's own tier table. *Shape* is the evidence for how "
      "damage rises with the hazard. *Cost* is the evidence for turning that damage into a share of value. When one "
      "source gives damage directly as a share of value (for example a FEMA Hazus loss ratio), shape and cost share "
      "that tier. Lower is stronger.")
    w("")
    w("| Tier | Repository label | Plain meaning |")
    w("|---|---|---|")
    for code, (label, meaning) in TIERS.items():
        repo_label = {"T1": "T1_claims_or_field_calibrated", "T2": "T2_public_lab_standard_or_physics",
                      "T3": "T3_engineering_proxy_or_adjacent_empirical", "T4": "T4_placeholder_or_expert_judgment"}[code]
        w(f"| {code} · {label} | `{repo_label}` | {meaning} |")
    w("")
    w("**Scope words.** *Not covered* lists parts that are inside the asset's value but have no curve, so the loss "
      "for them is missing. *Out of scope* lists things outside the asset's value or priced by another cell. "
      "*Missing mechanisms* are kinds of damage that a covered part's curve leaves out.")
    w("")
    w("**Notes on a curve row** (at most two): " + " · ".join(
        f"*{label}*" for label in NOTE_LABELS.values()) + ". *Opt-in only* means the platform must pass an explicit "
      "acknowledgement code before the curve answers.")
    w("")
    w("**Checks.** A *curve check* compares the curve itself with outside data in this repository. A *result check* "
      "compares the finished loss with outside loss numbers in the Hazard repository "
      "(`docs/data_sources/financial_range_*`).")
    w("")

    # Coverage map
    w("## Coverage map")
    w("")
    assets = ordered({e["asset"] for e in entries}, ASSET_ORDER)
    hazards = ordered({e["hazard"] for e in entries}, HAZARD_ORDER)
    w("| Asset | " + " | ".join(hazards) + " |")
    w("|---|" + "---|" * len(hazards))
    for asset in assets:
        cells = []
        for hazard in hazards:
            found = [e for e in entries if e["asset"] == asset and e["hazard"] == hazard]
            if not found:
                cells.append("–")
                continue
            parts = []
            for e in found:
                i = info[e["entry_id"]]
                text = STATUS_LABELS[i["status"]]
                if e["kind"] != "gap":
                    text += f' · {tier_span(e["rows"], "shape")} / {tier_span(e["rows"], "cost")}'
                if e.get("not_covered"):
                    text += " · partial"
                parts.append(f'[{text}](#{anchor(e)})')
            cells.append("<br>".join(parts))
        w(f"| **{asset}** | " + " | ".join(cells) + " |")
    w("")
    w("Cell text: status · shape tier / cost tier. *Partial* means some parts of the asset's value have no curve.")
    w("")

    # Index grouped by asset
    w("## Index")
    w("")
    for asset in assets:
        w(f"### {asset}")
        w("")
        w("| Cell | Status | Version | Method | Curves | Shape | Cost | Outside checks |")
        w("|---|---|---|---|---:|---|---|---|")
        for e in [e for h in hazards for e in entries if e["asset"] == asset and e["hazard"] == h]:
            i = info[e["entry_id"]]
            if e["kind"] == "gap":
                w(f'| [{e["hazard"]}](#{anchor(e)}) | Gap | – | – | 0 | – | – | – |')
                continue
            method = METHOD_LABELS.get(e["method"]["type"], e["method"]["type"])
            n_checks = len(e.get("checks") or [])
            curves = i["records"] if e["kind"] == "cell" else sum(len(r["curves"]) for r in e["rows"])
            w(f'| [{e["hazard"]}](#{anchor(e)}) | {STATUS_LABELS[i["status"]]} | {esc(i["version"])} | {method} | '
              f'{curves} | {tier_span(e["rows"], "shape")} | {tier_span(e["rows"], "cost")} | '
              f'{n_checks if n_checks else "none yet"} |')
        w("")

    # Detail
    w("## Cells")
    w("")
    for asset in assets:
        for e in [e for h in hazards for e in entries if e["asset"] == asset and e["hazard"] == h]:
            render_entry(w, e, info[e["entry_id"]])
    return "\n".join(out).rstrip() + "\n"


def render_entry(w, e: dict, i: dict) -> None:
    w(f'<a id="{anchor(e)}"></a>')
    w("")
    w(f"### {cell_title(e)}")
    w("")
    head = f'**{STATUS_LABELS[i["status"]]}**'
    if i["version"]:
        head += f' · {i["version"]}'
    if e["kind"] != "gap":
        head += f' · `{e["entry_id"]}` · {link(e["artifact"], "curve file" if e["kind"] == "cell" else "binding")}'
    head += f' · {e["reviewed_on"]}: {e["read_by"]}'
    w(head)
    w("")
    if e["kind"] == "gap":
        w(f'**Why no curve yet:** {e["reason"]}')
        w("")
        if e.get("out_of_scope"):
            w("**Out of scope:** " + "; ".join(e["out_of_scope"]))
            w("")
        if e.get("open_items"):
            w("**Open items:** " + "; ".join(e["open_items"]))
            w("")
        return
    if e.get("bindings"):
        w("**Consumer binding inside this cell:** " + " · ".join(link(b, str(Path(b).parent.name)) for b in e["bindings"]))
        w("")
    if e.get("next_version"):
        w(f'**Next version:** {e["next_version"]}')
        w("")
    w(f'**Input:** {e["input"]}')
    w("")
    w(f'**Method:** {METHOD_LABELS.get(e["method"]["type"], e["method"]["type"])}. {e["method"]["summary"]}.')
    w("")

    w("| Part | Curves | Variants | Shape | Cost | Notes |")
    w("|---|---|---|---|---|---|")
    for r in e["rows"]:
        curves = "<br>".join(f"`{c}`" for c in r["curves"])
        notes = "<br>".join(f'*{NOTE_LABELS.get(n["type"], n["type"])}:* {esc(n["text"])}' for n in r.get("notes") or [])
        w(f'| {esc(r["part"])} | {curves} | {esc(r.get("variants", "none"))} | '
          f'{r["shape"]} · {esc(r.get("shape_basis", ""))} | {r["cost"]} · {esc(r.get("cost_basis", ""))} | {notes} |')
    w("")

    hu = e["how_to_use"]
    w("**How to use this curve**")
    w("")
    w(f'- Damage is a share of: {hu["share_of"]}')
    for key, label in OUTPUT_LABELS:
        if key in hu.get("outputs", {}):
            w(f'- {label}: {hu["outputs"][key]}')
    for c in hu.get("conditions") or []:
        w(f"- Condition: {c}")
    w("")

    w("**Scope**")
    w("")
    w("- Not covered: " + ("; ".join(e["not_covered"]) if e.get("not_covered") else "nothing in the asset's value is left without a curve"))
    if e.get("out_of_scope"):
        w("- Out of scope: " + "; ".join(e["out_of_scope"]))
    if e.get("missing_mechanisms"):
        w("- Missing mechanisms: " + "; ".join(e["missing_mechanisms"]))
    w("")

    src_note = "from the cell's source register" if e.get("sources_from") == "register" else "taken from the cell's write-up"
    w(f"**Key sources** ({src_note})")
    w("")
    for s in e["key_sources"]:
        w(f"- {s}")
    w("")
    if e.get("judgment"):
        w("**Our judgment (T4 items)**")
        w("")
        for j in e["judgment"]:
            w(f"- {j}")
        w("")
    w("**Outside checks**")
    w("")
    if e.get("checks"):
        for c in e["checks"]:
            kind = "Curve check" if c["kind"] == "curve" else "Result check, Hazard repo"
            target = link(c["link"], "link") if not c["link"].startswith("http") else f'[link]({c["link"]})'
            w(f'- {kind}: {c["name"]} ({target})')
    else:
        w("- None yet")
    w("")
    if e.get("open_items"):
        w("**Open items**")
        w("")
        for o in e["open_items"]:
            w(f"- {o}")
        w("")
    files = e.get("files") or {}
    shown = [link(files[k], label) for k, label in
             (("write_up", "write-up"), ("decisions", "decisions"), ("validation", "validation"), ("notebooks", "notebooks"))
             if files.get(k)]
    if shown:
        w("**Files:** " + " · ".join(shown))
        w("")


def main() -> int:
    text = render(load_entries(), live_index())
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"STALE {OUT.relative_to(ROOT)}: rebuild with {Path(__file__).name}")
            return 1
        print(f"OK {OUT.relative_to(ROOT)} is up to date")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
