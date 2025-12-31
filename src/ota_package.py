"""
OTA Package Module

Handles OTA update packages and manifests.
"""

import json
import hashlib
from typing import Dict, List, Optional


class OTAPackage:
    """Represents an OTA update package."""

    def __init__(self, package_id: str, version: str, files: List[Dict[str, str]]):
        self.package_id = package_id
        self.version = version
        self.files = files  # List of dicts with 'path', 'hash', 'size'

    def to_manifest(self) -> Dict:
        """Generate manifest dictionary."""
        return {
            'package_id': self.package_id,
            'version': self.version,
            'files': self.files
        }

    def save_manifest(self, path: str):
        """Save manifest to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_manifest(), f, indent=2)

    @classmethod
    def from_manifest(cls, path: str) -> 'OTAPackage':
        """Load package from manifest file."""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(data['package_id'], data['version'], data['files'])


def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()



"""
def calculate_file_hash(file_path: str) -> str:
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
"""