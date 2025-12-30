"""
Updater Module

Handles the logic for applying OTA updates.
"""

import os
import shutil
from typing import List, Dict, Callable
from .ota_package import OTAPackage
from .verifier import Verifier


class Updater:
    """Manages OTA update application."""

    def __init__(self, verifier: Verifier, backup_dir: str = "/tmp/ota_backup"):
        self.verifier = verifier
        self.backup_dir = backup_dir
        self.update_steps: List[Callable] = []

    def add_update_step(self, step: Callable):
        """Add a step to the update process."""
        self.update_steps.append(step)

    def apply_update(self, package: OTAPackage, target_dir: str) -> bool:
        """Apply the OTA update package."""
        try:
            # Create backup
            self._create_backup(target_dir)

            # Verify package
            if not self._verify_package(package):
                self._rollback(target_dir)
                return False

            # Apply update steps
            for step in self.update_steps:
                if not step(package, target_dir):
                    self._rollback(target_dir)
                    return False

            # Clean up backup on success
            self._cleanup_backup()
            return True

        except Exception as e:
            print(f"Update failed: {e}")
            self._rollback(target_dir)
            return False

    def _verify_package(self, package: OTAPackage) -> bool:
        """Verify all files in the package."""
        for file_info in package.files:
            file_path = os.path.join(package.package_id, file_info['path'])
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False
            if not self.verifier.verify_hash(file_path, file_info['hash']):
                print(f"Hash verification failed for: {file_path}")
                return False
        return True

    def _create_backup(self, target_dir: str):
        """Create backup of current state."""
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)
        shutil.copytree(target_dir, self.backup_dir)

    def _rollback(self, target_dir: str):
        """Rollback to previous state."""
        if os.path.exists(self.backup_dir):
            shutil.rmtree(target_dir)
            shutil.copytree(self.backup_dir, target_dir)

    def _cleanup_backup(self):
        """Clean up backup after successful update."""
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)