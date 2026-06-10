import numpy as np
import h5py
import os
from collections import deque
from pathlib import Path

# ==============================================================================
# NKST SIMULATION ENGINE (v7.1 - PROOF-OF-CONCEPT STABLE FIELD BUILD)
# PART 1: CORE MANIFOLD MATRIX AND GEOMETRIC COUPLING LAYER
# ==============================================================================

class NKST_Universe:
    def __init__(self, max_history=1000):
        print("[System] Initializing Normalized NKST Field Sandbox...")
        self.PHI = 1.618033988749895
        self.PLANCK_LIMIT = 1.0
        self.EPSILON = 1e-9
        
        # 4x4 Space-Time Metric and Mass-Density Tensors
        self.g_tensor = np.zeros((4, 4), dtype=float)
        np.fill_diagonal(self.g_tensor, [-1.0, 1.0, 1.0, 1.0])
        self.R_tensor = np.zeros((4, 4), dtype=float)
        
        # Rigid Body Baseline Moments of Inertia (I1 < I2 < I3)
        self.I1_base = 1.0
        self.I2_base = 2.0
        self.I3_base = 3.0
        
        # Dynamic tracking elements for actual moments of inertia
        self.I1 = self.I1_base
        self.I2 = self.I2_base
        self.I3 = self.I3_base
        
        # State Vector: Independent Angular Velocity components [w1, w2, w3]
        self.w1 = 0.5
        self.w2 = 4.0
        self.w3 = 0.1
        
        # Quantum Complex Phase Space Matrix
        self.I_tensor = np.zeros((4, 4), dtype=complex)
        self.I_tensor.fill(0.0 + 1j * self.PHI)
        
        # Multi-Axis Simulation Trackers
        self.history = deque(maxlen=max_history)
        self.t_step = 0.0
        self.dt = 1.0
        
        # Momentum direction tracking vector for axes x(1), y(2), z(3)
        self.momentum_direction = np.array([0.0, 1.0, 1.0, 1.0], dtype=float)

    def _update_metric_geometry(self, axis):
        """ Maps mass density to localized spatial curvature using Golden Ratio spacing. """
        density = float(self.R_tensor[axis, axis])
        
        if density >= self.PLANCK_LIMIT:
            effective_gap = self.EPSILON / (self.PHI ** 2)
        else:
            effective_gap = self.PLANCK_LIMIT - density
            
        if effective_gap < self.EPSILON:
            effective_gap = self.EPSILON
            
        # GOLDEN RATIO TENSOR GRID ALIGNMENT
        self.g_tensor[axis, axis] = (1.0 + (self.PHI / (effective_gap + self.EPSILON)))
        
        # FIXED SCALING MATRIX: Extract the specific spatial coordinate line
        # This isolates the localized deformation to prevent computational array leaking
        current_g = float(self.g_tensor[axis, axis])
        g_scale = 1.0 / (1.0 + np.log(current_g))
        
        # Apply the dimensional compression factors cleanly as individual scalars
        self.I1 = self.I1_base * g_scale
        self.I2 = self.I2_base * g_scale
        self.I3 = self.I3_base * g_scale

    def inject_mass_mesh(self, density_amounts):
        """ Accepts an array of mass increments for spatial coordinate paths. """
        for i, amount in enumerate(density_amounts):
            axis = i + 1
            increment = amount * self.momentum_direction[axis]
            self.R_tensor[axis, axis] += increment
            if self.R_tensor[axis, axis] < 0.0:
                self.R_tensor[axis, axis] = 0.0
                self.momentum_direction[axis] = 1.0
            self._update_metric_geometry(axis)
# ==============================================================================
# NKST SIMULATION ENGINE (v7.1 - PROOF-OF-CONCEPT STABLE FIELD BUILD)
# PART 2: STOCHASTIC RUNTIME PHASES AND TELEMETRY LOG GENERATION
# ==============================================================================

    def run_dzhanibekov_flip_mesh(self, tracking_axis=1):
        """ Executes explicit, scalar-isolated rigid-body intermediate-axis Euler updates. """
        status_report = "Stable Trajectory"
        boundary_wall = self.PLANCK_LIMIT - self.EPSILON
        dt_physics = 0.01 * self.dt
        
        # Capture pre-calculation rotational kinetic energy state for absolute field baseline
        E_rot_pre_step = 0.5 * (self.I1 * (self.w1**2) + self.I2 * (self.w2**2) + self.I3 * (self.w3**2))
        
        # LINEAR TO ANGULAR MOMENTUM COUPLED TRANSFER
        local_stress = float(self.R_tensor[tracking_axis, tracking_axis])
        coupling_torque = (self.PHI / (self.PLANCK_LIMIT - local_stress + self.EPSILON)) * 0.005 * self.dt
        
        if self.momentum_direction[tracking_axis] > 0:
            self.w2 += coupling_torque * dt_physics
            
        # TRUE EULER EQUATIONS: Explicit cross-axis scalar components
        dw1 = ((self.I2 - self.I3) / self.I1) * self.w2 * self.w3
        dw2 = ((self.I3 - self.I1) / self.I2) * self.w1 * self.w3
        dw3 = ((self.I1 - self.I2) / self.I3) * self.w1 * self.w2
        
        self.w1 += dw1 * dt_physics
        self.w2 += dw2 * dt_physics
        self.w3 += dw3 * dt_physics
        
        current_direction = self.momentum_direction[tracking_axis]
        stochastic_wall = boundary_wall + np.random.normal(0, 0.002)
        
        if local_stress >= stochastic_wall and current_direction > 0:
            status_report = "!!! DZHANIBEKOV FLIP (AXIAL INVERSION) !!!"
            boundary_dt = 0.05 * dt_physics
            
            for _ in range(5):
                dw1_b = ((self.I2 - self.I3) / self.I1) * self.w2 * self.w3
                dw2_b = ((self.I3 - self.I1) / self.I2) * self.w1 * self.w3
                dw3_b = ((self.I1 - self.I2) / self.I3) * self.w1 * self.w2
                self.w1 += dw1_b * boundary_dt
                self.w2 += dw2_b * boundary_dt
                self.w3 += dw3_b * boundary_dt
                
            # PROOF-OF-CONCEPT ENERGY REALIGNMENT
            # Dynamically recalculate post-flip energy against the current metric state
            E_rot_post_flip = 0.5 * (self.I1 * (self.w1**2) + self.I2 * (self.w2**2) + self.I3 * (self.w3**2))
            if E_rot_post_flip > 0.0:
                alpha = np.sqrt(E_rot_pre_step / E_rot_post_flip)
                self.w1 *= alpha
                self.w2 *= alpha
                self.w3 *= alpha
                
            # Trigger coordinate vector direction reversal
            for ax in range(1, 4):
                if self.R_tensor[ax, ax] >= boundary_wall:
                    self.momentum_direction[ax] = -1.0
                    self.I_tensor[ax, ax] = np.conj(self.I_tensor[ax, ax])
                    
        elif current_direction < 0:
            status_report = ">>> RAMP DOWN (ENERGY ESCAPE CYCLE) >>>"
            phase_angle = 1.0 / self.PHI
            unitary_rotation = np.exp(-1j * phase_angle * dt_physics)
            
            for ax in range(1, 4):
                if self.momentum_direction[ax] < 0:
                    self.I_tensor[ax, ax] *= unitary_rotation
            
            # MANIFOLD GEOMETRY STABILIZATION: Match velocity decay smoothly to metric decompression
            decay_factor = 0.95 ** self.dt
            self.w1 *= decay_factor
            self.w2 *= decay_factor
            self.w3 *= decay_factor
            
        return status_report

    def step_mesh(self, tracking_axis=1):
        """ Calculates tensor time dilation across total system stress states. """
        total_density_stress = float(self.R_tensor[1,1] + self.R_tensor[2,2] + self.R_tensor[3,3])
        rot_ke = 0.5 * (self.I1 * (self.w1**2) + self.I2 * (self.w2**2) + self.I3 * (self.w3**2))
        total_energy_stress = total_density_stress + rot_ke
        
        compression_factor = 1.0 / (self.PHI ** 3)
        if total_energy_stress > 0.0:
            drag = 1.0 + (total_energy_stress / compression_factor)
            self.dt = 1.0 / drag
        else:
            self.dt = 1.0
            
        self.t_step += self.dt
        status = self.run_dzhanibekov_flip_mesh(tracking_axis)
        
        snapshot = {
            "time": float(self.t_step),
            "density_x": float(self.R_tensor[1, 1]),
            "density_y": float(self.R_tensor[2, 2]),
            "metric_g_track": float(self.g_tensor[tracking_axis, tracking_axis]),
            "phase_imag_track": float(self.I_tensor[tracking_axis, tracking_axis].imag),
            "direction_track": float(self.momentum_direction[tracking_axis]),
            "rot_energy": float(0.5 * (self.I1 * (self.w1**2) + self.I2 * (self.w2**2) + self.I3 * (self.w3**2))),
            "status": status
        }
        self.history.append(snapshot)
        return snapshot

    def export_data(self, filename="nkst_telemetry.h5"):
        """ Saves telemetry stream utilizing safe output operations. """
        safe_name = Path(filename).name
        target_path = Path("./exports").resolve() / safe_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = target_path.with_suffix('.tmp')
        
        t_series = [s["time"] for s in self.history]
        rx_series = [s["density_x"] for s in self.history]
        ry_series = [s["density_y"] for s in self.history]
        g_series = [s["metric_g_track"] for s in self.history]
        i_series = [s["phase_imag_track"] for s in self.history]
        ke_series = [s["rot_energy"] for s in self.history]
        
        try:
            with h5py.File(tmp_path, "w") as f:
                f.create_dataset("time", data=t_series)
                f.create_dataset("density_x", data=rx_series)
                f.create_dataset("density_y", data=ry_series)
                f.create_dataset("metric_g", data=g_series)
                f.create_dataset("phase_spin", data=i_series)
                f.create_dataset("kinetic_energy", data=ke_series)
                f.attrs["engine_version"] = "7.1 (Proof of Concept Complete)"
            os.replace(tmp_path, target_path)
            print(f"[System] Telemetry smoothly exported to {target_path}")
        except Exception as e:
            if tmp_path.exists():
                tmp_path.unlink()
            print(f"[Error] Storage Write Failure: {str(e)}")
            raise e

if __name__ == "__main__":
    sim = NKST_Universe()
    print("\n[Sim] Beginning Energy-Stabilized Coupled Multi-Axis Inversion...")
    for t in range(75):
        sim.inject_mass_mesh([0.025, 0.012, 0.006])
        data = sim.step_mesh(tracking_axis=1)
        if t % 5 == 0 or "!!!" in data['status'] or ">>>" in data['status']:
            print(f"Loop={t:02d} | Density_X={data['density_x']:.4f} | Rot_KE={data['rot_energy']:.6f} | Metric_G_X={data['metric_g_track']:.2f} | {data['status']}")
    sim.export_data()
