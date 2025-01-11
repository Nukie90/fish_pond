from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime


@dataclass
class Fish:
    fish_id: str
    spawn_time: datetime
    from_pond: str


@dataclass
class Pond:
    name: str
    fishes: Dict[str, Fish] = field(default_factory=dict)
    connected_ponds: List[str] = field(default_factory=list)

    def add_fish(self, fish: Fish) -> None:
        self.fishes[fish.fish_id] = fish

    def remove_fish(self, fish_id: str) -> Fish:
        if fish_id in self.fishes:
            return self.fishes.pop(fish_id)
        raise ValueError(f"Fish with ID {fish_id} not found in pond")

    def get_fish(self, fish_id: str) -> Fish:
        if fish_id in self.fishes:
            return self.fishes[fish_id]
        raise ValueError(f"Fish with ID {fish_id} not found in pond")

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
