import time
import sys
import threading
import os
import random

# DEPENDENCY NOTE: 
# This script runs on a simplified "Toy Model" of the GIO Engine.
# It simulates the Containment Field logic without the heavy 
# HDF5/Tensor overhead of arty_simulator.py.
#
# ==============================================================================
# ARTY_LIGHTSABER v4.0 (Stable Release)
# Logic: Boundary Confinement w/ Thread-Safe UI
# ==============================================================================

# ANSI Colors
C_GREEN = "\033[92m" # Real Mass
C_RED = "\033[91m"   # Imaginary Spin
C_CYAN = "\033[96m"  # The Containment Field
C_RESET = "\033[0m"

class KyberCrystal:
    def __init__(self):
        self.active = False
    
    def pulse(self):
        if self.active:
            # Emits Real Plasma (+1)
            return {"pos": 0.0, "vel": 1.0, "phase": "REAL", "type": "PLASMA"}
        return None

class NKST_ContainmentField:
    def __init__(self, max_length=24):
        self.max_length = max_length
        self.current_limit = 0 
        self.target_limit = 0
        
    def update_field_integrity(self):
        # The "Variable Geometry" logic
        if self.current_limit < self.target_limit:
            self.current_limit += 1
        elif self.current_limit > self.target_limit:
            self.current_limit -= 1
            
    def apply_boundary_logic(self, p):
        # -------------------------------------------------
        # (Vector Inversion)
        # -------------------------------------------------
        if p["pos"] >= self.current_limit:
            # 1. REFLECTION: Velocity Inverts
            p["vel"] = -1.0 
            
            # 2. TRANSFORMATION: Real Mass -> Imaginary Spin
            p["phase"] = "IMAGINARY" 
            p["type"] = "RECIRC"
            
            # 3. CLAMP: Lock to the Event Horizon
            p["pos"] = self.current_limit - 0.1
            return True
            
        # 4. RE-ABSORPTION: Energy returns to Hilt
        elif p["pos"] <= 0 and p["type"] == "RECIRC":
            p["type"] = "ABSORBED"
            return False
        return False

class Lightsaber:
    def __init__(self):
        self.crystal = KyberCrystal()
        self.field = NKST_ContainmentField()
        self.particles = []
        self.running = True
        self.state_label = "STANDBY"

    def toggle_power(self):
        if self.crystal.active:
            self.crystal.active = False
            self.field.target_limit = 0
            self.state_label = "RETRACTING"
        else:
            self.crystal.active = True
            self.field.target_limit = self.field.max_length
            self.state_label = "STABLE"

    def physics_tick(self):
        self.field.update_field_integrity()
        new_p = self.crystal.pulse()
        if new_p: self.particles.append(new_p)
            
        active_particles = []
        for p in self.particles:
            p["pos"] += p["vel"]
            self.field.apply_boundary_logic(p)
            if p["type"] != "ABSORBED":
                active_particles.append(p)
        self.particles = active_particles

    def render(self):
        sys.stdout.write("\033[K") # Clear Line
        
        # Draw Hilt
        hilt = f"{C_CYAN}[||||]{C_RESET}"
        
        # Draw Blade Buffer
        buffer = [" "] * (self.field.max_length + 5)
        
        # Populate Blade
        energy_density = 0
        for p in self.particles:
            idx = int(p["pos"])
            if 0 <= idx < len(buffer):
                # Green = Outbound, Red = Inbound
                char = "=" if p["phase"] == "REAL" else "~"
                color = C_GREEN if p["phase"] == "REAL" else C_RED
                buffer[idx] = f"{color}{char}{C_RESET}"
                energy_density += 1

        # Draw Tip (Event Horizon)
        if self.field.current_limit > 0:
            tip_idx = self.field.current_limit
            if tip_idx < len(buffer):
                buffer[tip_idx] = f"{C_CYAN}|{C_RESET}"

        blade_visual = "".join(buffer)
        
        # Dynamic Hum Text
        hum = "zZz" if energy_density > 5 else "..."
        
        # Final Composition
        print(f"\r{hilt}{blade_visual}  [{self.state_label}] {hum}", end="", flush=True)

def input_listener(saber):
    """Background thread waiting for ENTER key"""
    print(f"{C_CYAN}--- NKST PROTOCOL v4.0 ---{C_RESET}")
    print("Controls: [ENTER] to Toggle Blade  |  [Ctrl+C] to Quit")
    
    while saber.running:
        try:
            # Blocking call - waits for ENTER
            input() 
            if saber.running:
                saber.toggle_power()
        except EOFError:
            break

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    saber = Lightsaber()
    
    # Start Input Thread
    t = threading.Thread(target=input_listener, args=(saber,))
    t.daemon = True
    t.start()
    
    # Main Physics Loop
    try:
        while saber.running:
            saber.physics_tick()
            saber.render()
            time.sleep(0.04) # 25 FPS
    except KeyboardInterrupt:
        saber.running = False
        print(f"\n\n{C_CYAN}[SYSTEM] May the force be with you, always.{C_RESET}")
        sys.exit()
