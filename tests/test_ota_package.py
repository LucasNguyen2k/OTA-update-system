"""
Tests for OTA Package module.
"""

import unittest
import tempfile
import os
from src.ota_package import OTAPackage, calculate_file_hash


class TestOTAPackage(unittest.TestCase):

    def setUp(self):
        self.package_id = "test_package_001"
        self.version = "1.0.0"
        self.files = [
            {"path": "file1.txt", "hash": "abc123", "size": "100"},
            {"path": "file2.txt", "hash": "def456", "size": "200"}
        ]
        self.package = OTAPackage(self.package_id, self.version, self.files)

    def test_to_manifest(self):
        manifest = self.package.to_manifest()
        self.assertEqual(manifest['package_id'], self.package_id)
        self.assertEqual(manifest['version'], self.version)
        self.assertEqual(manifest['files'], self.files)

    def test_save_and_load_manifest(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            self.package.save_manifest(temp_path)
            loaded_package = OTAPackage.from_manifest(temp_path)

            self.assertEqual(loaded_package.package_id, self.package_id)
            self.assertEqual(loaded_package.version, self.version)
            self.assertEqual(loaded_package.files, self.files)
        finally:
            os.unlink(temp_path)

    def test_calculate_file_hash(self):
        # Create a temporary file with known content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            # SHA256 hash of "test content"
            expected_hash = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72d3"
            actual_hash = calculate_file_hash(temp_path)
            self.assertEqual(actual_hash, expected_hash)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()