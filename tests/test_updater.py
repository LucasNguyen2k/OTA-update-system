"""
Tests for Updater module.
"""

import unittest
import tempfile
import os
import shutil
from src.updater import Updater
from src.verifier import Verifier
from src.ota_package import OTAPackage


class TestUpdater(unittest.TestCase):

    def setUp(self):
        self.verifier = Verifier()
        self.updater = Updater(self.verifier)

    def test_add_update_step(self):
        def dummy_step(package, target_dir):
            return True

        self.updater.add_update_step(dummy_step)
        self.assertEqual(len(self.updater.update_steps), 1)

    def test_apply_update_success(self):
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = os.path.join(temp_dir, "target")
            os.makedirs(target_dir)

            # Create a simple package
            files = [{"path": "test.txt", "hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "size": "4"}]
            package = OTAPackage("test_pkg", "1.0.0", files)

            # Create the file in package directory
            package_dir = os.path.join(temp_dir, package.package_id)
            os.makedirs(package_dir)
            with open(os.path.join(package_dir, "test.txt"), "w") as f:
                f.write("test")

            # Mock the update step
            def copy_file(package, target_dir):
                src = os.path.join(package.package_id, "test.txt")
                dst = os.path.join(target_dir, "test.txt")
                shutil.copy(src, dst)
                return True

            self.updater.add_update_step(copy_file)

            # Change to temp_dir for relative paths
            old_cwd = os.getcwd()
            os.chdir(temp_dir)

            try:
                result = self.updater.apply_update(package, target_dir)
                self.assertTrue(result)
                self.assertTrue(os.path.exists(os.path.join(target_dir, "test.txt")))
            finally:
                os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main()