from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import uuid


@dataclass
class Fish:
    name: str
    group_name: str = "DC_Universe"
    lifetime: int = 15

    @property
    def remaining_lifetime(self):
        """Calculate remaining lifetime in seconds"""
        return max(0, self.lifetime - 1)

    @property
    def is_alive(self):
        """Check if fish is still alive"""
        return self.remaining_lifetime > 0


@dataclass
class Pond:
    name: str
    fishes: Dict[str, Fish] = field(default_factory=dict)
    connected_ponds: List[str] = field(default_factory=list)

    def add_fish(self, name, group_name, lifetime):
        """Create and add a new fish to the pond"""
        fish = Fish(
            name=name,
            group_name=group_name,
            lifetime=lifetime,
        )
        self.fishes[fish.name] = fish
        return fish

    def get_fish(self, name: str):
        if name in self.fishes:
            return self.fishes[name]
        raise ValueError(f"Fish with name {name} not found in pond")

    def remove_fish(self, name: str):
        if name in self.fishes:
            return self.fishes.pop(name)
        raise ValueError(f"Fish with name {name} not found in pond")

    def list_fishes(self):
        return list(self.fishes.values())

    def add_connected_pond(self, pond_name: str):
        if pond_name not in self.connected_ponds:
            self.connected_ponds.append(pond_name)

    def remove_connected_pond(self, pond_name: str):
        if pond_name in self.connected_ponds:
            self.connected_ponds.remove(pond_name)

    def get_connected_ponds(self):
        return self.connected_ponds
