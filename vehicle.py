from dataclasses import dataclass
from typing import Literal

Direction = Literal["N", "S", "E", "W"]


def opposite_direction(d: Direction) -> Direction:
    return {"N": "S", "S": "N", "E": "W", "W": "E"}[d]


@dataclass
class Vehicle:

    id: int
    position: float  # distance to intersection (e.g. meters)
    vitesse: float  # speed (e.g. m/s)
    origin: Direction  # approach direction (d'où il vient)
    destination: Direction  # exit direction (où il va) — peut être tout droit, à droite ou à gauche
    priorite: int  # 1 = normal, 2 = bus/emergency
    ETA_naturel: float  # estimated time of arrival at intersection without modification

    def __post_init__(self) -> None:
        if self.position < 0:
            raise ValueError("position must be >= 0")
        if self.vitesse <= 0:
            raise ValueError("vitesse must be > 0")
        if self.priorite not in (1, 2):
            raise ValueError("priorite must be 1 or 2")
        if self.origin not in ("N", "S", "E", "W"):
            raise ValueError("origin must be N, S, E or W")
        if self.destination not in ("N", "S", "E", "W"):
            raise ValueError("destination must be N, S, E or W")
        if self.origin == self.destination:
            raise ValueError("origin and destination must differ (no U-turn)")

    def __repr__(self) -> str:
        return (
            f"Vehicle(id={self.id}, pos={self.position:.1f}, v={self.vitesse:.1f}, "
            f"{self.origin}->{self.destination}, prio={self.priorite}, ETA={self.ETA_naturel:.2f})"
        )

    @staticmethod
    def compute_eta_naturel(position: float, vitesse: float) -> float:
        """Compute natural ETA at intersection (position / speed)."""
        if vitesse <= 0:
            raise ValueError("vitesse must be > 0")
        return position / vitesse
