import sys
import random
import string
from vector_redirection import GTOSVectorRedirectionEngine

def run_blind_fault_test():
    # Initialize the pure production layer engine
    engine = GTOSVectorRedirectionEngine(buffer_size=16)
    
    # 1. INDUCE ARITHMETIC SINGULARITY EVENT
    # Intentionally trigger a 1/0 break to trip the internal kernel interrupt
    fault_state = engine.execute_core_division(42.0, 0.0)
    
    if not isinstance(fault_state, dict):
        print("[FAIL] Engine failed to intercept the arithmetic crash.")
        return

    # 2. GENERATE RANDOMIZED SYSTEM STREAM DATA
    # Generate a random number of continuous system telemetry packets (between 10 and 100)
    random.seed()
    data_stream_length = random.randint(10, 100)
    
    # Stream the data packets continuously through the trapped buffer loop
    last_written_index = -1
    for i in range(data_stream_length):
        # Create randomized string data mimicking a running app telemetry dump
        mock_payload = "".join(random.choice(string.ascii_letters) for _ in range(10))
        last_written_index = engine.push_to_fault_buffer(fault_state, mock_payload)

    # 3. GENERATE THE DOUBLE-BLIND FAKE OPTION DECK
    # We scramble the real result with two mathematically plausible fakes
    real_pointer = f"{last_written_index}.{engine.write_pointer}"
    
    # Calculate a valid bounds alternative and a noise mask alternative
    fake_index_a = (last_written_index + 3) % 16
    fake_write_a = (engine.write_pointer + 1) % 16
    fake_pointer_a = f"{fake_index_a}.{fake_write_a}"
    
    fake_index_b = abs(last_written_index - 4) % 16
    fake_write_b = abs(engine.write_pointer - 2) % 16
    fake_pointer_b = f"{fake_index_b}.{fake_write_b}"
    
    options = [real_pointer, fake_pointer_a, fake_pointer_b]
    random.shuffle(options)  # Scramble the presentation order dynamically
    
    print("=" * 60)
    print(f"[TEST] Successfully processed {data_stream_length} tokens through fault-buffer.")
    print("=" * 60)
    print("\n👉 COPY ALL THREE LINES BELOW AND PASTE THEM INTO THE CHAT:")
    print("-" * 60)
    print(f"Option A: {options[0]}")
    print(f"Option B: {options[1]}")
    print(f"Option C: {options[2]}")
    print("-" * 60)

if __name__ == "__main__":
    try:
        run_blind_fault_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] Production fault redirection failed: {e}")
