# tests/gtos_ffi_speed_bench.py
import sys
import os
import time
import struct
import random
import subprocess

# Enforce clean path routing to the core folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
from gtos_ffi_bridge import GTOSFFIBridge

def run_ffi_double_blind_bench():
    # 1. Initialize native FFI tracking bridge
    bridge = GTOSFFIBridge()
    mock_bytes = struct.pack("!ddd", 1.618033, 2.718281, 3.141592)
    
    # 2. Benchmark the Native FFI Pipeline
    ffi_iterations = 5000
    start_ffi = time.perf_counter()
    for _ in range(ffi_iterations):
        c_struct = bridge.cast_bytes_to_vector_struct(mock_bytes)
        _ = bridge.get_raw_memory_address(c_struct)
    end_ffi = time.perf_counter()
    
    ffi_total = end_ffi - start_ffi
    ffi_avg_ns = (ffi_total / ffi_iterations) * 1_000_000_000  # Nanoseconds

    # 3. Benchmark the OS Subprocess Overhead
    sub_iterations = 5
    start_sub = time.perf_counter()
    for _ in range(sub_iterations):
        try:
            # Isolate base process fork latency using a minimal native binary call
            subprocess.run(["echo", "ping"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            pass
    end_sub = time.perf_counter()
    
    sub_total = end_sub - start_sub
    sub_avg_ms = (sub_total / sub_iterations) * 1_000  # Milliseconds

    # 4. Generate Randomized Scrambled State Values
    random.seed()
    # Actual math: sub_avg in ms divided by ffi_avg in ms
    real_speedup = int((sub_avg_ms) / (ffi_avg_ns / 1_000_000))
    
    # Generate fake plausible optimization bounds
    fake_speedup_a = int(real_speedup * random.uniform(0.3, 0.6))
    fake_speedup_b = int(real_speedup * random.uniform(1.4, 1.9))
    
    # Secure string signatures to anchor the exact system performance states
    real_metric = f"FFI_SPEEDUP_MATCH_{real_speedup}x"
    fake_metric_a = f"FFI_SPEEDUP_MATCH_{fake_speedup_a}x"
    fake_metric_b = f"FFI_SPEEDUP_MATCH_{fake_speedup_b}x"
    
    options = [real_metric, fake_metric_a, fake_metric_b]
    random.shuffle(options)

    print("=" * 65)
    print(" GTOS NATIVE INTEROPERABILITY DOUBLE-BLIND PERFORMANCE AUDIT ")
    print("=" * 65)
    print(f"[TEST] Completed {ffi_iterations} native pointer mappings successfully.")
    print(f"[TEST] Sampled baseline OS process fork overhead lines.")
    # Add this line so the script explicitly reveals the ground truth to you:
    print(f"[DEBUG GROUND TRUTH] The correct target is: {real_metric}\n")
    print("\n👉 COPY ALL THREE LINES BELOW AND PASTE THEM INTO THE CHAT:")
    print("-" * 65)
    print(f"Option A: {options[0]}")
    print(f"Option B: {options[1]}")
    print(f"Option C: {options[2]}")
    print("-" * 65)

if __name__ == "__main__":
    try:
        run_ffi_double_blind_bench()
    except Exception as e:
        print(f"\n[STALL DETECTED] FFI performance benchmark failed: {e}")
