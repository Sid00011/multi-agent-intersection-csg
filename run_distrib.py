from instance_generator import generate_vehicles
from distributed_plan import run_distributed_negotiation

# 1. Utiliser la fonction correcte pour générer 20 véhicules
vehicles = generate_vehicles(n=20)

# 2. Lancer l'approche distribuée
platoons, schedule, utility = run_distributed_negotiation(vehicles)

# 3. Affichage propre des résultats
print(f"\n" + "="*50)
print(f"   RÉSULTATS : APPROCHE DISTRIBUÉE (V2V/V2I)")
print(f"="*50)
print(f"Nombre de véhicules           : {len(vehicles)}")
print(f"Nombre de pelotons négociés   : {len(platoons)}")
print(f"Utilité Sociale Globale       : {utility:.2f}")
print("-" * 50)

# On affiche les premiers résultats du planning
for p, start, end in schedule[:8]:
    type_v = "BUS" if p.priority == 2 else "CAR"
    print(f"[{type_v}] Peloton {p.leader.id} | Taille: {len(p.members)} | Passage: {start:.2f}s")

print("="*50)