import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms  
import numpy as np
from csg_plan import run_ccsg_plan, GAP_BETWEEN_MEMBERS
from instance_generator import generate_vehicles


ROAD_LIMIT = 150
STOP_LINE = 40
LANE_OFFSET = 12 

def get_pos(v, t, t_start_platoon, idx_in_platoon):
    
    t_my_pass = t_start_platoon + (idx_in_platoon * GAP_BETWEEN_MEMBERS)
    
    offsets = {"N": (-LANE_OFFSET, 0), "S": (LANE_OFFSET, 0), 
               "E": (0, -LANE_OFFSET), "W": (0, LANE_OFFSET)}
    off_x, off_y = offsets[v.origin]
    
    if t < t_my_pass:
        d = max(STOP_LINE, v.position - (v.vitesse * t))
        if v.origin == "S": return (off_x, -d), 90
        if v.origin == "N": return (off_x, d), -90
        if v.origin == "E": return (d, off_y), 180
        if v.origin == "W": return (-d, off_y), 0
    
    t_after = t - t_my_pass
    d_cross = STOP_LINE - (25.0 * t_after)
    
    if v.origin == "S": return (off_x, -d_cross), 90
    if v.origin == "N": return (off_x, d_cross), -90
    if v.origin == "E": return (d_cross, off_y), 180
    if v.origin == "W": return (-d_cross, off_y), 0
    return (0,0), 0

def main():
    print("Correction appliquée. Lancement de la simulation...")
    vehicles = generate_vehicles(20, seed=42)
    platoons, schedule, total_u = run_ccsg_plan(vehicles)
    
    car_plans = {}
    for p, start, end in schedule:
        members = sorted(p.members, key=lambda x: x.ETA_naturel)
        for i, m in enumerate(members):
            car_plans[m.id] = (start, i)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('#34495e')
    ax.set_xlim(-ROAD_LIMIT, ROAD_LIMIT)
    ax.set_ylim(-ROAD_LIMIT, ROAD_LIMIT)
    
    ax.add_patch(mpatches.Rectangle((-30, -ROAD_LIMIT), 60, 2*ROAD_LIMIT, color='#95a5a6', zorder=0))
    ax.add_patch(mpatches.Rectangle((-ROAD_LIMIT, -30), 2*ROAD_LIMIT, 60, color='#95a5a6', zorder=0))
    ax.plot([0,0], [-ROAD_LIMIT, ROAD_LIMIT], 'w--', lw=2)
    ax.plot([-ROAD_LIMIT, ROAD_LIMIT], [0,0], 'w--', lw=2)

    patches = []
    for v in vehicles:
        color = '#f1c40f' if v.priorite == 2 else '#3498db'
        width, height = (14, 7) if v.priorite == 2 else (10, 5)
        rect = mpatches.Rectangle((0,0), width, height, fc=color, ec='black', zorder=10)
        ax.add_patch(rect)
        patches.append(rect)

    def update(frame):
        t = frame * 0.4
        for i, v in enumerate(vehicles):
            t_start, idx = car_plans[v.id]
            (x, y), angle = get_pos(v, t, t_start, idx)
            

            tr = mtransforms.Affine2D().rotate_deg_around(x, y, angle) + ax.transData
            patches[i].set_transform(tr)
            patches[i].set_xy((x - 5, y - 2.5))
            
        return patches

    ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
    plt.title(f"C-CSG-Plan LIRIS - Utilité: {total_u:.1f}", color='white', fontsize=15)
    
    save_name = "simulation_parfaite.gif"
    ani.save(save_name, writer='pillow')
    print(f"Succès ! Le fichier '{save_name}' a été généré sans erreur.")
    plt.show()

if __name__ == "__main__":
    main()