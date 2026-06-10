import sys
from gtos_kernel_main import GTOSKernelCoreExecutive
from gtos_ai_driver import GTOSAIDriver

def launch_gtos_terminal_shell():
    # Initialize the pure production kernel core executive and direct process driver
    kernel = GTOSKernelCoreExecutive()
    ai_driver = GTOSAIDriver()
    
    print("=" * 65)
    print(f" GTOS INTERACTIVE TERMINAL SHELL INTERFACE v1.0.0-Ready ")
    print("=" * 65)
    print("Available Core OS Commands:")
    print("  WRITE  [file_id] \"[payload]\" -> Serialize data to 24-byte seed")
    print("  READ   [file_id]            -> Reconstruct text payload from coordinate")
    print("  DIVIDE [num] [den]          -> Safe arithmetic fault check")
    print("  AI     [prompt]             -> Query local AI model natively")
    print("  STATUS                      -> Query manifold domain states")
    print("  EXIT                        -> Terminate shell loop")
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
                print(f" ↳ Core Executive State: {kernel.kernel_status}")
                print(f" ↳ Active Domain Sector: {domain}")
                print(f" ↳ Manifold Density Load: {kernel.memory.system_load:.6f} / {kernel.memory.BOUNDARY_LIMIT:.2f}")
                print(f" ↳ Allocated Cell Count: {kernel.memory.allocation_counter}")

            elif command == "WRITE":
                if '"' not in args_string:
                    print("[Shell Error] Syntax: WRITE [file_id] \"[payload text in quotes]\"")
                    continue
                file_id, text_payload = args_string.split('"', 1)
                file_id = file_id.strip()
                text_payload = text_payload.rsplit('"', 1)
                
                kernel.system_write_file(file_id, text_payload)
                print(f" ↳ [SUCCESS] Packed binary block committed successfully.")

            elif command == "READ":
                file_id = args_string.strip()
                recovered_text = kernel.system_read_file(file_id)
                if recovered_text is not None:
                    print(f" ↳ Reconstructed Output: \"{recovered_text}\"")
                else:
                    print(f" ↳ [File Error] Target node location '{file_id}' missing from tracking matrix.")

            elif command == "DIVIDE":
                num_str, den_str = args_string.split()
                n = float(num_str)
                d = float(den_str)
                
                execution_result = kernel.system_process_math(n, d)
                if isinstance(execution_result, dict):
                    print(f" ↳ {execution_result['status']}")
                else:
                    print(f" ↳ Calculation Success Vector: {execution_result}")

            # --- MILESTONE 2: PURE DIRECT PROCESS CONVERSATION LOOP ---
            elif command == "AI":
                prompt_text = args_string.strip()
                if not prompt_text:
                    print("[Shell Error] Syntax: AI [your question/prompt text]")
                    continue
                
                # Direct hardware execution via system memory pipes
                raw_response = ai_driver.bridge_prompt_to_tokens(prompt_text)
                
                # Silent background serialization down to our rigid 24-byte compression layer
                session_id = f"ai_session_{kernel.memory.allocation_counter:03d}"
                kernel.system_write_file(session_id, raw_response)
                
                # Display nothing but the clean, conversational text output block
                print(f"\n{raw_response}\n")

            else:
                print(f"[Shell Error] Instruction code '{command}' is non-existent in active kernel schema.")
                
        except Exception as e:
            print(f"[Core Error] Pipeline failure parsing command line: {e}")

if __name__ == "__main__":
    launch_gtos_terminal_shell()
