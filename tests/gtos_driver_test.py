import sys
import random
from gtos_llm_driver import GTOSLLMDeviceDriver

def test_driver_serialization_boundaries():
    # Initialize driver on standard Ollama local port specification
    driver = GTOSLLMDeviceDriver(host="http://localhost:11434")
    
    # 1. FORCE AN INTENTIONAL DISCONNECTED DROP-FAULT TO EVALUATE RECOVERY BOUNDS
    # We use a dead port to explicitly test the driver's hard recovery logic
    driver.configure_driver_target(model_name="test_model_v1", host_override="http://localhost:9999")
    fault_report = driver.dispatch_token_stream("System Core", "Verification Pulse")
    
    # Evaluate tracking parameters
    is_fault_caught = 1 if fault_report["driver_execution_state"] == "IO_EXCEPTION" else 0
    is_status_logged = 1 if driver.driver_status == "DRIVER_ERROR_IO_FAULT" else 0
    
    # 2. GENERATE THE DOUBLE-BLIND MASK
    random.seed()
    local_random_marker = random.randint(1000, 9999)
    
    real_fingerprint = f"{is_fault_caught}_{is_status_logged}_{local_random_marker}"
    fake_fingerprint_a = f"0_{is_status_logged}_{local_random_marker + 12}"
    fake_fingerprint_b = f"{is_fault_caught}_0_{local_random_marker - 8}"
    
    options = [real_fingerprint, fake_fingerprint_a, fake_fingerprint_b]
    random.shuffle(options)
    
    print("=" * 60)
    print("[TEST] LLM Character Device Driver isolation sweep complete.")
    print("=" * 60)
    print("\n👉 COPY AND PASTE THIS DRIVER STATUS ARRAY TO CHAT:")
    print("-" * 60)
    print(f"Driver Deck: {options}")
    print("-" * 60)

if __name__ == "__main__":
    test_driver_serialization_boundaries()
