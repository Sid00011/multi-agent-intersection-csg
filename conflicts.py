"""
Conflict table for intersection trajectories (origin -> destination).
Gère désormais les virages à gauche et les conflits de croisement complexes.
"""
from typing import Dict, Set, Tuple
from vehicle import Direction

Trajectory = Tuple[Direction, Direction]
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}

def _is_left_turn(o: Direction, d: Direction) -> bool:
    
    turns = {"S": "W", "N": "E", "E": "N", "W": "S"}
    return turns.get(o) == d

def _is_right_turn(o: Direction, d: Direction) -> bool:
    turns = {"S": "E", "N": "W", "E": "S", "W": "N"}
    return turns.get(o) == d

def are_trajectories_conflicting(t1: Trajectory, t2: Trajectory) -> bool:
    """
    Retourne True si les trajectoires t1 et t2 se croisent physiquement.
    """
    o1, d1 = t1
    o2, d2 = t2

    if o1 == o2:
        return True 
    
    if o1 == OPPOSITE[o2] and d1 == OPPOSITE[d2] and not _is_left_turn(o1, d1) and not _is_left_turn(o2, d2):
        return False 

    if _is_right_turn(o1, d1) and _is_right_turn(o2, d2):
        return d1 == d2 


    if _is_left_turn(o1, d1):
        if o2 == OPPOSITE[o1] and d2 == OPPOSITE[o2]: return True 
        
    ns_set = {"N", "S"}
    if (o1 in ns_set and o2 not in ns_set) or (o1 not in ns_set and o2 in ns_set):
        if _is_right_turn(o1, d1) or _is_right_turn(o2, d2):
            return False 
        return True

    return True 

def trajectories_conflict(
    origin_a: Direction,
    dest_a: Direction,
    origin_b: Direction,
    dest_b: Direction,
) -> bool:
    """
    Interface utilisée par csg_plan.py.
    """
    return are_trajectories_conflicting((origin_a, dest_a), (origin_b, dest_b))