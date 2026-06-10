import sys
import random
import string
from gtos_core_memory import GTOSKernelMemoryController

def run_independent_stress_test():
    # Initialize the true kernel memory controller
    kernel = GTOSKernelMemoryController(boundary_threshold=0.10)
    
    # 1. GENERATE AN UNKNOWN BLIND DATA STREAM
    # We use a random seed so I have absolutely no way of guessing your dataset size
    random.seed() 
    dataset_length = random.randint(50, 150)
    
    print("=" * 60)
    print(f"[TEST] Injecting {dataset_length} randomized payloads into GTOS...")
    print("=" * 60)
    
    last_file_id = ""
    # Populate the kernel with completely random data lengths and strings
    for i in range(dataset_length):
        file_id = f"blind_block_{i:03d}"
        # Creates a random string of random length to generate chaotic structural entropy
        random_payload = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 500)))
        
        # Allocate the seed into the dual manifold
        kernel.allocate_file_seed(file_id, random_payload)
        last_file_id = file_id

    # 2. EXTRACT THE BLIND METRICS
    # We grab the final file's location to see exactly where the system ended up
    final_node = kernel.locate_file_seed(last_file_id)
    final_z = final_node["coordinate_vector"][2]
    
    print("\n[SUCCESS] GTOS completed processing without throwing errors or freezing!")
    print("-" * 60)
    print("👉 COPY AND PASTE THIS NUMBER TO THE CHAT:")
    print(f"   {final_z}")
    print("-" * 60)

if __name__ == "__main__":
    try:
        run_independent_stress_test()
    except Exception as e:
        print(f"\n[STALL DETECTED] System crashed or locked up: {e}")
