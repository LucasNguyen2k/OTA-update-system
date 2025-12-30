"""
Tests for Rollback module.
"""

import unittest
import tempfile
import os
from src.rollback import RollbackManager


class TestRollbackManager(unittest.TestCase):

    def setUp(self):
        self.rollback_manager = RollbackManager()

    def test_create_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a source directory with some files
            source_dir = os.path.join(temp_dir, "source")
            os.makedirs(source_dir)
            with open(os.path.join(source_dir, "file1.txt"), "w") as f:
                f.write("content1")
            with open(os.path.join(source_dir, "file2.txt"), "w") as f:
                f.write("content2")

            snapshot_id = self.rollback_manager.create_snapshot(source_dir, "test_snapshot")

            self.assertIn("test_snapshot", self.rollback_manager.snapshots)
            snapshot_path = self.rollback_manager.snapshots[snapshot_id]
            self.assertTrue(os.path.exists(snapshot_path))
            self.assertTrue(os.path.exists(os.path.join(snapshot_path, "file1.txt")))
            self.assertTrue(os.path.exists(os.path.join(snapshot_path, "file2.txt")))

    def test_rollback_to_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source and target directories
            source_dir = os.path.join(temp_dir, "source")
            target_dir = os.path.join(temp_dir, "target")
            os.makedirs(source_dir)
            os.makedirs(target_dir)

            # Create initial files
            with open(os.path.join(source_dir, "file1.txt"), "w") as f:
                f.write("original")

            # Create snapshot
            snapshot_id = self.rollback_manager.create_snapshot(source_dir, "test_snapshot")

            # Modify target directory
            with open(os.path.join(target_dir, "file1.txt"), "w") as f:
                f.write("modified")
            with open(os.path.join(target_dir, "file3.txt"), "w") as f:
                f.write("new")

            # Rollback
            result = self.rollback_manager.rollback_to_snapshot(snapshot_id, target_dir)
            self.assertTrue(result)

            # Check rollback worked
            self.assertTrue(os.path.exists(os.path.join(target_dir, "file1.txt")))
            with open(os.path.join(target_dir, "file1.txt"), "r") as f:
                self.assertEqual(f.read(), "original")
            self.assertFalse(os.path.exists(os.path.join(target_dir, "file3.txt")))

    def test_list_snapshots(self):
        snapshots = self.rollback_manager.list_snapshots()
        self.assertIsInstance(snapshots, list)

    def test_delete_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "source")
            os.makedirs(source_dir)
            with open(os.path.join(source_dir, "file.txt"), "w") as f:
                f.write("test")

            snapshot_id = self.rollback_manager.create_snapshot(source_dir, "test_snapshot")
            result = self.rollback_manager.delete_snapshot(snapshot_id)
            self.assertTrue(result)
            self.assertNotIn(snapshot_id, self.rollback_manager.snapshots)


if __name__ == '__main__':
    unittest.main()