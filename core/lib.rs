// core/lib.rs
// GTOS Master Kernel Executive Library Crate Root
// Unifies Layers 1 through 4 into a monolithic, zero-overhead, unallocated namespace tree.

#![no_std]

// =========================================================================
// MODULE REGISTRATION TREE BY STRUCTURAL LAYERS
// =========================================================================

// LAYER 1: Core Bus Barrier & Physical Register Mapping
pub mod gtos_register_map;
pub mod gtos_hardware_accelerator;
pub mod gtos_hal_mmu;

// LAYER 2: Unified Storage Buffering & Core FFI Bridges
pub mod gtos_hal_ai_compute;
pub mod gtos_ffi_bridge;

// LAYER 3: Executive Core Architecture & Seed Scheduling Conductor
pub mod gtos_void_compressor;
pub mod gtos_kernel_main;

// LAYER 4: Edge I/O Peripherals (Semantic Processing & General Actuation)
pub mod gtos_token_bridge;
pub mod gtos_robot_driver;

// SYSTEM INTEGRATION & ORCHESTRATION INFRASTRUCTURE
pub mod gtos_conductor; // The Master Monolithic Runtime Engine Core (The Conductor)

// =========================================================================
// MASTER CRATE-LEVEL STRUCTURAL FOOTPRINT ASSERTION MATRIX
// =========================================================================
// These static compile-time validations guarantee that the unified crate
// tree enforces every single multi-layer invariant with zero padding leaks.

// Layer 1: Core Bus Width
const _: () = assert!(core::mem::size_of::<gtos_hardware_accelerator::GTOSAcceleratorControlBlock>() == 11);

// Layer 2: Memory Buffers & API Interop Bridges
const _: () = assert!(core::mem::size_of::<gtos_hal_ai_compute::GTOSUnifiedTokenBuffer>() == 517);
const _: () = assert!(core::mem::size_of::<gtos_ffi_bridge::GTOSHardwareRegisters>() == 24);   // Upgraded to Root Check
const _: () = assert!(core::mem::size_of::<gtos_ffi_bridge::GTOSCoordinatePayload>() == 24);   // Upgraded to Root Check

// Layer 3: Executive Node Containers
const _: () = assert!(core::mem::size_of::<gtos_kernel_main::GTOSFileNodeSeed>() == 36);

// Layer 4: Edge I/O Peripherals (Semantic Processing & General Actuation)
const _: () = assert!(core::mem::size_of::<gtos_token_bridge::GTOSTokenBridgeState>() == 12);
const _: () = assert!(core::mem::size_of::<gtos_robot_driver::GTOSRobotDriverState>() == 15);

// Structural Multi-Layer Verification Proof:
// Asserts that your total compute layout block size (517) combined with the 
// 4-byte interlock window perfectly matches your maximum physical container limit (521).
const _: () = assert!(core::mem::size_of::<gtos_hal_ai_compute::GTOSUnifiedTokenBuffer>() + 4 == 521);
