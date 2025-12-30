"""
Rollback Module

Handles rollback functionality for failed updates.
"""

import os
import shutil
from typing import Optional, Dict, List
from datetime import datetime


class RollbackManager:
    """Manages rollback operations for OTA updates."""

    def __init__(self, backup_dir: str = "/tmp/ota_backups"):
        self.backup_dir = backup_dir
        self.snapshots: Dict[str, str] = {}  # snapshot_id -> path

    def create_snapshot(self, source_dir: str, snapshot_id: Optional[str] = None) -> str:
        """Create a snapshot of the current state."""
        if snapshot_id is None:
            snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        snapshot_path = os.path.join(self.backup_dir, snapshot_id)
        if os.path.exists(snapshot_path):
            shutil.rmtree(snapshot_path)

        shutil.copytree(source_dir, snapshot_path)
        self.snapshots[snapshot_id] = snapshot_path
        return snapshot_id

    def rollback_to_snapshot(self, snapshot_id: str, target_dir: str) -> bool:
        """Rollback to a specific snapshot."""
        if snapshot_id not in self.snapshots:
            print(f"Snapshot {snapshot_id} not found")
            return False

        snapshot_path = self.snapshots[snapshot_id]
        if not os.path.exists(snapshot_path):
            print(f"Snapshot path {snapshot_path} does not exist")
            return False

        try:
            # Remove current state
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

            # Restore from snapshot
            for item in os.listdir(snapshot_path):
                src = os.path.join(snapshot_path, item)
                dst = os.path.join(target_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            return True

        except Exception as e:
            print(f"Rollback failed: {e}")
            return False

    def list_snapshots(self) -> List[str]:
        """List available snapshots."""
        return list(self.snapshots.keys())

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Delete a snapshot."""
        if snapshot_id not in self.snapshots:
            return False

        snapshot_path = self.snapshots[snapshot_id]
        if os.path.exists(snapshot_path):
            shutil.rmtree(snapshot_path)

        del self.snapshots[snapshot_id]
        return True

    def cleanup_old_snapshots(self, keep_count: int = 5):
        """Keep only the most recent snapshots."""
        sorted_snapshots = sorted(self.snapshots.keys(), reverse=True)
        to_delete = sorted_snapshots[keep_count:]

        for snapshot_id in to_delete:
            self.delete_snapshot(snapshot_id)