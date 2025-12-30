"""
Verifier Module

Handles hash and signature verification for OTA updates.
"""

import hashlib
import hmac
from typing import Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization


class Verifier:
    """Handles verification of OTA packages."""

    def __init__(self, public_key_path: Optional[str] = None):
        self.public_key = None
        if public_key_path:
            self.load_public_key(public_key_path)

    def load_public_key(self, path: str):
        """Load public key for signature verification."""
        with open(path, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(f.read())

    def verify_hash(self, file_path: str, expected_hash: str) -> bool:
        """Verify file hash matches expected value."""
        actual_hash = self._calculate_hash(file_path)
        return hmac.compare_digest(actual_hash, expected_hash)

    def verify_signature(self, data: bytes, signature: bytes) -> bool:
        """Verify digital signature."""
        if not self.public_key:
            raise ValueError("Public key not loaded")
        try:
            self.public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()