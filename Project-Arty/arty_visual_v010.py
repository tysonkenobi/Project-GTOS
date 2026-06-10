import numpy as np
import h5py
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

#Visualization layer. Reads NKST telemetry exports and renders 
#the geodesic vortex funnel as an animated 3D spiral. Shows 
#infall and bounce phases with dynamic camera rotation.
#Not yet connected to GIO instability metrics.

def load_telemetry_data(filepath="./exports/nkst_telemetry.h5"):
    """Extracts raw simulation telemetry layers from the HDF5 archive."""
    target_path = Path(filepath).resolve()
    if not target_path.exists():
        raise FileNotFoundError(f"Telemetry missing at {target_path}. "
                                "Execute simulator pipeline first.")
    
    with h5py.File(target_path, "r") as f:
        data = {
            "time": np.array(f["time"]),
            "density_x": np.array(f["density_x"]),
            "metric_g": np.array(f["metric_g"]),
            "phase_spin": np.array(f["phase_spin"]),
            "kinetic_energy": np.array(f["kinetic_energy"])
        }
    return data
def play_vortex_funnel_simulation():
    data = load_telemetry_data()
    num_frames = len(data["time"])
    
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(11, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    fig.suptitle("NKST SPACE-TIME GEODESIC VORTEX FUNNEL", 
                 fontsize=13, color="#00ffcc", weight="bold", y=0.96)
    
    # --------------------------------------------------------------------------
    # MAP COORDINATES INTO A CYLINDRICAL FUNNEL EMBEDDING
    # --------------------------------------------------------------------------
    # 1. Z-Axis represents the physical depth of the funnel (Mass Density approach)
    z_funnel = data["density_x"]
    
    # 2. Radius (R) represents the metric tension scaling
    # As metric explodes near the boundary, the funnel narrows down to a tiny tip
    radius = 1.5 / (1.0 + np.log10(data["metric_g"] + 1.0))
    
    # 3. Angle (Theta) tracks the physical rotational kinetic energy spinning over time
    theta = np.cumsum(np.abs(data["phase_spin"]) * 1.5)
    
    # Transform Cylindrical coordinates (R, Theta, Z) into 3D Cartesian coordinates (X, Y, Z)
    x_funnel = radius * np.cos(theta)
    y_funnel = radius * np.sin(theta)
    
    # Find the exact moment of the bounce
    bounce_idx = int(np.argmax(z_funnel))
    
    # Initialize visual trace paths
    infall_spiral, = ax.plot(x_funnel[:bounce_idx+1], y_funnel[:bounce_idx+1], z_funnel[:bounce_idx+1],
                             color="#00e5ff", lw=2.5, alpha=0.9, label="Spinning In (Infall)")
    bounce_spiral, = ax.plot([], [], [], color="#ff5500", lw=3, alpha=0.9, label="Spinning Out (Bounce)")
    
    probe_point, = ax.plot([], [], [], 'o', color="#ffff00", ms=14, mec="white", zorder=10)
    
    # Configure grid geometry limits
    ax.set_xlabel("Manifold Coordinate Width ($X$)", color="#00e5ff", labelpad=10)
    ax.set_ylabel("Manifold Coordinate Depth ($Y$)", color="#ff0055", labelpad=10)
    ax.set_zlabel("System Mass Density ($R_{xx}$ Horizon Layer)", color="#ffff00", labelpad=10)
    
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_zlim(0.0, 1.2)
    
    # --------------------------------------------------------------------------
    # GENERATE A 3D TRUNCATED FUNNEL MESH WALL (The Boundary Horizon Target)
    # --------------------------------------------------------------------------
    z_mesh = np.linspace(0.0, 1.0, 30)
    theta_mesh = np.linspace(0, 2*np.pi, 30)
    ZM, TM = np.meshgrid(z_mesh, theta_mesh)
    
    # Build the funnel shape matching your boundary scaling physics
    # High density at the bottom = tiny tight throat radius
    RM = 1.5 * (1.0 - ZM * 0.85) 
    XM = RM * np.cos(TM)
    YM = RM * np.sin(TM)
    
    # Draw the translucent, wireframe boundary funnel sheet
    ax.plot_surface(XM, YM, ZM, color="#ff0055", alpha=0.04, edgecolor="#ff0055", lw=0.3)
    
    text_overlay = ax.text2D(0.03, 0.90, "", transform=ax.transAxes, 
                             color="#00e5ff", fontproperties={"family":"monospace"})
    # --------------------------------------------------------------------------
    # CORE INTERACTIVE UPDATE LOOP
    # --------------------------------------------------------------------------
    def update_frame(frame_idx):
        # 1. Animate the line history cutting through the funnel coordinates
        if frame_idx <= bounce_idx:
            infall_spiral.set_data(x_funnel[:frame_idx+1], y_funnel[:frame_idx+1])
            infall_spiral.set_3d_properties(z_funnel[:frame_idx+1])
            bounce_spiral.set_data([], [])
            bounce_spiral.set_3d_properties([])
        else:
            infall_spiral.set_data(x_funnel[:bounce_idx+1], y_funnel[:bounce_idx+1])
            infall_spiral.set_3d_properties(z_funnel[:bounce_idx+1])
            bounce_spiral.set_data(x_funnel[bounce_idx:frame_idx+1], y_funnel[bounce_idx:frame_idx+1])
            bounce_spiral.set_3d_properties(z_funnel[bounce_idx:frame_idx+1])
            
        # 2. Anchor tracking node particle
        probe_point.set_data([x_funnel[frame_idx]], [y_funnel[frame_idx]])
        probe_point.set_3d_properties([z_funnel[frame_idx]])
        
        # 3. Dynamic camera rotation pathing mimicking a slow descending flyby
        ax.view_init(elev=35 + 8 * np.sin(frame_idx / 15), azim=15 + frame_idx * 0.7)
        
        g_real = data["metric_g"][frame_idx]
        status = ">>> VORTEX EXPANSION CYCLE <<<" if frame_idx > bounce_idx else "--- ACCELERATING VORTEX COLLAPSE ---"
        if g_real > 10000:
            status = "!!! QUANTUM HORIZON INVERSION !!!"
            
        text_overlay.set_text(
            f"FRAME INDEX  : {frame_idx:03d} / {num_frames-1}\n"
            f"VORTEX DEPTH : {z_funnel[frame_idx]:.4f} / 1.0000\n"
            f"THROAT RADIUS: {radius[frame_idx]:.4f}\n"
            f"SPIN ENERGY  : {data['kinetic_energy'][frame_idx]:.2f}\n"
            f"FIELD STATE  : {status}"
        )
        return infall_spiral, bounce_spiral, probe_point, text_overlay

    print("[Engine] Booting up Geometric Vortex Funnel Window...")
    # interval controls presentation pace
    ani = FuncAnimation(fig, update_frame, frames=num_frames, interval=110, repeat=True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    play_vortex_funnel_simulation()
