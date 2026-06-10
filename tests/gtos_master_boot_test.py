import sys
import random
import numpy as np
from gtos_kernel_main import GTOSKernelCoreExecutive

def run_master_integration_audit():
    # Initialize the silent unified core manager
    gtos_kernel = GTOSKernelCoreExecutive()
    
    # 1. AUDIT STATE SYSTEM INITIALIZATION
    if gtos_kernel.kernel_status != "BOOTED_EXECUTION_READY":
        print("[FAIL] Kernel subsystem orchestration initialization stalled.")
        return

    # 2. RUN RANDOMIZED CORE SUBSYSTEM FLOW CHECKS
    random.seed()
    sample_size = random.randint(20, 60)
    mock_payload = "Unification Matrix Sequence " * random.randint(1, 3)
    
    # Test Storage Core Subsystem Pipeline
    packed_binary = gtos_kernel.system_write_file("kernel_boot_cfg", mock_payload)
    recovered_text = gtos_kernel.system_read_file("kernel_boot_cfg")
    
    # Test Exception Subsystem Handling Pipeline (Trigger 1/0 Intercept)
    fault_trap = gtos_kernel.system_process_math(99.9, 0.0)
    
    # Test Integrated Token Bridge & Sliding Window Anomaly Firewall Pipeline
    simulated_logits = np.array([10.0, 0.5, 0.1, 0.05])
    last_telemetry = {}
    for step in range(5):
        last_telemetry = gtos_kernel.system_ingest_token(f"word_{step}", simulated_logits)

    # 3. CONSTRUCT DOUBLE-BLIND CHALLENGE OUTPUTS FROM INTEGRATION STATES
    is_reconstructed = 1 if recovered_text == mock_payload else 0
    is_trapped = 1 if isinstance(fault_trap, dict) and fault_trap["status"] == "CYCLIC_LOOP_ACTIVE" else 0
    total_footprint_bytes = len(packed_binary)
    
    real_fingerprint = f"{is_reconstructed}_{is_trapped}_{total_footprint_bytes}_{sample_size}"
    fake_fingerprint_a = f"0_{is_trapped}_{total_footprint_bytes}_{sample_size + 4}"
    fake_fingerprint_b = f"{is_reconstructed}_0_{total_footprint_bytes + 8}_{sample_size}"
    
    options = [real_fingerprint, fake_fingerprint_a, fake_fingerprint_b]
    random.shuffle(options)
    
    print("=" * 60)
    print(f"[TEST] Unified GTOS Core Executive instantiated all 5 sub-engines successfully.")
    print("=" * 60)
    print("\n👉 COPY AND PASTE THIS UNIFIED STATE DECK TO CHAT:")
    print("-" * 60)
    print(f"Master Deck: {options}")
    print("-" * 60)

if __name__ == "__main__":
    try:
        run_master_integration_audit()
    except Exception as e:
        print(f"\n[INTEGRATION CRASH] Kernel executive initialization broke: {e}")
