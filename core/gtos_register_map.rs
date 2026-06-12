// core/register_map.rs
// GTOS Layer 1: Metal-Native Register Map
// Tracks complex boundary conjugations and manifold loop states

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum ManifoldSpinState {
    PositiveInComplex = 0xAA, 
    NegativeInComplex = 0xBB, 
    BoundaryInversion = 0xFF, 
}

pub struct GTOSRegisterMap {
    pub reg_base_addr: u16,
    pub register_byte_array: [u8; 8],
}

impl GTOSRegisterMap {
    pub const REG_CR0_STATUS: usize = 0x00;  
    pub const REG_IER_INTERRUPT: usize = 0x01; 
    pub const REG_IFR_FLAGS: usize = 0x02;    
    pub const REG_FVR_VAL: usize = 0x04;      

    pub const VECTOR_BOUNDARY_REDIRECTION: u32 = 0x0000_00A0;
    pub const VECTOR_SPATIAL_FIREWALL_BREACH: u32 = 0x0000_00B0;

    pub const fn new() -> Self {
        Self {
            reg_base_addr: 0x4000,
            register_byte_array: [0u8; 8],
        }
    }

    pub fn write_register_byte(&mut self, offset: usize, byte_value: u8) -> bool {
        if offset >= self.register_byte_array.len() { return false; }
        self.register_byte_array[offset] = byte_value;
        true
    }

    pub fn read_register_byte(&self, offset: usize) -> u8 {
        if offset >= self.register_byte_array.len() { return 0x00; }
        self.register_byte_array[offset]
    }

    pub fn trigger_boundary_redirection(&mut self, state: ManifoldSpinState, drift: i64) -> u32 {
        match state {
            ManifoldSpinState::BoundaryInversion => {
                self.write_register_byte(Self::REG_IFR_FLAGS, 0x03);
                let trunc = ((if drift < 0 { -drift } else { drift }) as u64 & 0xFF) as u8;
                self.write_register_byte(Self::REG_FVR_VAL, trunc);
                Self::VECTOR_BOUNDARY_REDIRECTION
            }
            _ => {
                self.write_register_byte(Self::REG_IFR_FLAGS, 0x05);
                Self::VECTOR_SPATIAL_FIREWALL_BREACH
            }
        }
    }
}
