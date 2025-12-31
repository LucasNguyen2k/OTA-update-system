"""
Tests for Verifier module.
"""

import unittest
import tempfile
import os
from src.verifier import Verifier


class TestVerifier(unittest.TestCase):

    def setUp(self):
        self.verifier = Verifier()

    def test_verify_hash_valid(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test content")
            temp_path = f.name

        try:
            # SHA256 hash of "test content"
            expected_hash = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"
            result = self.verifier.verify_hash(temp_path, expected_hash)
            self.assertTrue(result)
        finally:
            os.unlink(temp_path)

    def test_verify_hash_invalid(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            invalid_hash = "invalid_hash"
            result = self.verifier.verify_hash(temp_path, invalid_hash)
            self.assertFalse(result)
        finally:
            os.unlink(temp_path)

    def test_verify_signature_without_key(self):
        with self.assertRaises(ValueError):
            self.verifier.verify_signature(b"data", b"signature")


if __name__ == '__main__':
    unittest.main()