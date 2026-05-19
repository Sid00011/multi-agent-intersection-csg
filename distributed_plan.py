from typing import List, Tuple
from vehicle import Vehicle
from platoon import Platoon
from v2x_messages import V2XMessage, MessageType
from negotiation import NegotiationEngine
from collections import defaultdict
from conflicts import trajectories_conflict

GAP = 0.5
SAFETY = 0.8
CROSS_TIME = 2.0
LOCAL_VISION = 6.0  

def run_distributed_negotiation(vehicles: List[Vehicle]) -> Tuple[List[Platoon], List[Tuple[Platoon, float, float]], float]:
    """
    Approche distribuée optimisée :
    - V2V : Vision locale plus large et dictionnaire par trajectoire
    - V2I : Insertion intelligente dans le planning pour éviter boucle while imbriquée
    """
    platoons = []
    processed_ids = set()

    sorted_vehicles = sorted(vehicles, key=lambda v: v.ETA_naturel)
    platoons_by_traj = defaultdict(list)  

    for v in sorted_vehicles:
        if v.id in processed_ids:
            continue
        key = (v.origin, v.destination)
        candidates = platoons_by_traj.get(key, [])
        best_target = None

        for p in candidates:
            if abs(v.ETA_naturel - p.leader.ETA_naturel) < LOCAL_VISION:
                if NegotiationEngine.evaluate_proposal(v, {'delay': 0.8}):
                    best_target = p
                    break

        if best_target:
            best_target.members.append(v)
            processed_ids.add(v.id)
        else:
            new_p = Platoon([v], v)
            platoons.append(new_p)
            platoons_by_traj[key].append(new_p)
            processed_ids.add(v.id)


    platoons_by_arrival = sorted(platoons, key=lambda p: p.leader.ETA_naturel)
    schedule = []
    timeline = []  

    for p in platoons_by_arrival:
        duration = (len(p.members) - 1) * GAP + CROSS_TIME
        t_req = p.leader.ETA_naturel

        # Chercher le prochain créneau disponible
        for start, end in timeline:
            if not (t_req + duration < start or t_req > end):
                t_req = end + SAFETY

        schedule.append((p, t_req, t_req + duration))
        timeline.append((t_req, t_req + duration))
        timeline.sort()

    # Calcul de l'utilité distribuée
    total_u = sum((len(p.members)**2 * 5.0) - (start - p.leader.ETA_naturel)*0.5
                  for p, start, end in schedule)

    return platoons, schedule, total_u
