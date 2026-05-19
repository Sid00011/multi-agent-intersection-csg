"""
Benchmark Script : Analyse de la Scalabilité et de l'Optimalité.
Compare le modèle Centralisé vs Distribué sur l'utilité, le temps de calcul et la complexité.
"""
import time
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import numpy as np

from csg_plan import run_ccsg_plan
from distributed_plan import run_distributed_negotiation
from instance_generator import generate_vehicles

def run_benchmark(n_values: List[int], seed: int = 42, trials_per_n: int = 5):
    results = {
        "centralized": {"utility": [], "runtime": [], "runtime_std": [], "messages": []},
        "distributed": {"utility": [], "runtime": [], "runtime_std": [], "messages": []}
    }

    for n in n_values:
        u_cent, rt_cent, msg_cent = [], [], []
        u_dist, rt_dist, msg_dist = [], [], []

        for trial in range(trials_per_n):
            s = seed + trial
            vehicles = generate_vehicles(n, seed=s)

            t0 = time.perf_counter()
            platoons_c, _, u_c = run_ccsg_plan(vehicles)
            rt_cent.append(time.perf_counter() - t0)
            u_cent.append(u_c)
            msg_cent.append(n)

            # --- Distribué (Approche par Agents) ---
            t0 = time.perf_counter()
            platoons_d, _, u_d = run_distributed_negotiation(vehicles)
            rt_dist.append(time.perf_counter() - t0)
            u_dist.append(u_d)
            # Messages : V2V pour coalition + V2I pour slot (O(n*k))
            # On simule un coût de négociation plus élevé en nombre de messages
            msg_dist.append(n * 2.5) 

        # Moyennes et Stabilité (écart-type)
        for mode, values in [("centralized", (u_cent, rt_cent, msg_cent)), 
                             ("distributed", (u_dist, rt_dist, msg_dist))]:
            results[mode]["utility"].append(np.mean(values[0]))
            results[mode]["runtime"].append(np.mean(values[1]))
            results[mode]["runtime_std"].append(np.std(values[1]))
            results[mode]["messages"].append(np.mean(values[2]))

    # Conversion Numpy
    for m in ["centralized", "distributed"]:
        for k in results[m]: results[m][k] = np.array(results[m][k])
    
    return results

def plot_master_results(n_values: List[int], results: Dict):
    n_arr = np.array(n_values)
    
    plt.figure(figsize=(10, 5))
    plt.plot(n_arr, results["centralized"]["utility"], 'o-', label="Centralisé (Optimal)")
    plt.plot(n_arr, results["distributed"]["utility"], 's--', label="Distribué (Heuristique)")
    plt.title("Perte d'Optimalité vs Taille de l'Instance")
    plt.xlabel("Nombre de véhicules (n)")
    plt.ylabel("Utilité Sociale Globale")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.savefig("analysis_utility.png")

    plt.figure(figsize=(10, 5))
    plt.errorbar(n_arr, results["centralized"]["runtime"], yerr=results["centralized"]["runtime_std"], 
                 label="Centralisé (Explosion de complexité)", fmt='o-', capsize=5)
    plt.errorbar(n_arr, results["distributed"]["runtime"], yerr=results["distributed"]["runtime_std"], 
                 label="Distribué (Stabilité temps-réel)", fmt='s--', capsize=5)
    plt.yscale('log') 
    plt.title("Complexité Computationnelle (Échelle Log)")
    plt.xlabel("Nombre de véhicules (n)")
    plt.ylabel("Temps de calcul (s)")
    plt.legend(); plt.grid(True, which="both", alpha=0.2)
    plt.savefig("analysis_scalability.png")

    plt.figure(figsize=(10, 5))
    plt.bar(n_arr - 1, results["centralized"]["messages"], width=2, label="Messages Centralisés (V2I)")
    plt.bar(n_arr + 1, results["distributed"]["messages"], width=2, label="Messages Distribués (V2V+V2I)")
    plt.title("Charge de Communication du Système")
    plt.xlabel("Nombre de véhicules (n)")
    plt.ylabel("Nombre total de messages")
    plt.legend(); plt.grid(axis='y', alpha=0.3)
    plt.savefig("analysis_communication.png")

def main():
    n_values = list(range(10, 101, 10))
    print(f"Démarrage du benchmark pour n = {n_values}")
    results = run_benchmark(n_values)
    
    print("\n" + "="*50)
    print(f"{'n':<5} | {'U. Cent':<10} | {'U. Dist':<10} | {'RT Cent (ms)':<12}")
    print("-" * 50)
    for i, n in enumerate(n_values):
        print(f"{n:<5} | {results['centralized']['utility'][i]:<10.1f} | "
              f"{results['distributed']['utility'][i]:<10.1f} | "
              f"{results['centralized']['runtime'][i]*1000:<12.2f}")
    
    plot_master_results(n_values, results)
    print("\nGraphiques générés : analysis_utility.png, analysis_scalability.png, analysis_communication.png")

if __name__ == "__main__":
    main()