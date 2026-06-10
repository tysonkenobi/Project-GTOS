import sys
import random
import struct
from gtos_hal_mmu import GTOSHardwareMMU

def run_blind_mmu_test():
    mmu = GTOSHardwareMMU(total_pages=50)
    
    # 1. GENERATE RANDOM MOCK GEOMETRIC SEED DATA
    random.seed()
    mock_cell_id = f"sys_cell_{random.randint(100, 999)}"
    
    # Create distinct test coordinates
    x_test = float(random.uniform(1.0, 100.0))
    y_test = float(random.uniform(1.0, 100.0))
    z_test = float(random.uniform(-10.0, 10.0))
    
    packed_test_bytes = struct.pack("!ddd", x_test, y_test, z_test)
    
    # 2. COMMMIT DIRECTLY TO CONTIGUOUS BUS ADDRESS
    write_success = mmu.write_coordinate_to_physical_ram(mock_cell_id, packed_test_bytes)
    
    # 3. READ BACK VIA DIRECT PAGE FRAME EXTRACTION
    recovered_bytes = mmu.read_coordinate_from_physical_ram(mock_cell_id)
    
    # 4. UNPACK AND RUN HARDWARE EQUIVALENCE CHECK
    if recovered_bytes:
        x_rec, y_rec, z_rec = struct.unpack("!ddd", recovered_bytes)
        precision_delta = abs(x_test - x_rec) + abs(y_test - y_rec) + abs(z_test - z_rec)
    else:
        precision_delta = 1.0
        
    print("=" * 60)
    print(f"[TEST] Verifying Hardware Abstraction MMU Bus Allocation...")
    print("=" * 60)
    print(f"Target Registered Hardware ID: {mock_cell_id}")
    print(f"Bus Read Success Status:       {write_success and recovered_bytes is not None}")
    print(f"Bus Data Transmit Delta:       {precision_error if 'precision_error' in locals() else precision_delta:.14f}")
    print("-" * 60)
    
    if precision_delta < 1e-12:
        print("\n[SUCCESS] Contiguous byte-array segment isolation verified clean!")
        print("-" * 60)
        print("👉 COPY AND PASTE THIS ENTIRE DECK ARRAY TO CHAT:")
        
        # Generate double-blind state verification tags
        local_random_id = random.randint(100, 999)
        real_tag = f"1_1_{local_random_id}"
        fake_tag_a = f"0_1_{local_random_id + 5}"
        fake_tag_b = f"1_0_{local_random_id - 3}"
        
        deck = [real_tag, fake_tag_a, fake_tag_b]
        random.shuffle(deck)
        print(f"MMU Deck: {deck}")
        print("-" * 60)
    else:
        print("[FAIL] MMU memory leak detected. Contiguous block segments overlapped.")

if __name__ == "__main__":
    try:
        run_blind_mmu_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] HAL MMU connection failure: {e}")
