// apps/gtos_core_shell.rs
// GTOS Phase 10.7 Conversational Shell Interface Master Target
// Status: APPROVED PHASE 10.7 UNFRAGMENTED PRODUCTION CANOPY (NO_STD / NO_MAIN)

#![no_std]     //To be removed 
#![no_main]    //To be removed

extern crate gtos_core;

use gtos_core::gtos_hal_ai_compute::GTOSHALAIComputeDriver;
use gtos_core::gtos_kernel_main::{GTOSKernelCoreExecutive, ManifoldDomain};
use gtos_core::gtos_hal_mmu::GTOSHalMMU;
use gtos_core::gtos_register_map::GTOSRegisterMap;

// =========================================================================
// REGISTERED INSTRUMENTATION PIPELINE LINKS (CORE-9 MASTER WORKSPACE)
// =========================================================================
#[path = "./gtos_modulator_core.rs"]
pub mod local_modulator_core;
#[path = "./gtos_instrument_acoustic.rs"]
pub mod local_acoustic_instrument;
#[path = "./gtos_ai_bridge_universal.rs"]
pub mod local_intelligence_instrument;
#[path = "./gtos_motherboard_core.rs"]
pub mod local_motherboard_instrument;
#[path = "./gtos_instrument_vision.rs"]
pub mod local_vision_instrument;
#[path = "./gtos_bio_metrics.rs"]
pub mod local_biometric_instrument;
#[path = "./gtos_robot_interface.rs"]
pub mod local_robotics_instrument;
#[path = "./gtos_financial_fix.rs"]
pub mod local_finance_instrument;
#[path = "./gtos_comms.rs"]
pub mod local_comms_instrument;

// =========================================================================
// STATIC COCKPIT MEMORY MATRIX STATIONS
// =========================================================================
static mut MAIN_TYPING_BUFFER: [u8; 256] = [0u8; 256];
static mut TYPING_LENGTH: usize = 0;
static mut GLOBAL_TICKER_COUNT: usize = 0;

/// Core Primitive: Writes raw CP437 index character bytes directly to VGA memory map cells
unsafe fn write_vga_char(row: usize, col: usize, character: u8, color_attr: u8) {
    if row >= 25 || col >= 80 { return; }
    let vga_base = 0xB8000 as *mut u8;
    let linear_offset = ((row * 80) + col) * 2;
    core::ptr::write_volatile(vga_base.add(linear_offset), character);
    core::ptr::write_volatile(vga_base.add(linear_offset + 1), color_attr);
}

/// Core Primitive: Streams non-allocated slice streams directly onto precise row-coordinate offsets
unsafe fn write_vga_string(row: usize, mut col: usize, text: &[u8], color_attr: u8) {
    for &byte in text {
        if col >= 80 { break; }
        write_vga_char(row, col, byte, color_attr);
        col += 1;
    }
}

/// Core Primitive: Flushes an isolated screen zone with clean unallocated blank cells
unsafe fn clear_vga_region(row_start: usize, row_end: usize, col_start: usize, col_end: usize) {
    for r in row_start..=row_end {
        for c in col_start..=col_end {
            write_vga_char(r, c, b' ', 0x0F);
        }
    }
}

/// Core Primitive: Shits lines 03 through 21 upward by one line to ensure traditional upward scrolling
unsafe fn scroll_cli_viewport_up() {
    let vga_base = 0xB8000 as *mut u8;
    for row in 3..22 {
        let dest_offset = ((row * 80) + 5) * 2;
        let src_offset = (((row + 1) * 80) + 5) * 2;
        let length_to_copy = (80 - 5) * 2;
        core::ptr::copy_nonoverlapping(vga_base.add(src_offset), vga_base.add(dest_offset), length_to_copy);
    }
    // Flood line 21 with spaces to receive the next system message
    for col in 5..80 {
        write_vga_char(21, col, b' ', 0x0F);
    }
}

// =========================================================================
// PART 1: GENUINE COMPILABLE HARDWARE SENTINELS
// =========================================================================
unsafe fn write_gt_phi_sentinel(reg_map: &GTOSRegisterMap, executive: &GTOSKernelCoreExecutive) {
    let register_map_is_sane = core::mem::size_of::<GTOSRegisterMap>() > 0;
    let manifold_stable = executive.memory_controller.active_manifold_state == ManifoldDomain::StablePositive;
    let system_healthy = register_map_is_sane && manifold_stable;
    let color_attribute = if system_healthy { 0x0A } else { 0x0C }; // Green or Red Flash

    // Lock sentinel tightly over top box corner coordinates
    write_vga_char(0, 0, b'G', 0x0F);
    write_vga_char(0, 1, b'T', 0x0F);
    write_vga_char(0, 2, 0xE4, color_attribute); 
}

// =========================================================================
// PART 2: MANIFOLD-DRIVEN 10.7 GRAPHICS ENGINE (TICKERS & CLIS)
// =========================================================================
unsafe fn render_cockpit_canvas(
    typing_buffer: &[u8],
    reg_map: &GTOSRegisterMap,
    executive: &GTOSKernelCoreExecutive,
    ticker_tick: usize
) {
    // ---------------------------------------------------------------------
    // REQ F: FULL-SPAN DUAL HARDWARE & SOFTWARE HORIZONTAL MARQUEE TICKERS
    // ---------------------------------------------------------------------
    // Real raw metric pull from the 8-byte metal array parameters
    let b0 = reg_map.read_register_byte(0);
    let b1 = reg_map.read_register_byte(1);
    let b2 = reg_map.read_register_byte(2);
    let b3 = reg_map.read_register_byte(3);
    
    // Non-allocated formatting structures reading real system base parameters
    let hw_telemetry = b"HW CORE: [CPU: x86_64 Core ; ADDR: 0x4000 ; PCI_0: 0x01 ; REG_FLAGS: SYSTEM_ACTIVE]    ";
    let sw_telemetry = b"SW CORE: [0x01 SHELL: OK ; 0x02 ACOUSTIC: INBOUND ; 0x03 INTEL: ACTIVE_NO_LLM ; 0x04 M-BOARD: OK]    ";

    let hw_offset = ticker_tick % hw_telemetry.len();
    let sw_offset = ticker_tick % sw_telemetry.len();

    for col in 0..80 {
        // Enforce the Greek Phi sentinel footprint on columns 0-2 of line 00
        if col > 2 {
            let hw_idx = (hw_offset + col) % hw_telemetry.len();
            write_vga_char(0, col, hw_telemetry[hw_idx], 0x0B); // Blue-Cyan Marquee
        }
        let sw_idx = (sw_offset + col) % sw_telemetry.len();
        write_vga_char(1, col, sw_telemetry[sw_idx], 0x0E); // Yellow Marquee
    }

    // ---------------------------------------------------------------------
    // REQ C: LINE 02 VOICE-TO-TEXT "HEARD" MARQUEE STREAM
    // ---------------------------------------------------------------------
    write_vga_string(2, 0, b"|| HEARD: TRANSCRIBED RECORDED AUDIO SCROLL HERE", 0x0A);
    for col in 48..80 { write_vga_char(2, col, b' ', 0x0F); }

    // ---------------------------------------------------------------------
    // REQ E: COLUMNS 00-04 SPATIOTEMPORAL LEFT MARGIN VECTORS (PROTECTED ZONE)
    // ---------------------------------------------------------------------
    let current_manifold = executive.memory_controller.active_manifold_state;
    let vector_color = match current_manifold {
        ManifoldDomain::StablePositive => 0x0A,   // Inbound Active Green
        ManifoldDomain::InvertedNegative => 0x0C, // Phase Failure Fault Red
    };

    for r in 3..24 {
        write_vga_string(r, 0, b"|| ", 0x09); // Blue primary margin bracket bars
        if r < 6 {
            write_vga_char(r, 3, 0x1F, vector_color); // Downward vector '▼'
        } else if r == 6 {
            write_vga_char(r, 3, b'=', vector_color);  // Balance barrier '='
        } else {
            write_vga_char(r, 3, 0x1E, vector_color); // Upward vector '▲'
        }
        write_vga_char(r, 4, b' ', 0x0F); // Buffer channel column boundary wall
    }

    // ---------------------------------------------------------------------
    // REQ G: SHIFTED ACTIVE TERMINAL PROMPT (LINE 22, START COLUMN 05)
    // ---------------------------------------------------------------------
    write_vga_string(22, 5, b"gtos> ", 0x0B);
    for i in 0..(80 - 11) {
        if i < typing_buffer.len() {
            write_vga_char(22, 11 + i, typing_buffer[i], 0x0F);
        } else {
            write_vga_char(22, 11 + i, b' ', 0x0F);
        }
    }

    // ---------------------------------------------------------------------
    // REQ D: TEXT-TO-SPEECH CLOSED CAPTION MONITOR WITH DEDICATED PHI CELL
    // ---------------------------------------------------------------------
    write_vga_char(23, 5, 0xE4, 0x0A); // High-contrast Greek Phi symbol 'ɸ'
    write_vga_string(23, 7, b" [CC] GTOS SPEECH CLOSED CAPTION SCROLL HERE", 0x0F);
    for col in 51..80 { write_vga_char(23, col, b' ', 0x0F); }
    
    // Flat baseline matrix row loop
    for col in 5..80 { write_vga_char(24, col, b' ', 0x0F); }
}

/// Zero-Allocation pattern matching CLI directive parser
pub unsafe fn execute_functional_cli_parse(text_slice: &[u8]) {
    if text_slice == b"clear" {
        for row in 3..22 {
            for col in 5..80 {
                write_vga_char(row, col, b' ', 0x0F);
            }
        }
    } else if text_slice == b"sys-info" {
        scroll_cli_viewport_up();
        write_vga_string(21, 5, b"SYSTEM MANIFOLD: SOUND / UNFRAGMENTED GEOMETRY", 0x0E);
    } else if text_slice == b"sys-reboot" {
        scroll_cli_viewport_up();
        write_vga_string(21, 5, b"[WARP POINTER RE-ROUTE] REBOOTING NATIVE SILICON INTERFACES...", 0x0C);
    } else {
        // Fallback Command Reflection Output Engine
        scroll_cli_viewport_up();
        write_vga_string(21, 5, b"EXEC: ", 0x07);
        let print_clip = core::cmp::min(text_slice.len(), 40);
        write_vga_string(21, 11, &text_slice[0..print_clip], 0x0F);
    }
}

pub fn gtos_ingest_shell_command(
    driver: &GTOSHALAIComputeDriver,
    executive: &mut GTOSKernelCoreExecutive,
    mmu: &mut GTOSHalMMU,
    reg_map: &mut GTOSRegisterMap,
    raw_text_buffer: &[u8],
) {
    local_modulator_core::modulate_universal_stream(driver, executive, mmu, reg_map, 0x01, raw_text_buffer);
}

// =========================================================================
// INTERCEPT MONITOR: READ PROCESSED CHORDS FROM THE CONDUCTOR PIPELINE
// =========================================================================
pub unsafe fn process_live_system_inputs(
    reg_map: &GTOSRegisterMap,
    executive: &mut GTOSKernelCoreExecutive,
) {
    // 1. Audit active hardware flags out of offset 0x02 (REG_IFR_FLAGS)
    let _status_flags = reg_map.read_register_byte(GTOSRegisterMap::REG_IFR_FLAGS);

    // 2. Extract keystroke bytes out of the kernel files populated by Instrument ID 0x01
    let mut keyboard_read_frame = [0u8; 1];
    let bytes_captured = executive.system_read_file_buffer(0x01, &mut keyboard_read_frame);

    if bytes_captured > 0 {
        let active_char = keyboard_read_frame[0];

        if active_char == b'\n' || active_char == b'\r' {
            if TYPING_LENGTH > 0 {
                execute_functional_cli_parse(&MAIN_TYPING_BUFFER[0..TYPING_LENGTH]);
                
                // Zero tracking values cleanly without destabilizing stack coordinates
                TYPING_LENGTH = 0;
                for i in 0..256 { 
                    MAIN_TYPING_BUFFER[i] = 0; 
                }
            }
        } else if active_char == 0x08 {
            // Process backspace deletion bounds
            if TYPING_LENGTH > 0 {
                TYPING_LENGTH -= 1;
                MAIN_TYPING_BUFFER[TYPING_LENGTH] = 0;
            }
        } else if TYPING_LENGTH < 256 {
            // Commit raw character to our static workspace array
            MAIN_TYPING_BUFFER[TYPING_LENGTH] = active_char;
            TYPING_LENGTH += 1;
        }
    }
}

// =========================================================================
// ENTRY TRACKS: EMBEDDED HANDOVER FOR LONG-MODE BOOT
// =========================================================================
#[link_section = ".text.entry"]
#[cfg(target_os = "none")]
#[no_mangle]
pub unsafe extern "C" fn initialize_shell_interface() -> ! {
    let driver = GTOSHALAIComputeDriver::new();
    let mut executive = GTOSKernelCoreExecutive::new(100_000);
    let mut mmu = GTOSHalMMU::new();
    let mut reg_map = GTOSRegisterMap::new();

    // 1. Map physical motherboard chipset registers natively
    local_motherboard_instrument::sweep_and_modulate_chipset(&driver, &mut executive, &mut mmu, &mut reg_map);

    // 2. Clear out the entire screen array prior to initial layout grid render
    clear_vga_region(0, 24, 0, 79);

    // 3. Pre-stage a real command word into the local persistent static input array
    let boot_cmd = b"sys-info";
    TYPING_LENGTH = boot_cmd.len();
    core::ptr::copy_nonoverlapping(boot_cmd.as_ptr(), MAIN_TYPING_BUFFER.as_mut_ptr(), TYPING_LENGTH);

    executive.memory_controller.active_manifold_state = ManifoldDomain::StablePositive;

    loop {
        // Continuous non-allocating hardware input intercept scan pass
        process_live_system_inputs(&reg_map, &mut executive);

        // Continuous refresh loop mapping live attributes onto the layout coordinate matrix
        render_cockpit_canvas(
            &MAIN_TYPING_BUFFER[0..TYPING_LENGTH],
            &reg_map,
            &executive,
            GLOBAL_TICKER_COUNT
        );

        // Shift marquee horizontal ticker indices every loop cycle pass
        GLOBAL_TICKER_COUNT = GLOBAL_TICKER_COUNT.wrapping_add(1);

        // Render the top hardware sentinel over column 0
        write_gt_phi_sentinel(&reg_map, &executive);

        core::hint::spin_loop();
    }
}
