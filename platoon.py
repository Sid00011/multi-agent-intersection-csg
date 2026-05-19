"""
Platoon (Coalition) data structure and utility computation.
"""
from typing import List

from vehicle import Vehicle


class Platoon:
    """a
    A coalition of vehicles (platoon) with same destination.
    Utility: U = (Number of vehicles) - (Formation/speed adjustment cost).
    """

    def __init__(self, members: List[Vehicle], leader: Vehicle) -> None:
        if not members:
            raise ValueError("Platoon must have at least one member")
        if leader not in members:
            raise ValueError("Leader must be in members")
        self.members = list(members)
        self.leader = leader
        self._adjustment_cost: float = 0.0
        self._utilité: float = float(len(self.members))

    @property
    def utilité(self) -> float:
        """U = (Nombre de véhicules) - (Coût de formation/ajustement de vitesse)."""
        return self._utilité

    def set_adjustment_cost(self, cost: float) -> None:
        """Set the speed/formation adjustment cost and update utility."""
        self._adjustment_cost = max(0.0, cost)
        self._utilité = len(self.members) - self._adjustment_cost

    @property
    def adjustment_cost(self) -> float:
        return self._adjustment_cost

    @property
    def priority(self) -> int:
        """Platoon priority = max priority among members (2 > 1)."""
        return max(v.priorite for v in self.members)

    def __repr__(self) -> str:
        return f"Platoon(members={len(self.members)}, leader={self.leader.id}, U={self._utilité:.2f})"
