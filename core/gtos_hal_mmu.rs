// core/hal_mmu.rs
// GTOS Layer 1: Metal-Native Central Hardware Abstraction Layer MMU

#![no_std]

use crate::gtos_register_map::{GTOSRegisterMap, ManifoldSpinState};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OloidPhysicalPage {
    pub base_pointer_address: usize,
    pub allocated_capacity_bytes: usize,
    pub boundary_distance_metric: usize, 
}

pub struct GTOSHalMMU {
    pub oloid_page_pool: [OloidPhysicalPage; 4],
}

impl GTOSHalMMU {
    pub const PHI_BASE: f64 = 1.618033988749895;

    pub const fn new() -> Self {
        Self {
            oloid_page_pool: [
                OloidPhysicalPage { base_pointer_address: 0x8000, allocated_capacity_bytes: 0, boundary_distance_metric: 10 },
                OloidPhysicalPage { base_pointer_address: 0x9000, allocated_capacity_bytes: 0, boundary_distance_metric: 20 },
                OloidPhysicalPage { base_pointer_address: 0xA000, allocated_capacity_bytes: 0, boundary_distance_metric: 30 },
                OloidPhysicalPage { base_pointer_address: 0xB000, allocated_capacity_bytes: 0, boundary_distance_metric: 40 },
            ],
        }
    }

    pub fn calculate_geometric_time_delta(&self, page_index: usize) -> f64 {
        if page_index >= self.oloid_page_pool.len() { return 0.0; }
        let distance = self.oloid_page_pool[page_index].boundary_distance_metric as f64;
        let phi_cubed = Self::PHI_BASE * Self::PHI_BASE * Self::PHI_BASE;
        let compression_denominator = 6.0 * phi_cubed;
        distance / compression_denominator
    }

    pub fn resolve_oloid_address(
        &mut self, 
        reg_map: &mut GTOSRegisterMap, 
        page_index: usize, 
        requested_allocation: usize
    ) -> usize {
        if page_index >= self.oloid_page_pool.len() {
            reg_map.trigger_boundary_redirection(ManifoldSpinState::BoundaryInversion, 0.0);
            return 0; 
        }
        let page = &mut self.oloid_page_pool[page_index];
        page.allocated_capacity_bytes = requested_allocation;
        page.base_pointer_address
    }
}
