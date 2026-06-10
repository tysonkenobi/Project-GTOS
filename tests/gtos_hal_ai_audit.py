# tests/gtos_hal_ai_audit.py
import sys
import os
import random

# Enforce clean path routing to the core folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
from gtos_hal_ai_compute import GTOSHALAIComputeDriver

def run_hal_ai_double_blind_audit():
    # 1. Instantiate the bare-metal abstract compute driver
    driver = GTOSHALAIComputeDriver()
    buffer_frame = driver.allocate_unified_frame()
    
    # 2. Seed the randomizer and determine a variable token test load
    random.seed()
    token_count = random.randint(15, 35)
    
    # 3. Stream a sequence of words to fill up the contiguous memory block
    stream_success = True
    total_chars_streamed = 0
    words_pool = ["manifold", "vector", "entropy", "shannon", "kernel", "quantum", "topology", "buffer", "matrix", "core"]
    
    for _ in range(token_count):
        mock_token = random.choice(words_pool) + " "
        total_chars_streamed += len(mock_token)
        # Attempt direct streaming to hardware buffer via DMA emulation
        status = driver.stream_token_to_hardware(buffer_frame, mock_token)
        if not status:
            stream_success = False
            break

    # 4. Extract metrics directly from the physical ctypes struct bytes
    final_bytes_used = buffer_frame.active_token_length
    remaining_bytes = buffer_frame.allocated_capacity - final_bytes_used
    
    # 5. Formulate the Double-Blind Verification Strings
    real_signature = f"AI_LEAK_TRACKER_USED_{final_bytes_used}_FREE_{remaining_bytes}"
    
    # Compute randomized mathematically plausible fake configurations
    fake_used_a = abs(final_bytes_used - random.randint(4, 12))
    fake_free_a = buffer_frame.allocated_capacity - fake_used_a
    fake_signature_a = f"AI_LEAK_TRACKER_USED_{fake_used_a}_FREE_{fake_free_a}"
    
    fake_used_b = final_bytes_used + random.randint(5, 15)
    fake_free_b = buffer_frame.allocated_capacity - fake_used_b
    fake_signature_b = f"AI_LEAK_TRACKER_USED_{fake_used_b}_FREE_{fake_free_b}"
    
    options = [real_signature, fake_signature_a, fake_signature_b]
    random.shuffle(options)
    
    print("=" * 65)
    print(" GTOS BARE-METAL AI COMPUTE UNIFIED MEMORY SYSTEM AUDIT ")
    print("=" * 65)
    print(f"[TEST] Streamed {token_count} active token loops onto the bus layer.")
    print(f"[TEST] Hardware buffer boundary checks enforced: {stream_success}")
    
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
        run_hal_ai_double_blind_audit()
    except Exception as e:
        print(f"\n[STALL DETECTED] Bare-metal AI allocation driver failed: {e}")
