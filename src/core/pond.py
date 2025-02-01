from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import uuid


@dataclass
class Fish:
    name: str = field(default_factory=lambda: str(uuid.uuid4()))
    spawn_time: datetime = field(default_factory=datetime.now)
    group_name: str = ""
    lifetime: int = 15

    @property
    def remaining_lifetime(self) -> float:
        """Calculate remaining lifetime in seconds"""
        elapsed = (datetime.now() - self.spawn_time).total_seconds()
        return max(0, self.lifetime - elapsed)

    @property
    def is_alive(self) -> bool:
        """Check if fish is still alive"""
        return self.remaining_lifetime > 0


@dataclass
class Pond:
    name: str
    fishes: Dict[str, Fish] = field(default_factory=dict)
    connected_ponds: List[str] = field(default_factory=list)
    fish_lifetime: int = 15

    def add_fish(self) -> Fish:
        """Create and add a new fish to the pond"""
        fish = Fish(
            group_name=self.name,
            lifetime=self.fish_lifetime,
        )
        self.fishes[fish.name] = fish
        return fish

    def get_fish(self, name: str) -> Fish:
        if name in self.fishes:
            return self.fishes[name]
        raise ValueError(f"Fish with name {name} not found in pond")

    def remove_fish(self, name: str) -> Fish:
        if name in self.fishes:
            return self.fishes.pop(name)
        raise ValueError(f"Fish with name {name} not found in pond")

    def list_fishes(self) -> List[Fish]:
        return list(self.fishes.values())

    def add_connected_pond(self, pond_name: str) -> None:
        if pond_name not in self.connected_ponds:
            self.connected_ponds.append(pond_name)

    def remove_connected_pond(self, pond_name: str) -> None:
        if pond_name in self.connected_ponds:
            self.connected_ponds.remove(pond_name)

    def get_connected_ponds(self) -> List[str]:
        return self.connected_ponds
