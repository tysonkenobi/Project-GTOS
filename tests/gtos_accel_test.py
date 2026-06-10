# tests/gtos_accel_test.py
import sys
import os
import random

# Enforce clean path routing to the core folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
from gtos_hardware_accelerator import GTOSHardwareAcceleratorInterface

def run_accelerator_double_blind_test():
    # 1. Instantiate the bare-metal hardware accelerator interface
    interface = GTOSHardwareAcceleratorInterface()
    
    # 2. Seed the randomizer and generate dynamic runtime metrics
    random.seed()
    command_bit = 1 # Active RUN state
    manifold_state = random.choice([1, -1])
    
    # Simulate a dynamic floating-point Shannon entropy value
    mock_entropy = round(random.uniform(0.5, 3.2), 4)
    mock_variance = round(random.uniform(0.01, 0.45), 4)
    
    # 3. Commit variables directly to the packed C structure registers
    control_block = interface.map_metrics_to_hardware_bus(
        command_bit=command_bit,
        manifold=manifold_state,
        entropy=mock_entropy,
        variance=mock_variance
    )
    
    # 4. Trigger the simulated execution cycle to extract the status flag
    execution_status = interface.trigger_npu_compute_cycle(control_block)
    
    # 5. Extract structural parameters to formulate the explicit ground truth
    # We create a secure string anchor using the runtime manifold and the exact entropy value
    real_signature = f"ACCEL_REG_M_{manifold_state}_E_{int(mock_entropy * 1000)}"
    
    # Compute randomized mathematically plausible fake register targets
    fake_entropy_a = int(abs(mock_entropy - random.uniform(0.2, 0.8)) * 1000)
    fake_signature_a = f"ACCEL_REG_M_{manifold_state}_E_{fake_entropy_a}"
    
    fake_entropy_b = int((mock_entropy + random.uniform(0.3, 0.9)) * 1000)
    fake_signature_b = f"ACCEL_REG_M_{-manifold_state}_E_{fake_entropy_b}"
    
    options = [real_signature, fake_signature_a, fake_signature_b]
    random.shuffle(options)
    
    print("=" * 65)
    print(" GTOS HARDWARE ACCELERATOR CONTROL REGISTER AUDIT ")
    print("=" * 65)
    print(f"[TEST] Packed C struct allocated size: {interface.register_footprint_bytes} bytes.")
    print(f"[TEST] Core execution system response: {execution_status}")
    
    # Explicit ground truth revealing key on your side
    print(f"[DEBUG GROUND TRUTH] The correct target is: {real_signature}\n")
    
    print("👉 COPY ALL THREE LINES BELOW AND PASTE THEM INTO THE CHAT:")
    print("-" * 65)
    print(f"Option A: {options[0]}")
    print(f"Option B: {options[1]}")
    print(f"Option C: {options[2]}")
    print("-" * 65)

if __name__ == "__main__":
    try:
        run_accelerator_double_blind_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] Hardware accelerator test failed: {e}")
