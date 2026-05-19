"""
Instance generator for benchmarking: creates Vehicle lists with reproducible randomness.
Trajectoires de virage corrigées : respecte les sens de circulation pour éviter les collisions frontales.
"""
import random
from typing import List

from vehicle import Vehicle, Direction

DIRECTIONS: List[Direction] = ["N", "S", "E", "W"]

def generate_vehicles(
    n: int,
    seed: int = 42,
    position_range: tuple = (100.0, 500.0), 
    speed_range: tuple = (8.0, 15.0),      
    bus_fraction: float = 0.15,            
) -> List[Vehicle]:
    """
    Génère n véhicules avec des règles de destination strictes :
    - Sud (S) -> Nord (N) ou Est (E)
    - Nord (N) -> Sud (S) ou Ouest (W)
    - Est (E)  -> Ouest (W) ou Nord (N)
    - Ouest (W) -> Est (E) ou Sud (S)
    """
    rng = random.Random(seed)
    vehicles: List[Vehicle] = []
    
    for i in range(n):
        position = rng.uniform(*position_range)
        vitesse = rng.uniform(*speed_range)
        origin = rng.choice(DIRECTIONS)
        
        if origin == "S":
            destination = rng.choice(["N", "E"])
        elif origin == "N":
            destination = rng.choice(["S", "W"])
        elif origin == "E":
            destination = rng.choice(["W", "N"])
        elif origin == "W":
            destination = rng.choice(["E", "S"])

        priorite = 2 if rng.random() < bus_fraction else 1
        eta = Vehicle.compute_eta_naturel(position, vitesse)
        
        v = Vehicle(
            id=i,
            position=position,
            vitesse=vitesse,
            origin=origin,
            destination=destination,
            priorite=priorite,
            ETA_naturel=eta,
        )
        vehicles.append(v)
        
    return vehicles