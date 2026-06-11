import sys
import random
from trajectory_snapping import GTOSTrajectorySnapper

def run_blind_snapping_test():
    snapper = GTOSTrajectorySnapper()
    
    # Prime the safe context cache
    snapper.register_safe_state("System Configuration Complete")
    snapper.register_safe_state("Manifold Alpha Ingestion Running Stable")
    
    # Simulate a randomized firewall action
    random.seed()
    trigger_firewall_violation = random.choice([True, False])
    
    if trigger_firewall_violation:
        mock_firewall_report = {"classification": "BOUNDS_VIOLATION_DETECTED"}
        input_payload = "CHAOTIC_HALLUCINATION_MATRIX_DRIFT_OVERDRIVE"
    else:
        mock_firewall_report = {"classification": "BOUNDS_NORMAL"}
        input_payload = "Verification data block processed pure"
        
    # Execute the production data scrub filter
    sanitized_output = snapper.scrub_and_snap_payload(input_payload, mock_firewall_report)
    
    # Strict validation mapping
    is_snapped = 1 if sanitized_output == "Manifold Alpha Ingestion Running Stable" else 0
    is_reset = 1 if sanitized_output == "RECOVERY_FALLBACK_CORE_RESET" else 0
    is_passed_through = 1 if sanitized_output == "Verification data block processed pure" else 0
    
    local_random_id = random.randint(100, 999)
    real_fingerprint = f"{is_snapped}_{is_reset}_{is_passed_through}_{local_random_id}"
    
    # Generate true mathematical alternative masks
    fake_fingerprint_a = f"{1 if is_snapped == 0 else 0}_{is_reset}_0_{local_random_id + 7}"
    fake_fingerprint_b = f"0_{1 if is_reset == 0 else 0}_{is_passed_through}_{local_random_id - 4}"
    
    options = [real_fingerprint, fake_fingerprint_a, fake_fingerprint_b]
    random.shuffle(options)
    
    print("=" * 60)
    print(f"[TEST] Evaluated production trajectory data scrubber pipeline.")
    print("=" * 60)
    print("\n👉 COPY AND PASTE THIS ENTIRE DECK STRING TO CHAT:")
    print("-" * 60)
    print(f"Snapper Deck: {options}")
    print("-" * 60)

if __name__ == "__main__":
    try:
        run_blind_snapping_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] Snapper validation interface connection failed: {e}")
