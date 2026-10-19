"""Run the Hazard generic v3 damage loader against the hail × real estate proposal.

A read-only consumer check for the validation report §4: every known-answer test request is sent through
Hazard's ``evaluate_v3_damage_call`` and compared with this cell's contract. Differences are listed, not
fixed; the Hazard repository is not modified.

Usage (from the repository root), with a copy of Hazard's loader, e.g.
``git -C <Hazard_Modeling> show origin/main:drivers/deep/src/deep/damage_loader.py > /tmp/hz/damage_loader.py``:
    python scripts/reference_helpers/check_hail_real_estate_hazard_loader.py /tmp/hz
Needs jsonschema (imported by the Hazard loader).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "docs/cells/hail_real_estate/proposed"
TAG = "hail_real_estate__model_v0_1__docs_r1"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    sys.path.insert(0, argv[1])
    import damage_loader as hazard  # noqa: E402  (Hazard's module, loaded from the given directory)

    art = json.loads((PROP / f"{TAG}__curve_artifact.json").read_text())
    kats = json.loads((PROP / f"known_answer_tests_{TAG}.json").read_text())
    agree, groups = 0, {}
    for t in kats["formula_known_answer_tests"] + kats["withheld_tests"] + kats["error_tests"]:
        try:
            out = hazard.evaluate_v3_damage_call(art, t["input"])
            got = (out["status"], out.get("failure_unit_damage_ratio"), out.get("reason_code"))
        except hazard.DamageLoadError as err:
            got = ("error", None, str(err))
        if "expected_error_code" in t:
            want = ("error", None, t["expected_error_code"])
        elif t["expected"]["status"] == "withheld":
            want = ("withheld", None, t["expected"]["reason_code"])
        else:
            want = ("conditional", t["expected"]["failure_unit_damage_ratio"], None)
        same = (got[0] == want[0]
                and (want[0] != "conditional" or math.isclose(got[1], want[1], rel_tol=0, abs_tol=1e-12))
                and (want[0] == "conditional" or got[2] == want[2]))
        if same:
            agree += 1
        else:
            groups.setdefault(f"cell {want[0]} {want[2] or ''} -> Hazard {got[0]} {got[2] or ''}".strip(), []).append(t["test_id"])
    total = agree + sum(len(v) for v in groups.values())
    print(f"{agree}/{total} known-answer requests agree")
    for key, ids in groups.items():
        print(f"  {len(ids):3d}  {key}   e.g. {ids[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
