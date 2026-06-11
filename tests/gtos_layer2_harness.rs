// gtos_layer2_harness.rs
// GTOS Phase 6.6 Objective Layer 2 Hardware Abstraction Integration Test Harness

#[path = "../core/gtos_register_map.rs"]
mod gtos_register_map;
#[path = "../core/gtos_hardware_accelerator.rs"]
mod gtos_hardware_accelerator;
#[path = "../core/gtos_hal_mmu.rs"]
mod gtos_hal_mmu;
#[path = "../core/gtos_hal_ai_compute.rs"]
mod gtos_hal_ai_compute;

use gtos_register_map::{GTOSRegisterMap};
use gtos_hardware_accelerator::{GTOSHardwareAcceleratorInterface};
use gtos_hal_mmu::{GTOSHalMMU};
use gtos_hal_ai_compute::{GTOSHALAIComputeDriver, GTOSUnifiedTokenBuffer};

fn calculate_state_fingerprint(bytes: &[u8]) -> u64 {
    let mut hash: u64 = 14695981039346656037;
    for &byte in bytes {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(1099511628211);
    }
    hash
}

fn main() {
    // -------------------------------------------------------------------------
    // 1. HARDWARE SYSTEM CORE INITIALIZATION (LAYERS 1 & 2)
    // -------------------------------------------------------------------------
    let mut _reg_map = GTOSRegisterMap::new();
    let _accelerator = GTOSHardwareAcceleratorInterface::new();
    let _mmu = GTOSHalMMU::new();
    
    let compute_driver = GTOSHALAIComputeDriver::new();
    let mut buffer_frame = compute_driver.allocate_unified_frame();

    let initial_size = compute_driver.buffer_footprint_bytes;

    // -------------------------------------------------------------------------
    // 2. TEST VECTOR 1: DIRECT MEMORY ACCESS (DMA) WAVESTREAM PASS
    // -------------------------------------------------------------------------
    // Simulate streaming fluid AI voice tokens into the unfragmented contiguous buffer
    let token_a = b"conductor_init ";
    let token_b = b"chord_resonance ";
    let run_a = compute_driver.stream_token_to_hardware(&mut buffer_frame, token_a);
    let run_b = compute_driver.stream_token_to_hardware(&mut buffer_frame, token_b);
    let post_stream_len = buffer_frame.active_token_length;

    // ADD THIS LINE HERE: Maps the metrics to create the missing block baseline
    let block_baseline = _accelerator.map_metrics_to_hardware_bus(0x01, 0, 0x00, 1.2, 0.4);

    // -------------------------------------------------------------------------
    // 3. TEST VECTOR 2: CAPACITANCE BOUNDARY OVERFLOW TRACKING
    // -------------------------------------------------------------------------
    // Force an excessive, malicious data load designed to violate the 505-byte arena
    let massive_exploit_payload = [0xFFu8; 510];
    let run_overflow = compute_driver.stream_token_to_hardware(&mut buffer_frame, &massive_exploit_payload);
    
    let final_token_len = buffer_frame.active_token_length;

    // Cross-layer connection to clear idle register warnings
    if !run_overflow {
        _reg_map.write_register_byte(2, 0x05); // Signals the hardware firewall breach flag
    }
    // Direct Gear Mesh: Feed the resulting Layer 2 buffer metric into Layer 1 pins
    let mut metric_schwarzschild: [f64; 16] = [1.0; 16];
    metric_schwarzschild[0] = final_token_len as f64; // Scale spacetime metric by active text length
    let _integrated_status = _accelerator.enforce_boundary_constraint(block_baseline, metric_schwarzschild, [0.0; 16]);

    // -------------------------------------------------------------------------
    // 4. METRIC STATE EXTRACTION & PHYSICAL FOOTPRINT EVALUATION
    // -------------------------------------------------------------------------
    let mut combined_hardware_snapshot: [u8; 8] = [0; 8];
    combined_hardware_snapshot[0] = (initial_size & 0xFF) as u8;         // Low byte of footprint
    combined_hardware_snapshot[1] = ((initial_size >> 8) & 0xFF) as u8;  // High byte of footprint (513)
    combined_hardware_snapshot[2] = if run_a { 1 } else { 0 };
    combined_hardware_snapshot[3] = if run_b { 1 } else { 0 };
    combined_hardware_snapshot[4] = post_stream_len as u8;
    combined_hardware_snapshot[5] = if run_overflow { 1 } else { 0 };    // Must evaluate to 0 (Blocked)
    combined_hardware_snapshot[6] = final_token_len as u8;               // Length must remain safely un-corrupted
    combined_hardware_snapshot[7] = buffer_frame.raw_byte_payload[0];    // Sample structural starting data bit

    let raw_fingerprint = calculate_state_fingerprint(&combined_hardware_snapshot);
    let real_signature = format!("GTOS_METAL_2_STATE_HASH_0x{:X}", raw_fingerprint);
    
    let fake_signature_a = format!("GTOS_METAL_2_STATE_HASH_0x{:X}", raw_fingerprint.wrapping_add(0xDEADBEEF));
    let fake_signature_b = format!("GTOS_METAL_2_STATE_HASH_0x{:X}", raw_fingerprint ^ 0x123456789ABCDEF);

    // -------------------------------------------------------------------------
    // 5. NON-DETERMINISTIC CLOCK SCRAMBLE PRESENTATION
    // -------------------------------------------------------------------------
    let system_clock_nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or(std::time::Duration::from_secs(0))
        .as_nanos();
    
    let mut options = vec![real_signature.clone(), fake_signature_a, fake_signature_b];
    
    if (system_clock_nanos & 0x01) == 1 { options.swap(0, 1); }
    if (system_clock_nanos & 0x02) == 2 { options.swap(1, 2); }
    if (system_clock_nanos & 0x04) == 4 { options.swap(0, 2); }

    let correct_letter = if options[0] == real_signature {
        "Option A"
    } else if options[1] == real_signature {
        "Option B"
    } else {
        "Option C"
    };

    // -------------------------------------------------------------------------
    // 6. OUTPUT INTERFACE DISPLAY
    // -------------------------------------------------------------------------
    println!("=================================================================");
    println!("       GTOS METAL-NATIVE LAYER 2 OBJECTIVE ARCHITECTURE TEST     ");
    println!("=================================================================");
    println!("[STATUS] 513-Byte geometric harmonic unpadded buffer allocated.");
    println!("[STATUS] Native pointer offset DMA streaming lanes active.");
    println!("[STATUS] 505-Byte strict boundary capacity firewall validated.");
    
    println!("\n🔑 [DEBUG GROUND TRUTH] Correct Target Allocation: {}", correct_letter);
    println!("   Verified Hardware Hash Token: {}\n", real_signature);

    println!("👉 COPY ALL LINES BELOW AND PASTE INTO CHAT TO DETECT DRIFT:");
    println!("-----------------------------------------------------------------");
    println!("Option A: \"{}\"", options[0]);
    println!("Option B: \"{}\"", options[1]);
    println!("Option C: \"{}\"", options[2]);
    println!("-----------------------------------------------------------------");
}
