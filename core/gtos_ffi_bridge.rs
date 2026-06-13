// core/gtos_ffi_bridge.rs
// GTOS Layer 2: Metal-Native Foreign Function Interface (FFI) Bridge
// Exposes 24-byte coordinate tensors and raw memory pointer addresses cleanly to C/Python runtimes

use crate::gtos_hal_ai_compute::{GTOSUnifiedTokenBuffer};

/// Rigid 24-byte hardware metrics register structure.
/// Enforces absolute 1-byte packing to maintain exact alignment with the machine layout.
#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct GTOSHardwareRegisters {
    pub active_manifold: i32,     // 4 bytes
    pub system_load: i64,          // 8 bytes
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

    /// Phase 9.2: Maps and transforms a packed 11-byte Layer 1 control block 
    /// directly into a 24-byte co-processor coordinate target vector using 1/φ² scaling.
    #[no_mangle]
    pub unsafe extern "C" fn transmute_accelerator_block(
        control_block: crate::gtos_hardware_accelerator::GTOSAcceleratorControlBlock
    ) -> GTOSCoordinatePayload {
        let entropy_scalar = control_block.token_entropy_register as i64;
        let variance_scalar = control_block.token_variance_register as i64;

        // Scale registers using inverse square STEP_MULT (381_966)
        let scaled_x = entropy_scalar.saturating_mul(Self::STEP_MULT as i64);
        let scaled_y = variance_scalar.saturating_mul(Self::STEP_MULT as i64);
        
        GTOSCoordinatePayload {
            x: scaled_x,
            y: scaled_y,
            z: scaled_x ^ scaled_y, // Cross-layer structural validation bit
        }
    }
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

    // Direct Pointer Offset Arithmetic: Step past the 8 bytes of headers
    let raw_ptr = buffer_frame as *mut u8;
    raw_ptr.add(8)
}
