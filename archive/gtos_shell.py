# core/gtos_shell.py
import sys
import ctypes
from gtos_kernel_main import GTOSKernelCoreExecutive
from gtos_ai_driver import GTOSAIDriver

def launch_gtos_terminal_shell():
    # Initialize the pure production kernel core executive and direct low-latency driver
    kernel = GTOSKernelCoreExecutive()
    ai_driver = GTOSAIDriver()

    print("=" * 65)
    print(f"       GTOS INTERACTIVE TERMINAL SHELL INTERFACE v1.3.0       ")
    print("=" * 65)
    print("Available Core OS Commands:")
    print("  WRITE [file_id] \"[payload]\" -> Serialize data to 24-byte seed")
    print("  READ [file_id] -> Reconstruct text payload from coordinate")
    print("  DIVIDE [num] [den] -> Safe arithmetic fault check")
    print("  VOICE -> Stream input characters natively to unified memory channel")
    print("  STATUS -> Query manifold domain states")
    print("  EXIT -> Terminate shell loop")
    print("=" * 65)

    while True:
        try:
            user_input = input("gtos_kernel_v1.0.0> ").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].upper()
            args_string = parts[1] if len(parts) > 1 else ""

            if command == "EXIT":
                print("[System] Shutting down GTOS shell loop interface. Goodbye.")
                break

            elif command == "STATUS":
                domain = "MANIFOLD_ALPHA (Universe A / i)" if kernel.memory.active_manifold_state == 1 else "MANIFOLD_BETA (Universe B / -i)"
                print(f"  ↳ Core Executive State: {kernel.kernel_status}")
                print(f"  ↳ Active Domain Sector: {domain}")
                print(f"  ↳ Manifold Density Load: {kernel.memory.system_load:.6f} / {kernel.memory.BOUNDARY_LIMIT:.2f}")
                print(f"  ↳ Allocated Cell Count: {kernel.memory.allocation_counter}")

            elif command == "WRITE":
                if '"' not in args_string:
                    print("[Shell Error] Syntax: WRITE [file_id] \"[payload text in quotes]\"")
                    continue
                file_id, text_payload = args_string.split('"', 1)
                file_id = file_id.strip()
                text_payload = text_payload.rsplit('"', 1)[0]
                kernel.system_write_file(file_id, text_payload)
                print(f"  ↳ [SUCCESS] Packed binary block committed successfully.")

            elif command == "READ":
                file_id = args_string.strip()
                recovered_text = kernel.system_read_file(file_id)
                if recovered_text is not None:
                    print(f"  ↳ Reconstructed Output: \"{recovered_text}\"")
                else:
                    print(f"  ↳ [File Error] Target node location '{file_id}' missing from tracking matrix.")

            elif command == "DIVIDE":
                num_str, den_str = args_string.split()
                n = float(num_str)
                d = float(den_str)
                execution_result = kernel.system_process_math(n, d)
                print(f"  ↳ Calculation Success Vector: {execution_result}")

            # --- MILESTONE 6.3: NATIVE STREAMING VOICE PARADIGM ---
            elif command == "VOICE":
                print("\n[CHANNEL OPEN] Streaming directly to 512-byte contiguous memory. Type '.' to end stream.\n")
                
                # Allocate a clean, rigid unpadded memory page via the hardware driver space
                buffer_frame = ai_driver.compute_driver.allocate_unified_frame()
                
                while True:
                    # Stream raw word segments or character sequences continuously
                    stream_input = input("voice_stream> ").strip()
                    if stream_input == ".":
                        print("[CHANNEL CLOSED] Stream committed cleanly to hardware bus.\n")
                        break
                    
                    if not stream_input:
                        continue
                        
                    # Append a trailing space to simulate natural speech word tokenization
                    token_chunk = stream_input + " "
                    
                    # Stream tokens directly onto the flat raw hardware buffer index offset
                    status = ai_driver.stream_inference_token(buffer_frame, token_chunk)
                    
                    if not status:
                        print("\n[HARDWARE FAULT] Buffer ceiling breached. Trapped safely.")
                        break

                # Silent background tracking: archive the final session data buffer layout
                session_id = f"ai_session_{kernel.memory.allocation_counter:03d}"
                raw_payload_text = ai_driver.compute_driver.read_clean_payload(buffer_frame)
                kernel.system_write_file(session_id, raw_payload_text)

            else:
                print(f"[Shell Error] Instruction code '{command}' is non-existent in active kernel schema.")

        except Exception as e:
            print(f"[Core Error] Pipeline failure parsing command line: {e}")

if __name__ == "__main__":
    launch_gtos_terminal_shell()
