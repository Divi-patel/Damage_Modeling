"""Check that the damage-curve catalogue entries still match the cells they describe.

Fails when an entry is malformed, points at a missing file, describes a curve file that changed since it was
reviewed, misses or invents a curve ID, leaves a cell without an entry, or when CATALOGUE.md is stale.
Standard library only.

    python3 scripts/reference_helpers/validate_damage_curve_catalogue.py
    HAZARD_REPO=~/path/to/Hazard_Modeling python3 ...   # also confirm result-check paths on Hazard origin/main
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from fnmatch import fnmatchcase
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_damage_curve_catalogue as cat  # noqa: E402

KINDS = {"cell", "binding", "gap"}
COMMON = ["entry_id", "kind", "asset", "hazard", "reviewed_on", "read_by", "not_covered", "out_of_scope", "checks"]
WITH_CURVE = ["artifact", "artifact_sha256", "input", "how_to_use", "method", "key_sources", "sources_from",
              "judgment", "files", "rows"]
ROW_FIELDS = ["part", "curves", "variants", "shape", "shape_basis", "cost", "cost_basis", "notes"]
METHODS = set(cat.METHOD_LABELS)
OUTPUT_VALUES = ("allowed", "conditional", "withheld")
HAZARD_MAIN = "https://github.com/aamani-ai/Hazard_Modeling/blob/main/"
# Optional local Hazard checkout used to confirm result-check paths exist on its origin/main.
HAZARD_REPO = os.environ.get("HAZARD_REPO")


def on_hazard_main(path: str) -> bool | None:
    if not HAZARD_REPO:
        return None
    done = subprocess.run(["git", "-C", HAZARD_REPO, "cat-file", "-e", f"origin/main:{path}"], capture_output=True)
    return done.returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def all_curve_ids() -> set[str]:
    ids: set[str] = set()
    for path in cat.CELLS.glob("*/*/*curve_artifact.json"):
        ids.update(r["curve_id"] for r in cat.curve_records(cat.load_json(path)))
    for path in cat.CELLS.glob("*/*/curve_artifact.json"):
        ids.update(r["curve_id"] for r in cat.curve_records(cat.load_json(path)))
    return ids


def check_entry(e: dict, index: dict, known_ids: set[str]) -> list[str]:
    errs: list[str] = []
    name = e["_file"]
    missing = [f for f in COMMON if f not in e]
    if e.get("kind") in ("cell", "binding"):
        missing += [f for f in WITH_CURVE if f not in e]
    if e.get("kind") == "gap" and "reason" not in e:
        missing.append("reason")
    if missing:
        return [f"{name}: missing fields {missing}"]
    if e["entry_id"] + ".json" != name:
        errs.append(f"{name}: entry_id {e['entry_id']!r} does not match the file name")
    if e["kind"] not in KINDS:
        errs.append(f"{name}: kind {e['kind']!r} not one of {sorted(KINDS)}")
    for c in e["checks"]:
        if c.get("kind") not in ("curve", "result") or not c.get("name") or not c.get("link"):
            errs.append(f"{name}: check needs kind curve|result, name and link: {c}")
        elif c["kind"] == "result":
            if not c["link"].startswith(HAZARD_MAIN):
                errs.append(f"{name}: result check must link into the Hazard repo ({HAZARD_MAIN}...): {c['link']}")
            elif on_hazard_main(c["link"][len(HAZARD_MAIN):]) is False:
                errs.append(f"{name}: result check path not on Hazard origin/main: {c['link']}")
        elif not (cat.ROOT / c["link"]).exists():
            errs.append(f"{name}: check link does not exist: {c['link']}")
    if e["kind"] == "gap":
        return errs

    artifact = cat.ROOT / e["artifact"]
    if not artifact.exists():
        return errs + [f"{name}: artifact does not exist: {e['artifact']}"]
    actual = sha256(artifact)
    if actual != e["artifact_sha256"]:
        errs.append(f"{name}: {e['artifact']} changed since review (sha256 now {actual}); "
                    "re-read the cell, update the entry, then update artifact_sha256")
    for b in e.get("bindings") or []:
        if not (cat.ROOT / b).exists():
            errs.append(f"{name}: bindings path does not exist: {b}")
    for key, path in e["files"].items():
        if path and not (cat.ROOT / path).exists():
            errs.append(f"{name}: files.{key} does not exist: {path}")
    if e["method"].get("type") not in METHODS:
        errs.append(f"{name}: method.type {e['method'].get('type')!r} not one of {sorted(METHODS)}")
    if e["sources_from"] not in ("register", "write-up"):
        errs.append(f"{name}: sources_from must be register or write-up")
    if not 1 <= len(e["key_sources"]) <= 6:
        errs.append(f"{name}: key_sources should list 3-5 sources (has {len(e['key_sources'])})")
    outputs = e["how_to_use"].get("outputs", {})
    for key, _ in cat.OUTPUT_LABELS:
        if not str(outputs.get(key, "")).startswith(OUTPUT_VALUES):
            errs.append(f"{name}: how_to_use.outputs.{key} must start with allowed / conditional / withheld")
    if not e["how_to_use"].get("share_of"):
        errs.append(f"{name}: how_to_use.share_of is empty")

    patterns: list[str] = []
    for r in e["rows"]:
        lack = [f for f in ROW_FIELDS if f not in r]
        if lack:
            errs.append(f"{name}: row {r.get('part')!r} missing {lack}")
            continue
        for key in ("shape", "cost"):
            if r[key] not in cat.TIERS:
                errs.append(f"{name}: row {r['part']!r} {key} tier {r[key]!r} not T1-T4")
        if len(r["notes"]) > 2:
            errs.append(f"{name}: row {r['part']!r} has {len(r['notes'])} notes (max 2)")
        for n in r["notes"]:
            if n.get("type") not in cat.NOTE_LABELS:
                errs.append(f"{name}: row {r['part']!r} note type {n.get('type')!r} unknown")
        patterns.extend(r["curves"])

    if e["kind"] == "cell":
        data = cat.load_json(artifact)
        ids = {r["curve_id"] for r in cat.curve_records(data)}
        uncovered = sorted(i for i in ids if not any(fnmatchcase(i, p) for p in patterns))
        unknown = sorted(p for p in patterns if not any(fnmatchcase(i, p) for i in ids))
        if uncovered:
            errs.append(f"{name}: curve records with no catalogue row: {uncovered}")
        if unknown:
            errs.append(f"{name}: row curve IDs not in the curve file: {unknown}")
        live = index.get(data.get("cell_id"))
        if live and live["path"] != e["artifact"]:
            errs.append(f"{name}: {data.get('cell_id')} is live at {live['path']}; the entry must describe the live "
                        "version (a newer proposal goes in next_version)")
    else:
        unknown = sorted(p for p in patterns if not any(fnmatchcase(i, p) for i in known_ids))
        if unknown:
            errs.append(f"{name}: reused curve IDs not found in any cell: {unknown}")
    return errs


def main() -> int:
    entries = cat.load_entries()
    index = cat.live_index()
    known_ids = all_curve_ids()
    errors: list[str] = []
    for e in entries:
        errors += check_entry(e, index, known_ids)

    by_id = {e["entry_id"] for e in entries}
    for folder in sorted(p.name for p in cat.CELLS.iterdir() if p.is_dir() and p.name != "catalogue"):
        if folder not in by_id:
            errors.append(f"cell folder docs/cells/{folder} has no catalogue entry")
    for cell_id in sorted(index):
        if cell_id not in by_id:
            errors.append(f"live cell {cell_id} has no catalogue entry")
    bindings = {str(p.parent.relative_to(cat.ROOT) / "binding.json")
                for p in (cat.ROOT / "docs/contracts/hazard_handoff").glob("*/binding.json")}
    described = {e.get("artifact") for e in entries if e.get("kind") == "binding"}
    described |= {b for e in entries for b in e.get("bindings") or []}
    for b in sorted(bindings - described):
        errors.append(f"consumer binding {b} has no catalogue entry")

    if not errors:
        text = cat.render(entries, index)
        if not cat.OUT.exists() or cat.OUT.read_text(encoding="utf-8") != text:
            errors.append("docs/cells/CATALOGUE.md is stale: run build_damage_curve_catalogue.py")

    for err in errors:
        print("FAIL", err)
    print(f"{'FAIL' if errors else 'PASS'}: {len(entries)} entries, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
