from vehicle import Vehicle

class NegotiationEngine:
    @staticmethod
    def evaluate_proposal(vehicle: Vehicle, proposal_data: dict) -> bool:
        """
        Décide d'accepter ou non de rejoindre un peloton.
        Arguments : Gain de temps vs Coût de coordination.
        """
        # Un Bus (prio 2) n'accepte de rejoindre que si ça ne le ralentit presque pas
        max_delay_allowed = 1.0 if vehicle.priorite == 2 else 5.0
        
        delay_offered = proposal_data.get('delay', 0)
        
        if delay_offered <= max_delay_allowed:
            return True
        return False

    @staticmethod
    def generate_arguments(platoon) -> dict:
        """ Génère des arguments pour convaincre l'intersection. """
        return {
            'has_bus': any(v.priorite == 2 for v in platoon.members),
            'size': len(platoon.members),
            'avg_eta': sum(v.ETA_naturel for v in platoon.members) / len(platoon.members)
        }