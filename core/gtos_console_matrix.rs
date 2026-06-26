// core/gtos_console_matrix.rs (Part 1 of 2)
// GT-OS Layer 4 Core Ingestion Asset - Matrix Layout Configurations

#![no_std]

// =========================================================================
// HARDWARE MODIFIER BITMASKS & SOUND SYSTEM REGISTER SETTINGS
// =========================================================================
pub const MASK_LEFT_SHIFT: u8  = 0x01;
pub const MASK_RIGHT_SHIFT: u8 = 0x02;
pub const MASK_CTRL: u8        = 0x04;
pub const MASK_ALT: u8         = 0x08;
pub const MASK_META: u8        = 0x10;
pub const MASK_META_MIC: u8    = 0x20; // Acoustic Instrument Gate Trigger
pub const SETTING_MIC_PTT: u8  = 0x40; // Push-To-Talk Toggle Selector State
pub const MASK_EXTENDED_E0: u8 = 0x80; // Extended prefix tracking flag

// =========================================================================
// STRUCTURAL CONTAINER LAYOUT PROFILES
// =========================================================================
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum MatrixLayoutProfile {
    StandardQWERTY = 0x00,
    StandardAZERTY = 0x01,
    StandardQWERTZ = 0x02,
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct TriadCommandState {
    pub active_modifier_bitmask: u8,
    pub break_gate_tripped: u8,
    pub acoustic_entropy_scalar: i32,
    pub acoustic_variance_scalar: i32,
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct GTOSLayer5UXTracking {
    pub cursor_x: u8,
    pub cursor_y: u8,
    pub token_counter: u16,
    pub clipboard_cache: [u8; 48],

    // =========================================================================
    // LAYER 5 PLUG-AND-PLAY ACCESSIBILITY & SECURITY GATEWAY (11-BYTE GATEWAY)
    // =========================================================================
    // Multi-purpose 11-byte gateway serving three distinct operational modes:
    // Mode 1 (Security Wall): 11-Byte Rolling Attestation Hash & Cycle Signature
    // Mode 2 (Hardware Auth): Phase-Velocity Chord Gate Microsecond Jitter Tracker
    // Mode 3 (State Isolation): Layer 5 Telemetry Anchor Permission Flags
    pub security_gateway_block: [u8; 11],
}

#[repr(C, packed)]
#[derive(Debug, Clone, Copy)]
pub struct GTOSConsoleMatrixState {
    pub last_processed_signal: u8,
    pub modifier_mask: u8,
    pub active_profile: MatrixLayoutProfile,
    pub triad_state: TriadCommandState,
    pub ux_tracking: GTOSLayer5UXTracking, // Natively nested tracking component
}

// core/gtos_console_matrix.rs (Refined Implementation TBD)
impl GTOSConsoleMatrixState {
    /// Factory constructor defining a baseline layout profile
    pub const fn new(profile: MatrixLayoutProfile) -> Self {
        Self {
            last_processed_signal: 0,
            modifier_mask: 0,
            active_profile: profile,
            triad_state: TriadCommandState {
                active_modifier_bitmask: 0,
                break_gate_tripped: 0,
                acoustic_entropy_scalar: 0,
                acoustic_variance_scalar: 0,
            },
            ux_tracking: GTOSLayer5UXTracking {
                cursor_x: 0,
                cursor_y: 0,
                token_counter: 0,
                clipboard_cache: [0; 48],
                security_gateway_block: [0; 11],
            },
        }
    }

    pub fn transform_silicon_signal(&mut self, port: u16, signal_byte: u8) -> Option<u8> {
        if port == 0x0060 { return
            self.decode_laptop_scancode(signal_byte); }
            return None
        }

    pub fn decode_laptop_scancode(&mut self, scancode: u8) -> Option<u8> {
        // Track the extended prefix state as a pseudo-modifier bit flag
        if scancode == 0xE0 {
            self.modifier_mask |= 0x80; // Use high bit of mask as E0 indicator
            return None;
        }

        if scancode == self.last_processed_signal {
            return None;
        }
        self.last_processed_signal = scancode;

        match scancode {
            // --- Modifier Tracking ---
            0x2A => { self.modifier_mask |= MASK_LEFT_SHIFT; None },
            0x36 => { self.modifier_mask |= MASK_RIGHT_SHIFT; None },
            0xAA => { self.modifier_mask &= !MASK_LEFT_SHIFT; None },
            0xB6 => { self.modifier_mask &= !MASK_RIGHT_SHIFT; None },
            0x1D => { self.modifier_mask |= MASK_CTRL; None },
            0x9D => { self.modifier_mask &= !MASK_CTRL; None },
            0x38 => { self.modifier_mask |= MASK_ALT; None },
            0xB8 => { self.modifier_mask &= !MASK_ALT; None },
            
            // --- Break Code Clear Lane ---
            code if (code & 0x80) != 0 => {
                // Clear the E0 indicator on any trailing break code
                self.modifier_mask &= !0x80;
                None
            },

            // --- Make Code Ingestion Lane ---
            code => {
                let is_shifted = (self.modifier_mask & (MASK_LEFT_SHIFT | MASK_RIGHT_SHIFT)) != 0;
                let is_ctrl = (self.modifier_mask & MASK_CTRL) != 0;
                let is_alt = (self.modifier_mask & MASK_ALT) != 0;
                let is_meta = (self.modifier_mask & MASK_META) != 0;
                let is_extended = (self.modifier_mask & 0x80) != 0;

                // Reset extended marker for the next sequence cycle
                self.modifier_mask &= !0x80;

                // LAYER 1 INTERCEPTS
                if is_ctrl && is_meta {
                    match code {
                        0x48 if is_extended => return Some(0x10), // True Extended Arrow Up
                        0x50 if is_extended => return Some(0x11), // True Extended Arrow Down
                        0x19 => return Some(237),                 // Ctrl + Meta + P -> 'φ'
                        0x1F => return Some(0x12),                 // Ctrl + Meta + S
                        _ => return None,
                    }
                }

                // LAYER 2 INTERCEPTS
                if is_ctrl {
                    match code {
                        0x2E => return Some(0x03), // Ctrl + C
                        0x2F => return Some(0x16), // Ctrl + V
                        0x46 => return Some(0xCC), // Ctrl + Break
                        0x26 => return Some(0x0C), // Ctrl + L
                        _ => {},
                    }
                }

                // LAYER 3 INTERCEPTS
                if is_alt {
                    match code {
                        0x17 => return Some(0x83), // Alt + I
                        0x32 => return Some(0x84), // Alt + M
                        0x2F => return Some(0x85), // Alt + V
                        0x13 => return Some(0x87), // Alt + R
                        0x2E => return Some(0x89), // Alt + C
                        _ => return None,
                    }
                }

                // LAYER 4 CORE PROFILE MAPPINGS
                match self.active_profile {
                    MatrixLayoutProfile::StandardQWERTY => self.map_qwerty_to_ascii(code, is_shifted),
                    MatrixLayoutProfile::StandardAZERTY => self.map_azerty_to_ascii(code, is_shifted),
                    MatrixLayoutProfile::StandardQWERTZ => self.map_qwertz_to_ascii(code, is_shifted),
            }
        }
    }
}
    
    // core/gtos_console_matrix.rs (Part 2 of 2)
    // Complete 1-to-1 US-QWERTY Translation Layout
    fn map_qwerty_to_ascii(&self, scancode: u8, shifted: bool) -> Option<u8> {
        match (scancode, shifted) {
            // Alphanumeric Text Layout Characters
            (0x10, false) => Some(b'q'), (0x10, true) => Some(b'Q'),
            (0x11, false) => Some(b'w'), (0x11, true) => Some(b'W'),
            (0x12, false) => Some(b'e'), (0x12, true) => Some(b'E'),
            (0x13, false) => Some(b'r'), (0x13, true) => Some(b'R'),
            (0x14, false) => Some(b't'), (0x14, true) => Some(b'T'),
            (0x15, false) => Some(b'y'), (0x15, true) => Some(b'Y'),
            (0x16, false) => Some(b'u'), (0x16, true) => Some(b'U'),
            (0x17, false) => Some(b'i'), (0x17, true) => Some(b'I'),
            (0x18, false) => Some(b'o'), (0x18, true) => Some(b'O'),
            (0x19, false) => Some(b'p'), (0x19, true) => Some(b'P'),
            (0x1E, false) => Some(b'a'), (0x1E, true) => Some(b'A'),
            (0x1F, false) => Some(b's'), (0x1F, true) => Some(b'S'),
            (0x20, false) => Some(b'd'), (0x20, true) => Some(b'D'),
            (0x21, false) => Some(b'f'), (0x21, true) => Some(b'F'),
            (0x22, false) => Some(b'g'), (0x22, true) => Some(b'G'),
            (0x23, false) => Some(b'h'), (0x23, true) => Some(b'H'),
            (0x24, false) => Some(b'j'), (0x24, true) => Some(b'J'),
            (0x25, false) => Some(b'k'), (0x25, true) => Some(b'K'),
            (0x26, false) => Some(b'l'), (0x26, true) => Some(b'L'),
            (0x2C, false) => Some(b'z'), (0x2C, true) => Some(b'Z'),
            (0x2D, false) => Some(b'x'), (0x2D, true) => Some(b'X'),
            (0x2E, false) => Some(b'c'), (0x2E, true) => Some(b'C'),
            (0x2F, false) => Some(b'v'), (0x2F, true) => Some(b'V'),
            (0x30, false) => Some(b'b'), (0x30, true) => Some(b'B'),
            (0x31, false) => Some(b'n'), (0x31, true) => Some(b'N'),
            (0x32, false) => Some(b'm'), (0x32, true) => Some(b'M'),

            // System Key Configurations
	    (0x01, _) => Some(0x1B), //esc
	    (0x3A, _) => Some(0x14), // caps lock token (DC4)
	    (0x53, _) => Some(0x7F), // del
            
            // Function Keys (F1 - Dialog Blocks)
            (0x3B, _) => Some(0x80), // F1 
            (0x3C, _) => Some(0x81), // F2
            (0x3D, _) => Some(0x82), // F3
            (0x3E, _) => Some(0x83), // F4
            (0x3F, _) => Some(0x84), // F5
            (0x40, _) => Some(0x85), // F6
            (0x41, _) => Some(0x86), // F7
            (0x42, _) => Some(0x87), // F8
            (0x43, _) => Some(0x88), // F9
            (0x44, _) => Some(0x89), // F10
            (0x57, _) => Some(0x8A), // F11
            (0x58, _) => Some(0x8B), // F12
             
            // Numeric Key Row Layout Characters
            (0x02, false) => Some(b'1'), (0x02, true) => Some(b'!'),
            (0x03, false) => Some(b'2'), (0x03, true) => Some(b'@'),
            (0x04, false) => Some(b'3'), (0x04, true) => Some(b'#'),
            (0x05, false) => Some(b'4'), (0x05, true) => Some(b'$'),
            (0x06, false) => Some(b'5'), (0x06, true) => Some(b'%'),
            (0x07, false) => Some(b'6'), (0x07, true) => Some(b'^'),
            (0x08, false) => Some(b'7'), (0x08, true) => Some(b'&'),
            (0x09, false) => Some(b'8'), (0x09, true) => Some(b'*'),
            (0x0A, false) => Some(b'9'), (0x0A, true) => Some(b'('),
            (0x0B, false) => Some(b'0'), (0x0B, true) => Some(b')'),

            // Full Regional Punctuation, Slashing, and Bracket Configurations
            (0x0C, false) => Some(b'-'), (0x0C, true) => Some(b'_'),
            (0x0D, false) => Some(b'='), (0x0D, true) => Some(b'+'),
            (0x1A, false) => Some(b'['), (0x1A, true) => Some(b'{'),
            (0x1B, false) => Some(b']'), (0x1B, true) => Some(b'}'),
            (0x27, false) => Some(b';'), (0x27, true) => Some(b':'),
            (0x28, false) => Some(b'\''),(0x28, true) => Some(b'"'),
            (0x29, false) => Some(b'`'), (0x29, true) => Some(b'~'),
            (0x2B, false) => Some(b'\\'),(0x2B, true) => Some(b'|'),
            (0x33, false) => Some(b','), (0x33, true) => Some(b'<'),
            (0x34, false) => Some(b'.'), (0x34, true) => Some(b'>'),
            (0x35, false) => Some(b'/'), (0x35, true) => Some(b'?'),

            // Navigational Systems & Hardware Interface Actions
            (0x39, _) => Some(b' '),  
            (0x1C, _) => Some(b'\n'), 
            (0x0E, _) => Some(0x08), // Backspace Key (Standard ASCII BS code)
            (0x0F, _) => Some(b'\t'), // Tab Key

            // Arrow Key Boundary Enforcements (Returning directional layout tokens)
            (0x48, _) => Some(0x1E), // Arrow Up (ASCII RS)
            (0x50, _) => Some(0x1F), // Arrow Down (ASCII US)
            (0x4B, _) => Some(0x11), // Arrow Left (ASCII DC1)
            (0x4D, _) => Some(0x12), // Arrow Right (ASCII DC2)
            _ => None,
        }
    }

    /// French AZERTY Translation Base
    fn map_azerty_to_ascii(&self, scancode: u8, shifted: bool) -> Option<u8> {
        match (scancode, shifted) {
            (0x10, false) => Some(b'a'), (0x10, true) => Some(b'A'), 
            (0x11, false) => Some(b'z'), (0x11, true) => Some(b'Z'), 
            _ => self.map_qwerty_to_ascii(scancode, shifted),
        }
    }

    /// German QWERTZ Translation Base
    fn map_qwertz_to_ascii(&self, scancode: u8, shifted: bool) -> Option<u8> {
        match (scancode, shifted) {
            (0x15, false) => Some(b'z'), (0x15, true) => Some(b'Z'), 
            (0x2C, false) => Some(b'y'), (0x2C, true) => Some(b'Y'),
            _ => self.map_qwerty_to_ascii(scancode, shifted),
        }
    }

    /// Accessibility Gate
    fn decode_pneumatic_cadence(&mut self, port: u16, timing_byte: u8) -> Option<u8> {
        if port == 0x0068 { 
            match timing_byte {
                1..=50 => Some(b'.'),
                51..=150 => Some(b'-'),
                151 => Some(b' '),
                _ => None,
            }
        } else {
            None
        }
    }
}
