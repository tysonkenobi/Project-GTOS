// core/hardware_accelerator.rs
// GTOS Layer 1: Metal-Native Hardware Accelerator Driver
// Enforces the zero-degree-of-freedom Euler conjugate reality brake

#![no_std]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum AccelStatus {
    IdleHolding = 0x00,
    BoundaryEquilibriumReached = 0xCC, // Left side matches the Ricci right side exactly
    GeometricDivergenceTrapped = 0xFD,
    ComputeSuccessVectorReady = 0xAA,
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct GTOSAcceleratorControlBlock {
    pub command_trigger_flag: u8,
    pub active_manifold_state: i8,
    pub phase_velocity_link: u8,
    pub token_entropy_register: i32,  // Hardened to fixed-point i32 (4 bytes)
    pub token_variance_register: i32, // Hardened to fixed-point i32 (4 bytes)
}

pub struct GTOSHardwareAcceleratorInterface {
    pub register_footprint_bytes: usize,
}

impl GTOSHardwareAcceleratorInterface {
    // Constant definition of the right-side reality brake modifier: -(G * hbar / c^3)
    // Approximate raw Planck scale constant parameter used for boundary calculation
    pub const PLANCK_SCALE_FACTOR: i64 = -13564;

    pub const fn new() -> Self {
        Self { register_footprint_bytes: 11 }
    }

    pub fn map_metrics_to_hardware_bus(
        &self, 
        command_bit: u8, 
        manifold: i8,
        phase_link: u8, 
        entropy: i32, 
        variance: i32
    ) -> GTOSAcceleratorControlBlock {
        GTOSAcceleratorControlBlock {
            command_trigger_flag: command_bit,
            active_manifold_state: manifold,
            phase_velocity_link: phase_link,
            token_entropy_register: entropy,
            token_variance_register: variance,
        }
    }

    /// Processes a zero-degree-of-freedom constraint calculation.
    /// Compares the Left-Hand information matrix mapping against the Right-Hand Ricci Curve Tensor.
    pub fn enforce_boundary_constraint(
        &self,
        control_block: GTOSAcceleratorControlBlock,
        schwarzschild_metric: [i64; 16], // g_mu_nu (4x4)
        ricci_tensor: [i64; 16],         // R_mu_nu (4x4)
    ) -> AccelStatus {
        if control_block.command_trigger_flag != 0x01 {
            return AccelStatus::IdleHolding;
        }

        // Left Side Calculation: ln( Information Matrix / (1/phi^3) )
        // Using token entropy as our live informational variable input
        // Hardened: Cast the i32 entropy register up to i64 to safely support 64-bit multiplication steps
        let left_side_scalar = control_block.token_entropy_register as i64;

        // Hardened: Initialize tracking registers as clean, unpadded i64 integers
        let mut left_trace: i64 = 0;
        let mut right_trace: i64 = 0;
        let diagonals: [usize; 4] = [0, 5, 10, 15];

        for idx in 0..4 {
            let cell = diagonals[idx];
            // Corrected lines matching your parameters:
            left_trace = left_trace.saturating_add(left_side_scalar.saturating_mul(schwarzschild_metric[cell]));
            right_trace = right_trace.saturating_add(Self::PLANCK_SCALE_FACTOR.saturating_mul(ricci_tensor[cell]));
        }


        if left_trace >= right_trace {
            return AccelStatus::BoundaryEquilibriumReached;
        }

        // Hardened: Fixed-point barrier ceiling check equivalent to the old 2.5 float threshold
        if left_side_scalar > 2_500_000 {
            return AccelStatus::GeometricDivergenceTrapped;
        }

        AccelStatus::ComputeSuccessVectorReady
    }
}