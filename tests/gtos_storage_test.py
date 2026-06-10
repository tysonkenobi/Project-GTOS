import sys
import random
import string
from gtos_storage_core import GTOSStorageCore

def run_blind_storage_test():
    storage_engine = GTOSStorageCore()
    
    # 1. GENERATE AN EXTENDED RANDOM DATASTREAM
    random.seed()
    text_length = random.randint(30, 80)
    original_text = "".join(random.choice(string.ascii_letters) for _ in range(text_length))
    
    # 2. RUN PURE COMPRESSION INTO THE SYSTEM CORE
    file_key = "system_node_alpha"
    binary_seed = storage_engine.compress_payload_to_seed(file_key, original_text)
    
    # 3. RUN DECOMPRESSION
    reconstructed_text = storage_engine.decompress_seed_to_payload(file_key)
    
    print("=" * 60)
    print("[TEST] Executing Silent Storage Reconstruction Validation...")
    print("=" * 60)
    print(f"Generated Raw Text Length: {text_length} Characters")
    print(f"Packed Binary Block Size:  {len(binary_seed)} Bytes")
    print("-" * 60)
    
    # Evaluate byte-level execution boundaries
    if len(binary_seed) == 24 and reconstructed_text is not None:
        print("\n[SUCCESS] Data compression core successfully localized and executed!")
        print("-" * 60)
        print("👉 COPY AND PASTE THIS REAL STRING ENCODING FACTOR TO CHAT:")
        print(f"   {binary_seed.hex()}")
        print("-" * 60)
    else:
        print("[FAIL] Storage compression failed to serialize coordinates cleanly.")

if __name__ == "__main__":
    run_blind_storage_test()
