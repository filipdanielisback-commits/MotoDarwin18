import copy
import json
import unittest
from pathlib import Path

from validate_platform import validate_inventory


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "platform" / "xt2135-2.json"


class PlatformInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_project_inventory_passes_structural_checks(self):
        errors, warnings = validate_inventory(self.data)
        self.assertEqual(errors, [])
        self.assertGreater(len(warnings), 0)

    def test_wrong_model_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["device"]["model"] = "XT2135-1"
        errors, _ = validate_inventory(data)
        self.assertTrue(any("exact project target" in item for item in errors))

    def test_family_evidence_cannot_be_marked_confirmed(self):
        data = copy.deepcopy(self.data)
        data["components"][0]["status"] = "confirmed"
        errors, _ = validate_inventory(data)
        self.assertTrue(any("confirmed status requires exact_model evidence" in item for item in errors))

    def test_unknown_component_must_not_claim_a_value(self):
        data = copy.deepcopy(self.data)
        data["components"][0]["status"] = "unknown"
        errors, _ = validate_inventory(data)
        self.assertTrue(any("unknown status requires value=null" in item for item in errors))

    def test_non_https_source_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["components"][0]["evidence"][0]["url"] = "http://example.com/source"
        errors, _ = validate_inventory(data)
        self.assertTrue(any("must be an HTTPS URL" in item for item in errors))

    def test_missing_required_component_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["components"] = data["components"][1:]
        errors, _ = validate_inventory(data)
        self.assertTrue(any("required component missing: memory" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
