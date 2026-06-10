import sys
import random
from anomaly_detection import GTOSAnomalyDetector

def run_blind_anomaly_test():
    detector = GTOSAnomalyDetector(baseline_threshold=3.5, window_size=5)
    test_sequence_length = 6
    last_report = {}
    
    # Generate an extended sequence track to engage the memory firewall
    random.seed()
    start_index = random.randint(10, 40)
    
    # Induce a slow, sustained memory bleed on the last few steps
    trigger_sustained_drift = random.choice([True, False])
    
    for step_offset in range(test_sequence_length):
        current_step = start_index + step_offset
        ideal_x, ideal_y, ideal_z = detector.calculate_ideal_node_position(current_step)
        
        # Apply data noise profile
        if trigger_sustained_drift and step_offset >= 3:
            # Incremental context drift under the 3.5 single-step threshold
            offset = 2.5
        else:
            # Fully stable data vectors
            offset = random.uniform(0.1, 0.5)
            
        simulated_coords = (ideal_x + offset, ideal_y - offset, ideal_z + (offset * 0.1))
        last_report = detector.evaluate_vector_drift(simulated_coords, current_step)

    # Build the double-blind challenge outputs
    real_distance = last_report["spatial_distance_delta"]
    rolling_momentum = last_report["rolling_momentum_velocity"]
    classification_bit = 1 if last_report["is_drifting"] else 0
    
    real_fingerprint = f"{real_distance:.6f}_{rolling_momentum:.6f}_{classification_bit}"
    fake_fingerprint_a = f"{(real_distance + 1.25):.6f}_{rolling_momentum:.6f}_{1 if classification_bit == 0 else 0}"
    fake_fingerprint_b = f"{real_distance:.6f}_{abs(rolling_momentum - 0.95):.6f}_{classification_bit}"
    
    options = [real_fingerprint, fake_fingerprint_a, fake_fingerprint_b]
    random.shuffle(options)
    
    print("=" * 60)
    print(f"[TEST] Evaluated sliding memory history stream ending at Step #{start_index + test_sequence_length - 1}.")
    print("=" * 60)
    print("\n👉 COPY AND PASTE THIS ENTIRE DECK STRING TO CHAT:")
    print("-" * 60)
    print(f"Deck: {options}")
    print("-" * 60)

if __name__ == "__main__":
    try:
        run_blind_anomaly_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] Integrated anomaly detector interface failed: {e}")
