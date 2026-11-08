import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_boot_handoff import ValidationError, load_manifest, validate_manifest


class BootHandoffValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load_manifest(ROOT / "boot-handoff" / "manifest.example.json")

    def valid(self):
        return copy.deepcopy(self.example)

    def add_region(self, manifest, name, base, size, alignment=4096, status="documented"):
        manifest["memory_regions"].append({
            "name": name,
            "base": base,
            "size": size,
            "alignment": alignment,
            "status": status,
            "evidence": [{
                "claim": "synthetic test fixture only",
                "status": "documented",
                "scope": "exact_model",
                "url": "https://example.invalid/test-fixture"
            }]
        })

    def test_example_manifest_passes(self):
        validate_manifest(self.valid())

    def test_wrong_target_rejected(self):
        data = self.valid()
        data["target"]["model"] = "OTHER"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_malformed_identity_status_rejected_without_crash(self):
        data = self.valid()
        data["target"]["identity_status"] = []
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_family_evidence_cannot_confirm_target_identity(self):
        data = self.valid()
        data["target"]["identity_status"] = "confirmed"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_bool_not_accepted_as_integer(self):
        data = self.valid()
        data["boot_handoff"]["revision"] = True
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_unsigned_64_bit_overflow_rejected(self):
        data = self.valid()
        data["boot_handoff"]["phys_base"] = 1 << 64
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_zero_region_size_rejected(self):
        data = self.valid()
        self.add_region(data, "synthetic-a", 0x1000, 0)
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_non_power_of_two_alignment_rejected(self):
        data = self.valid()
        self.add_region(data, "synthetic-a", 0x1000, 0x1000, alignment=3000)
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_misaligned_base_rejected(self):
        data = self.valid()
        self.add_region(data, "synthetic-a", 0x1001, 0x1000)
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_address_range_overflow_rejected(self):
        data = self.valid()
        self.add_region(data, "synthetic-a", (1 << 64) - 0xFFF, 0x2000, alignment=1)
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_overlapping_regions_rejected(self):
        data = self.valid()
        self.add_region(data, "synthetic-a", 0x1000, 0x3000)
        self.add_region(data, "synthetic-b", 0x3000, 0x2000)
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_family_evidence_cannot_confirm_region(self):
        data = self.valid()
        self.add_region(data, "synthetic-a", 0x1000, 0x1000, status="confirmed")
        data["memory_regions"][0]["evidence"][0]["scope"] = "device_family"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_unknown_device_tree_must_not_claim_metadata(self):
        data = self.valid()
        data["device_tree"]["length"] = 128
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_described_device_tree_requires_digest_and_evidence(self):
        data = self.valid()
        data["device_tree"].update({
            "status": "described",
            "format": "dtb",
            "length": 128,
            "sha256": "a" * 64,
            "evidence": []
        })
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_non_https_evidence_rejected(self):
        data = self.valid()
        data["evidence"][0]["url"] = "http://example.invalid"
        with self.assertRaises(ValidationError):
            validate_manifest(data)

    def test_duplicate_region_name_rejected(self):
        data = self.valid()
        self.add_region(data, "same", 0x1000, 0x1000)
        self.add_region(data, "same", 0x3000, 0x1000)
        with self.assertRaises(ValidationError):
            validate_manifest(data)


if __name__ == "__main__":
    unittest.main()
