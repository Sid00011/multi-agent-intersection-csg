from typing import Dict, List, Set, Tuple
import numpy as np
from conflicts import trajectories_conflict
from platoon import Platoon
from vehicle import Vehicle, Direction

GAP_BETWEEN_MEMBERS = 0.5  
SAFETY_MARGIN = 0.8       
MIN_CROSS_DURATION = 2.0   

def phase_filter(vehicles: List[Vehicle], eta_proximity: float = 6.0) -> List[List[Vehicle]]:
    """ Regroupe les véhicules par trajectoire. """
    by_traj: Dict[Tuple[Direction, Direction], List[Vehicle]] = {}
    for v in vehicles:
        key = (v.origin, v.destination)
        by_traj.setdefault(key, []).append(v)
    
    candidates = []
    for group in by_traj.values():
        group.sort(key=lambda x: x.ETA_naturel)
        i = 0
        while i < len(group):
            cluster = [group[i]]
            t0 = group[i].ETA_naturel
            j = i + 1
            while j < len(group) and (group[j].ETA_naturel - t0) <= eta_proximity:
                cluster.append(group[j])
                j += 1
            candidates.append(cluster)
            i = j
    return candidates

def phase_csg(vehicles: List[Vehicle], candidates: List[List[Vehicle]]) -> List[Platoon]:
    """ Génère les coalitions en priorisant les Bus et les grands groupes. """
    used_ids = set()
    platoons = []
    
    sorted_candidates = sorted(candidates, key=lambda g: (any(v.priorite == 2 for v in g), len(g)), reverse=True)
    
    for group in sorted_candidates:
        if any(v.id in used_ids for v in group): continue
        leader = min(group, key=lambda x: x.ETA_naturel)
        platoons.append(Platoon(group, leader))
        used_ids.update(v.id for v in group)
    
    for v in vehicles:
        if v.id not in used_ids:
            platoons.append(Platoon([v], v))
    return platoons

def phase_schedule(platoons: List[Platoon]) -> List[Tuple[Platoon, float, float]]:
    """ Ordonnance le passage sans collision. """
    sorted_p = sorted(platoons, key=lambda x: (-x.priority, x.leader.ETA_naturel))
    
    scheduled = [] 
    for p in sorted_p:
        duration = (len(p.members) - 1) * GAP_BETWEEN_MEMBERS + MIN_CROSS_DURATION
        t_req = p.leader.ETA_naturel
        
        conflict = True
        while conflict:
            conflict = False
            for other_p, o_start, o_end in scheduled:
                if trajectories_conflict(p.leader.origin, p.leader.destination, 
                                         other_p.leader.origin, other_p.leader.destination):
                    if not (t_req + duration < o_start or t_req > o_end):
                        t_req = o_end + SAFETY_MARGIN
                        conflict = True
                        break
        
        scheduled.append((p, t_req, t_req + duration))
    return scheduled

def run_ccsg_plan(vehicles: List[Vehicle]) -> Tuple[List[Platoon], List[Tuple[Platoon, float, float]], float]:
    """ Calcule l'utilité avec une pondération favorable aux pelotons. """
    candidates = phase_filter(vehicles)
    platoons = phase_csg(vehicles, candidates)
    schedule = phase_schedule(platoons)
    
    total_u = 0.0
    for p, start, end in schedule:
        bonus = (len(p.members) ** 2) * 5.0
        penalite_temps = (start - p.leader.ETA_naturel) * 0.5
        total_u += (bonus - penalite_temps)
        
    return platoons, schedule, total_u


def baseline_total_wait(vehicles: List[Vehicle]) -> float:
    return sum(v.ETA_naturel for v in vehicles)

def ccsg_total_wait(schedule: List[Tuple[Platoon, float, float]]) -> float:
    total_wait = 0.0
    for p, start, end in schedule:
        for i, _ in enumerate(p.members):
            total_wait += (start + (i * GAP_BETWEEN_MEMBERS))
    return total_wait