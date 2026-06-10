import sys
import random
from gtos_register_map import GTOSRegisterMap

def run_blind_register_test():
    reg_map = GTOSRegisterMap()
    
    # 1. SIMULATE AN ARITHMETIC EXCEPTION STATE
    random.seed()
    mock_failed_numerator = float(random.randint(10, 200))
    
    # 2. TRIGGER SYSTEM HANDSHAKE OVER LOGIC LINES
    target_vector = reg_map.trigger_hardware_interrupt("ZERO_DIVISION_FAULT", mock_failed_numerator)
    
    # 3. DIRECT REGISTRY INSPECTION
    flag_register_byte = reg_map.read_register_byte(reg_map.REG_IFR_FLAGS)
    saved_value_byte = reg_map.read_register_byte(reg_map.REG_FVR_VAL)
    
    print("=" * 60)
    print(f"[TEST] Verifying HAL Hardware Register Map Bit-Shifts...")
    print("=" * 60)
    print(f"Triggered Exception Input:  {mock_failed_numerator}")
    print(f"Fired CPU Interrupt Vector: {hex(target_vector)}")
    print(f"Flag Registry Byte Content: {bin(flag_register_byte)}")
    print(f"Saved Value Register Byte:  {saved_value_byte}")
    print("-" * 60)
    
    # Sanity check: Ensure bit flags and saved values match the input exactly
    if flag_register_byte == 0x03 and saved_value_byte == int(mock_failed_numerator):
        print("\n[SUCCESS] Hardware bit shifting and vector assignments validated!")
        print("-" * 60)
        print("👉 COPY AND PASTE THIS REGISTER CODE REgistry TAG:")
        
        local_random_id = random.randint(100, 999)
        real_tag = f"1_1_{local_random_id}"
        fake_tag_a = f"0_1_{local_random_id + 12}"
        fake_tag_b = f"1_0_{local_random_id - 8}"
        
        deck = [real_tag, fake_tag_a, fake_tag_b]
        random.shuffle(deck)
        print(f"Register Deck: {deck}")
        print("-" * 60)
    else:
        print("[FAIL] Register bit collision or memory corruption occurred.")

if __name__ == "__main__":
    try:
        run_blind_register_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] Register map lines failed to cycle: {e}")
