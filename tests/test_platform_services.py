import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_platform_services import (
    TouchEventModel,
    TouchSample,
    ValidationError,
    load_manifest,
    validate_manifest,
)


class PlatformServicesValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load_manifest(ROOT / "xnuloader" / "platform-services.example.json")

    def valid(self):
        return copy.deepcopy(self.example)

    def exact_evidence(self):
        return [{
            "claim": "synthetic exact-model test evidence",
            "scope": "exact_model",
            "url": "https://example.invalid/test-evidence",
        }]

    def test_unknown_by_default_example_passes(self):
        validate_manifest(self.valid())

    def test_wrong_target_rejected(self):
        data = self.valid()
        data["target"]["model"] = "OTHER"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_available_display_requires_exact_model_evidence(self):
        data = self.valid()
        data["display"].update({
            "status": "available",
            "mode": {
                "width": 1080,
                "height": 2460,
                "pixel_format": "synthetic",
                "pixels_per_scan_line": 1080,
            },
            "evidence": [{
                "claim": "family-only test evidence",
                "scope": "device_family",
                "url": "https://example.invalid/family",
            }],
        })
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_available_touch_requires_exact_model_evidence(self):
        data = self.valid()
        data["touch"].update({
            "status": "available",
            "coordinate_range": {"min_x": 0, "max_x": 100, "min_y": 0, "max_y": 200},
            "evidence": [{
                "claim": "family-only test evidence",
                "scope": "device_family",
                "url": "https://example.invalid/family",
            }],
        })
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_available_touch_with_exact_model_evidence_passes(self):
        data = self.valid()
        data["touch"].update({
            "status": "available",
            "coordinate_range": {"min_x": 0, "max_x": 100, "min_y": 0, "max_y": 200},
            "evidence": self.exact_evidence(),
        })
        validate_manifest(data)

    def test_unknown_touch_cannot_claim_coordinate_range(self):
        data = self.valid()
        data["touch"]["coordinate_range"] = {"min_x": 0, "max_x": 100, "min_y": 0, "max_y": 200}
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_invalid_display_stride_rejected(self):
        data = self.valid()
        data["display"].update({
            "status": "available",
            "mode": {
                "width": 100,
                "height": 200,
                "pixel_format": "synthetic",
                "pixels_per_scan_line": 99,
            },
            "evidence": self.exact_evidence(),
        })
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_available_fallback_requires_protocol_name(self):
        data = self.valid()
        data["fallback_pointer"]["status"] = "available"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_identified_environment_requires_name(self):
        data = self.valid()
        data["environment"]["status"] = "identified"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_malformed_identity_status_rejected_without_crash(self):
        data = self.valid()
        data["target"]["identity_status"] = []
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_malformed_evidence_scope_rejected_without_crash(self):
        data = self.valid()
        data["display"]["evidence"] = [{
            "claim": "malformed test evidence",
            "scope": [],
            "url": "https://example.invalid/test",
        }]
        with self.assertRaises(ValidationError):
            validate_manifest(data)


class TouchEventModelTests(unittest.TestCase):
    def setUp(self):
        self.model = TouchEventModel(0, 100, 0, 200)

    def test_contact_lifecycle_emits_down_move_up(self):
        self.assertEqual(self.model.process(TouchSample(True, 10, 20)).kind, "down")
        self.assertEqual(self.model.process(TouchSample(True, 15, 25)).kind, "move")
        self.assertEqual(self.model.process(TouchSample(False)).kind, "up")
        self.assertIsNone(self.model.process(TouchSample(False)))

    def test_failed_read_cancels_active_contact(self):
        self.model.process(TouchSample(True, 10, 20))
        event = self.model.process(TouchSample(False, failed=True))
        self.assertEqual((event.kind, event.x, event.y), ("cancel", 10, 20))
        self.assertIsNone(self.model.process(TouchSample(False)))

    def test_out_of_range_sample_cancels_active_contact(self):
        self.model.process(TouchSample(True, 10, 20))
        event = self.model.process(TouchSample(True, 101, 20))
        self.assertEqual(event.kind, "cancel")
        self.assertIsNone(self.model.process(TouchSample(False)))

    def test_out_of_range_initial_contact_is_rejected(self):
        with self.assertRaises(ValueError):
            self.model.process(TouchSample(True, 101, 20))

    def test_boolean_coordinates_are_not_integers(self):
        with self.assertRaises(ValueError):
            self.model.process(TouchSample(True, True, 20))

    def test_failure_without_active_contact_emits_nothing(self):
        self.assertIsNone(self.model.process(TouchSample(False, failed=True)))


if __name__ == "__main__":
    unittest.main()
