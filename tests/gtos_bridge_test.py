import sys
import random
import numpy as np
from gtos_core_memory import GTOSKernelMemoryController
from gtos_token_bridge import GTOSTokenBridge

def run_blind_bridge_test():
    # Initialize the core systems
    memory = GTOSKernelMemoryController()
    bridge = GTOSTokenBridge(memory)
    
    # 1. GENERATE RANDOMIZED BLIND AI DATA STREAM TERMINOLOGY
    random.seed()
    stable_length = random.randint(5, 25)
    hallucination_length = random.randint(3, 10)
    total_tokens = stable_length + hallucination_length
    
    print("=" * 60)
    print(f"[TEST] Injecting {total_tokens} tokens into GTOSTokenBridge...")
    print("=" * 60)
    
    # Simulate highly structured, low-entropy logits (Stable AI)
    for i in range(stable_length):
        word_id = f"token_{i:03d}"
        # High confidence logit at index 0 makes this incredibly low entropy
        stable_logits = np.array([12.0, 0.2, 0.1, 0.05])
        bridge.intercept_and_route_token(word_id, stable_logits)
        
    # Simulate completely flat, high-entropy logits (Hallucination Spike)
    last_report = {}
    for j in range(hallucination_length):
        word_id = f"token_{stable_length + j:03d}"
        # Flat distribution mimics severe semantic drift / entropy breakdown
        chaotic_logits = np.array([2.0, 2.05, 1.98, 2.01])
        last_report = bridge.intercept_and_route_token(word_id, chaotic_logits)

    # 2. EXTRACT THE DIVERGENT VECTOR ADDRESS FOOTPRINT
    final_vector = last_report["assigned_coordinates"]
    
    print("\n[SUCCESS] Token Bridge parsed the stream and executed safety overrides.")
    print("-" * 60)
    print("👉 COPY AND PASTE THIS COORDINATE STRING TO THE CHAT:")
    print(f"   {final_vector}")
    print("-" * 60)

if __name__ == "__main__":
    try:
        run_blind_bridge_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] Token bridge interface failed: {e}")
