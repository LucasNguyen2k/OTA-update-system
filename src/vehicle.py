"""
Vehicle Module

Represents the vehicle's software state and configuration.
"""

from typing import Dict, List, Optional
import json


class Vehicle:
    """Represents a vehicle's software state."""

    def __init__(self, vehicle_id: str, current_version: str):
        self.vehicle_id = vehicle_id
        self.current_version = current_version
        self.installed_components: Dict[str, str] = {}  # component -> version
        self.update_history: List[Dict] = []

    def add_component(self, component: str, version: str):
        """Add or update a software component."""
        self.installed_components[component] = version

    def get_component_version(self, component: str) -> Optional[str]:
        """Get version of a specific component."""
        return self.installed_components.get(component)

    def record_update(self, package_id: str, new_version: str, timestamp: str):
        """Record an update in history."""
        self.update_history.append({
            'package_id': package_id,
            'previous_version': self.current_version,
            'new_version': new_version,
            'timestamp': timestamp
        })
        self.current_version = new_version

    def is_update_applicable(self, target_version: str) -> bool:
        """Check if an update is applicable to this vehicle."""
        # Simple version comparison - in real implementation, this would be more complex
        return target_version > self.current_version

    def to_dict(self) -> Dict:
        """Convert vehicle state to dictionary."""
        return {
            'vehicle_id': self.vehicle_id,
            'current_version': self.current_version,
            'installed_components': self.installed_components,
            'update_history': self.update_history
        }

    def save_state(self, path: str):
        """Save vehicle state to file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_state(cls, path: str) -> 'Vehicle':
        """Load vehicle state from file."""
        with open(path, 'r') as f:
            data = json.load(f)
        vehicle = cls(data['vehicle_id'], data['current_version'])
        vehicle.installed_components = data['installed_components']
        vehicle.update_history = data['update_history']
        return vehicle