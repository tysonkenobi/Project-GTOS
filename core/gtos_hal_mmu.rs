// core/hal_mmu.rs
// GTOS Layer 1: Metal-Native Central Hardware Abstraction Layer MMU

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
    pub const PHI_BASE: i32 = 1_618_034;

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

    pub fn calculate_geometric_time_delta(&self, page_index: usize) -> i32 {
        if page_index >= self.oloid_page_pool.len() { return 0; }

        let distance = self.oloid_page_pool[page_index].boundary_distance_metric as i32;

        let compression_factor = 39_345;
        distance * compression_factor
    }

    pub fn resolve_oloid_address(
        &mut self, 
        reg_map: &mut GTOSRegisterMap, 
        page_index: usize, 
        requested_allocation: usize
    ) -> usize {
        if page_index >= self.oloid_page_pool.len() {
            reg_map.trigger_boundary_redirection(ManifoldSpinState::BoundaryInversion, 0);
            return 0; 
        }

        // --- PHASE 9: GEOMETRIC VOID ALIGNMENT ENFORCEMENT ---
        // Force the allocation size to snap to an unfragmented geometric boundary.
        // We use an 8-byte alignment barrier matching the Layer 3 translation gate.
        let alignment_barrier = 8;
        let geometric_aligned_allocation = (requested_allocation + (alignment_barrier - 1)) & !(alignment_barrier - 1);
        // -----------------------------------------------------

        let page = &mut self.oloid_page_pool[page_index];
        page.allocated_capacity_bytes = geometric_aligned_allocation;
        page.base_pointer_address
    }
}
