// core/gtos_ffi_bridge.rs
// GTOS Layer 2: Metal-Native Foreign Function Interface (FFI) Bridge
// Exposes 24-byte coordinate tensors and raw memory pointer addresses cleanly to C/Python runtimes

#![no_std]

use crate::gtos_hal_ai_compute::{GTOSUnifiedTokenBuffer};

/// Rigid 24-byte hardware metrics register structure.
/// Enforces absolute 1-byte packing to maintain exact alignment with the machine layout.
#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct GTOSHardwareRegisters {
    pub active_manifold: i32,     // 4 bytes
    pub system_load: i64,         // 8 bytes
    pub allocation_counter: u32,  // 4 bytes
    pub address_step_mult: i64,   // 8 bytes
} // Total: 4 + 8 + 4 + 8 = 24 bytes precisely

/// Rigid 24-byte coordinate vector layout tracking physical spatiotemporal tracks.
#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct GTOSCoordinatePayload {
    pub x: i64, // 8 bytes
    pub y: i64, // 8 bytes
    pub z: i64, // 8 bytes
} // Total: 8 + 8 + 8 = 24 bytes precisely

pub struct GTOSFFIBridge;

impl GTOSFFIBridge {
    /// Golden Ratio Constant (\phi = 1.6180339887...)
    pub const PHI: i32 = 1_618_034;
    
    /// Address step scaling factor tracking the inverse square: 1 / (\phi^2)
    /// This establishes your non-linear geometric compression step interval.
    pub const STEP_MULT: i32 = 381_966;
}

// -------------------------------------------------------------------------
// BARE-METAL INTEROPERABILITY EXPORT PIPELINES
// -------------------------------------------------------------------------

/// Native C-Export Interface: Populates and returns the 24-byte hardware register snapshot.
#[no_mangle]
pub extern "C" fn export_kernel_state_to_c(
    manifold: i32, 
    load: i64, 
    counter: u32
) -> GTOSHardwareRegisters {
    GTOSHardwareRegisters {
        active_manifold: manifold,
        system_load: load,
        allocation_counter: counter,
        address_step_mult: GTOSFFIBridge::STEP_MULT as i64,
    }
}

/// Zero-Copy Ingestion: Transmutes a raw byte stream pointer into an un-copied coordinate structure.
/// Direct memory cast protects against serialization performance overhead.
#[no_mangle]
pub unsafe extern "C" fn cast_bytes_to_vector_struct(
    raw_bytes_ptr: *const u8, 
    byte_len: usize
) -> GTOSCoordinatePayload {
    // Rigid safety assertion guard: input memory chunk size must match the 24-byte blueprint exactly
    if byte_len != 24 || raw_bytes_ptr.is_null() {
        return GTOSCoordinatePayload { x: 0, y: 0, z: 0 }; // Absolute fail-safe null return
    }

    // Cast the raw memory address pointer directly to the coordinate payload structure format
    let ptr = raw_bytes_ptr as *const GTOSCoordinatePayload;
    
    // Read the structure directly out of RAM memory via copy bitwise tracking
    core::ptr::read_unaligned(ptr)
}

/// In-Place DMA Tracking: Extracts the raw virtual memory pointer location of the active data 
/// segment, cleanly skipping the initial 8 bytes of control header tracking configurations.
#[no_mangle]
pub unsafe extern "C" fn get_token_payload_pointer(
    buffer_frame: *mut GTOSUnifiedTokenBuffer
) -> *mut u8 {
    if buffer_frame.is_null() {
        return core::ptr::null_mut(); // Protect against null pointer referencing faults
    }

    // Direct Pointer Offset Arithmetic: Step past the 8 bytes of headers (capacity and length fields)
    // to point directly to the raw byte character string segment array
    let raw_ptr = buffer_frame as *mut u8;
    raw_ptr.add(8)
}
