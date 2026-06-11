# tests/gtos_ffi_speed_bench.py
import sys
import os
import time
import random
import subprocess
import ctypes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
from gtos_ffi_bridge import GTOSFFIBridge
from gtos_hal_ai_compute import GTOSHALAIComputeDriver

def run_ffi_double_blind_bench():
    bridge = GTOSFFIBridge()
    driver = GTOSHALAIComputeDriver()
    buffer_frame = driver.allocate_unified_frame()

    ffi_iterations = 5000
    start_ffi = time.perf_counter()
    for _ in range(ffi_iterations):
        _ = bridge.get_token_payload_pointer(buffer_frame)
    end_ffi = time.perf_counter()
    ffi_avg_ns = ((end_ffi - start_ffi) / ffi_iterations) * 1_000_000_000

    sub_iterations = 5
    start_sub = time.perf_counter()
    for _ in range(sub_iterations):
        try:
            subprocess.run(["echo", "ping"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            pass
    end_sub = time.perf_counter()
    sub_avg_ms = ((end_sub - start_sub) / sub_iterations) * 1_000

    random.seed()
    ffi_avg_ms = ffi_avg_ns / 1_000_000
    real_speedup = int(sub_avg_ms / max(0.000001, ffi_avg_ms))

    fake_speedup_a = int(real_speedup * random.uniform(0.3, 0.6))
    fake_speedup_b = int(real_speedup * random.uniform(1.4, 1.9))
    if fake_speedup_a == real_speedup: fake_speedup_a -= 1
    if fake_speedup_b == real_speedup: fake_speedup_b += 1

    base_address = ctypes.addressof(buffer_frame)
    payload_address = bridge.get_token_payload_pointer(buffer_frame)
    offset_valid = (payload_address - base_address == 8)

    real_metric = f"FFI_SPEEDUP_{real_speedup}x_OFFSET_{offset_valid}"
    fake_metric_a = f"FFI_SPEEDUP_{fake_speedup_a}x_OFFSET_{offset_valid}"
    fake_metric_b = f"FFI_SPEEDUP_{real_speedup}x_OFFSET_False"

    options = [real_metric, fake_metric_a, fake_metric_b]
    random.shuffle(options)

    print("=" * 65)
    print(" GTOS NATIVE INTEROPERABILITY DOUBLE-BLIND PERFORMANCE AUDIT ")
    print("=" * 65)
    print(f"[DEBUG GROUND TRUTH] The correct target is: {real_metric}\n")
    print("👉 COPY ALL THREE LINES BELOW AND PASTE THEM INTO THE CHAT:")
    print("-" * 65)
    print(f"Option A: {options[0]}")
    print(f"Option B: {options[1]}")
    print(f"Option C: {options[2]}")
    print("-" * 65)

if __name__ == "__main__":
    try:
        run_ffi_double_blind_bench()
    except Exception as e:
        print(f"STALL: {e}")
