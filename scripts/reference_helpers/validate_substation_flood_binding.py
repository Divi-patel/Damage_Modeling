#!/usr/bin/env python3
"""Validate the non-reportable Flood station-binding review and its failure modes."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from review_substation_flood_binding import DEFAULT_BINDING, ROOT, evaluate_review, load_review


class BindingReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = load_review()

    def event(self, depth=4):
        return {"flood_depth_above_substation_grade_ft": depth,
                "water_quality_class": "freshwater_non_contaminated",
                "delivered_depth_basis": "unprotected_or_internal_post_bypass_depth"}

    def changed_binding(self, mutate):
        candidate = copy.deepcopy(self.review["binding"])
        mutate(candidate)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            path.write_text(json.dumps(candidate))
            return load_review(path)

    def test_full_value_accounted_once(self):
        r = self.review
        self.assertEqual(str(r["candidate_assembly_usd"]), "27353236.37")
        self.assertEqual(str(r["total_budget_usd"]), "30415059.81")
        self.assertEqual(str(r["outside_candidate_usd"]), "3061823.44")
        self.assertEqual(len(r["ledger"]), 31)
        self.assertEqual(sum(x["disposition"] == "candidate_assembly_denominator" for x in r["ledger"]), 27)

    def test_four_foot_source_and_candidate_dollars(self):
        result = evaluate_review(self.review, self.event())
        self.assertEqual(result["source_dr"], .07)
        self.assertEqual(result["audit_candidate_assembly_loss_usd"], 1914726.55)
        self.assertEqual(result["status"], "audit_arithmetic_only")
        self.assertIsNone(result["scenario_loss_usd"])
        self.assertIsNone(result["whole_station_loss_usd"])

    def test_knot_and_interpolation_parity(self):
        for depth, dr in [(0, 0), (1, .02), (3, .06), (5.5, .085), (7, .10), (10, .15)]:
            with self.subTest(depth=depth):
                result = evaluate_review(self.review, self.event(depth))
                self.assertAlmostEqual(result["source_dr"], dr, places=14)
                self.assertEqual(set(result["annual_metrics"].values()), {None})
                self.assertFalse(result["runtime_admitted"])

    def test_above_range_not_clamped(self):
        result = evaluate_review(self.review, self.event(10.01))
        self.assertIsNone(result["source_dr"])
        self.assertIsNone(result["audit_candidate_assembly_loss_usd"])
        self.assertIn("ABOVE_SOURCE_VALID_RANGE", result["reason_codes"])

    def test_missing_depth_is_not_dry(self):
        event = self.event(); del event["flood_depth_above_substation_grade_ft"]
        result = evaluate_review(self.review, event)
        self.assertIsNone(result["source_dr"])
        self.assertTrue(result["reason_codes"])

    def test_invalid_depth(self):
        for depth in [-1, float("nan"), float("inf"), True, "4"]:
            with self.subTest(depth=depth):
                result = evaluate_review(self.review, self.event(depth))
                self.assertIsNone(result["source_dr"])
                self.assertTrue(result["reason_codes"])

    def test_unknown_or_saline_water_withheld(self):
        for quality in ["unknown", "saline", None]:
            with self.subTest(quality=quality):
                event = self.event(); event["water_quality_class"] = quality
                result = evaluate_review(self.review, event)
                self.assertIsNone(result["audit_candidate_assembly_loss_usd"])
                self.assertTrue(result["reason_codes"])

    def test_missing_water_not_assumed_fresh(self):
        event = self.event(); del event["water_quality_class"]
        result = evaluate_review(self.review, event)
        self.assertIsNone(result["source_dr"])
        self.assertTrue(result["reason_codes"])

    def test_wse_same_datum_bridge(self):
        event = self.event(); del event["flood_depth_above_substation_grade_ft"]
        event.update(water_surface_elevation_m=11.2192, substation_grade_elevation_m=10,
                     water_surface_vertical_datum_id="LOCAL", substation_grade_vertical_datum_id="LOCAL")
        result = evaluate_review(self.review, event)
        self.assertAlmostEqual(result["source_dr"], .07, places=14)
        self.assertEqual(result["audit_candidate_assembly_loss_usd"], 1914726.55)
        event["substation_grade_vertical_datum_id"] = "OTHER"
        result = evaluate_review(self.review, event)
        self.assertIn("VERTICAL_DATUM_MISMATCH", result["reason_codes"])

    def test_no_double_depth_payload(self):
        event = self.event()
        event.update(water_surface_elevation_m=11.2192, substation_grade_elevation_m=10,
                     water_surface_vertical_datum_id="LOCAL", substation_grade_vertical_datum_id="LOCAL")
        result = evaluate_review(self.review, event)
        self.assertIsNone(result["source_dr"])
        self.assertTrue(result["reason_codes"])

    def test_annual_requests_never_emit(self):
        for metric in ["eal", "pml", "var", "tvar", "total", "scenario_loss"]:
            with self.subTest(metric=metric):
                result = evaluate_review(self.review, {**self.event(), "metric": metric})
                self.assertIsNone(result["source_dr"])
                self.assertIsNone(result["audit_candidate_assembly_loss_usd"])
                self.assertEqual(set(result["annual_metrics"].values()), {None})

    def test_no_hidden_height_value_or_ownership_override(self):
        for field in ["equipment_height_m", "value_usd", "exposure_fraction", "station_count", "component_dr"]:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "unknown field"):
                evaluate_review(self.review, {**self.event(), field: 1})

    def test_exact_input_and_artifact_pins(self):
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            self.changed_binding(lambda b: b["inputs"]["hazard_budget"].update(sha256="0" * 64))
        with self.assertRaisesRegex(ValueError, "ARTIFACT_PIN_MISMATCH"):
            self.changed_binding(lambda b: b["damage_pin"].update(documentation_revision="docs r999"))

    def test_value_row_overlap_and_omission_fail(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            self.changed_binding(lambda b: b["value_policy"]["candidate_assembly_row_ids"].append("road"))
        with self.assertRaisesRegex(ValueError, "missing"):
            self.changed_binding(lambda b: b["value_policy"]["candidate_assembly_row_ids"].pop())

    def test_no_parent_double_count_or_promotion(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            self.changed_binding(lambda b: b.update(component_responses_added=["FS_XFMR"]))
        with self.assertRaisesRegex(ValueError, "runtime"):
            self.changed_binding(lambda b: b.update(runtime_admitted=True))
        with self.assertRaisesRegex(ValueError, "one physical station"):
            self.changed_binding(lambda b: b.update(station_count=2))

    def test_known_helper_metadata_preserved(self):
        result = evaluate_review(self.review, self.event())
        self.assertEqual(result["source_helper_scenario_loss_status"], "withheld_noncanonical_proposal")
        self.assertIsNone(result["scenario_loss_usd"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BindingReviewTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"created": "2026-10-16", "status": "pass" if result.wasSuccessful() else "fail",
              "scope": "Candidate binding audit helper; not scientific or annual admission",
              "test_methods": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "binding_path": str(DEFAULT_BINDING.relative_to(ROOT)),
              "binding_sha256": hashlib.sha256(DEFAULT_BINDING.read_bytes()).hexdigest(),
              "review_helper_sha256": hashlib.sha256(Path(__file__).with_name(
                  "review_substation_flood_binding.py").read_bytes()).hexdigest(),
              "validator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path = ROOT / "docs/extra/discussion/substation_damage/verification/flood_binding_validation.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
