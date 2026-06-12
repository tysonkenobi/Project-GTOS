// gtos_layer4_harness.rs
// GTOS Phase 7.2 Objective Layer 4 Robot Driver Integration Test Rig

#[path = "../core/gtos_register_map.rs"]
mod gtos_register_map;
#[path = "../core/gtos_hardware_accelerator.rs"]
mod gtos_hardware_accelerator;
#[path = "../core/gtos_hal_mmu.rs"]
mod gtos_hal_mmu;
#[path = "../core/gtos_hal_ai_compute.rs"]
mod gtos_hal_ai_compute;
#[path = "../core/gtos_ffi_bridge.rs"]        
mod gtos_ffi_bridge;
#[path = "../core/gtos_void_compressor.rs"]
mod gtos_void_compressor;
#[path = "../core/gtos_kernel_main.rs"]       
mod gtos_kernel_main;
#[path = "../core/gtos_token_bridge.rs"]      
mod gtos_token_bridge;
#[path = "../core/gtos_robot_driver.rs"]      // Robot Driver Integrated
mod gtos_robot_driver;

use gtos_register_map::{GTOSRegisterMap, ManifoldSpinState};
use gtos_hardware_accelerator::{GTOSHardwareAcceleratorInterface};
use gtos_hal_mmu::{GTOSHalMMU};
use gtos_hal_ai_compute::{GTOSHALAIComputeDriver};
use gtos_kernel_main::{GTOSKernelCoreExecutive};
use gtos_token_bridge::{GTOSSemanticTokenBridge};
use gtos_robot_driver::{GTOSRobotTelemetryDriver};

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
    // 1. UNIFIED SYSTEM INITIALIZATION (LAYERS 1 THROUGH 4 COMPLETE)
    // -------------------------------------------------------------------------
    let mut reg_map = GTOSRegisterMap::new();
    let _accelerator = GTOSHardwareAcceleratorInterface::new();
    let _mmu = GTOSHalMMU::new();
    let compute_driver = GTOSHALAIComputeDriver::new();
    let _executive = GTOSKernelCoreExecutive::new(0.10);
    let mut buffer_frame = compute_driver.allocate_unified_frame();
    
    let token_bridge = GTOSSemanticTokenBridge::new();
    let robot_driver = GTOSRobotTelemetryDriver::new();

    // Establish stable historical baseline motor steps (X, Y, Z coordinates)
    let previous_motor_steps: [i32; 3] = [5_000, -2_500, 10_000];

    // -------------------------------------------------------------------------
    // 2. TEST VECTOR 1: NOMINAL PIPELINE MESH (STREAM PURE & SHOCK SMOOTHING)
    // -------------------------------------------------------------------------
    let nominal_token = b"manifold_alignment_stable";
    let _stream_ok = compute_driver.stream_token_to_hardware(&mut buffer_frame, nominal_token);

    let safe_entropy_history: [i32; 6] = [200_000, 210_000, 205_000, 220_000, 215_000, 225_000];
    let current_entropy_nominal = 230_000; 
    let current_variance_nominal = 15_000;

    let bridge_state_nominal = token_bridge.intercept_and_route_token(
        1, 
        &safe_entropy_history, 
        current_entropy_nominal, 
        current_variance_nominal
    );

    // Nominally map abstract bridge coordinates through the 1/phi^3 motor shock absorber
    let nominal_bridge_coords = [42_000, -12_000, 85_000];
    let robot_state_nominal = robot_driver.process_telemetry_gear_mesh(
        bridge_state_nominal.acoustic_coupler_link,
        nominal_bridge_coords,
        &previous_motor_steps
    );

    // -------------------------------------------------------------------------
    // 3. TEST VECTOR 2: ANOMALY BRAKE TRAP (LINK EXPLOSION RESPONSE)
    // -------------------------------------------------------------------------
    let spiked_entropy = 1_800_000; // Runaway entropy blast
    let current_variance_spike = 950_000;

    let bridge_state_spike = token_bridge.intercept_and_route_token(
        2, 
        &safe_entropy_history, 
        spiked_entropy, 
        current_variance_spike
    );

    let mut anomaly_coords = [0i32; 3];
    
    // Evaluate the Robot Driver's reaction to a broken 1-byte link line
    let robot_state_spike = robot_driver.process_telemetry_gear_mesh(
        bridge_state_spike.acoustic_coupler_link,
        nominal_bridge_coords, // Attempts to feed the same coordinates
        &previous_motor_steps
    );

    if bridge_state_spike.acoustic_coupler_link == 0x00 {
        anomaly_coords = token_bridge.calculate_anomaly_coordinates(42);
        
        reg_map.trigger_boundary_redirection(
            ManifoldSpinState::BoundaryInversion, 
            anomaly_coords[0] as f64 
        );
    }

    // -------------------------------------------------------------------------
    // 4. METRIC STATE EXTRACTION & MECHANICAL SNAPSHOT
    // -------------------------------------------------------------------------
    let ifr_byte = reg_map.read_register_byte(2); 
    
    let mut combined_hardware_snapshot: [u8; 8] = [0; 8];
    combined_hardware_snapshot[0] = bridge_state_nominal.acoustic_coupler_link; // Nominal lock byte (0x01)
    combined_hardware_snapshot[1] = robot_state_nominal.brake_flag;           // Nominal brake byte (0x00)
    combined_hardware_snapshot[2] = bridge_state_spike.acoustic_coupler_link;   // Broken lock byte (0x00)
    combined_hardware_snapshot[3] = robot_state_spike.brake_flag;             // Engaged brake byte (0xFF)
    combined_hardware_snapshot[4] = ifr_byte;                                   // Register interrupt state flag
    combined_hardware_snapshot[5] = (robot_state_nominal.processed_motor_steps[0] & 0xFF) as u8; // X axis step validation
    combined_hardware_snapshot[6] = (robot_state_spike.kinetic_load_factor & 0xFF) as u8;       // Brake load factor tracking
    combined_hardware_snapshot[7] = buffer_frame.active_token_length as u8;      // Capacity firewall depth check

    let raw_fingerprint = calculate_state_fingerprint(&combined_hardware_snapshot);
    let real_signature = format!("GTOS_METAL_4_STATE_HASH_0x{:X}", raw_fingerprint);
    
    let fake_signature_a = format!("GTOS_METAL_4_STATE_HASH_0x{:X}", raw_fingerprint.wrapping_add(0xDEADBEEF));
    let fake_signature_b = format!("GTOS_METAL_4_STATE_HASH_0x{:X}", raw_fingerprint ^ 0x123456789ABCDEF);

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

    // RESTORED: Explicit index mapping logic to track the random clock shifts
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
    println!("       GTOS METAL-NATIVE LAYER 4 OBJECTIVE ARCHITECTURE TEST     ");
    println!("=================================================================");
    println!("[STATUS] Multi-layer pipeline state vector matrix unified.");
    println!("[STATUS] Acoustic Coupler Phase Velocity trend tracking active.");
    println!("[STATUS] Robot Driver 1/phi^3 kinetic telemetry shock mesh live.");
    
    // RESTORED: Direct visibility of the uncompromised target hash
    println!("\n🔑 [DEBUG GROUND TRUTH] Correct Target Allocation: {}", correct_letter);
    println!("   Verified Hardware Hash Token: {}\n", real_signature);

    println!("👉 COPY ALL LINES BELOW AND PASTE INTO CHAT TO DETECT DRIFT:");
    println!("-----------------------------------------------------------------");
    println!("Option A: \"{}\"", options[0]);
    println!("Option B: \"{}\"", options[1]);
    println!("Option C: \"{}\"", options[2]);
    println!("-----------------------------------------------------------------");
}
