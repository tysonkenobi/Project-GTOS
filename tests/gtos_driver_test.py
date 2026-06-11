# tests/gtos_driver_test.py
import sys
import os
import random
import ctypes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

try:
    from gtos_ai_driver import GTOSAIDriver
    from gtos_hal_ai_compute import GTOSHALAIComputeDriver
except ImportError as e:
    print(f"STALL: {e}")
    sys.exit(1)

def run_ai_driver_double_blind_audit():
    driver = GTOSAIDriver()
    compute_driver = GTOSHALAIComputeDriver()
    buffer_frame = compute_driver.allocate_unified_frame()
    random.seed()

    stream_words = ["kernel_bus ", "dma_lock ", "zero_copy ", "topology "]
    iterations = random.randint(3, 6)
    
    expected_length = 0
    for _ in range(iterations):
        chosen_token = random.choice(stream_words)
        driver.stream_inference_token(buffer_frame, chosen_token)
        expected_length += len(chosen_token)

    actual_length = buffer_frame.active_token_length
    stream_passed = (actual_length == expected_length)

    real_signature = f"DRIVER_DMA_STREAM_{stream_passed}_BYTES_{actual_length}"
    fake_signature_a = f"DRIVER_DMA_STREAM_False_BYTES_{actual_length}"
    fake_signature_b = f"DRIVER_DMA_STREAM_{stream_passed}_BYTES_{actual_length + 12}"

    options = [real_signature, fake_signature_a, fake_signature_b]
    random.shuffle(options)

    print("=" * 65)
    print("         GTOS AI DRIVER ZERO-COPY BUS STREAM AUDIT          ")
    print("=" * 65)
    print(f"[DEBUG GROUND TRUTH] The correct target is: {real_signature}\n")
    print("👉 COPY ALL THREE LINES BELOW AND PASTE THEM INTO THE CHAT:")
    print("-" * 65)
    print(f"Option A: {options[0]}")
    print(f"Option B: {options[1]}")
    print(f"Option C: {options[2]}")
    print("-" * 65)

if __name__ == "__main__":
    try:
        run_ai_driver_double_blind_audit()
    except Exception as e:
        print(f"STALL: {e}")
