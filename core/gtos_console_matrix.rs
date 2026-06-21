// core/gtos_console_matrix.rs (Part 2 of 2)
impl GTOSConsoleMatrixState {
    /// Decodes raw laptop keyboard bytes, tracking modifiers cleanly via explicit masks
    fn decode_laptop_scancode(&mut self, scancode: u8) -> Option<u8> {
        if scancode == self.last_processed_signal {
            return None;
        }
        self.last_processed_signal = scancode;

        match scancode {
            // Track Shift modifier press/release
            0x2A => { self.modifier_mask |= MASK_LEFT_SHIFT; None },
            0x36 => { self.modifier_mask |= MASK_RIGHT_SHIFT; None },
            0xAA => { self.modifier_mask &= !MASK_LEFT_SHIFT; None },
            0xB6 => { self.modifier_mask &= !MASK_RIGHT_SHIFT; None },

            // Track Ctrl modifier press/release
            0x1D => { self.modifier_mask |= MASK_CTRL; None },
            0x9D => { self.modifier_mask &= !MASK_CTRL; None },

            // Track Alt modifier press/release
            0x38 => { self.modifier_mask |= MASK_ALT; None },
            0xB8 => { self.modifier_mask &= !MASK_ALT; None },

            // Track Meta Key (Windows/Command Key) press/release
            0x5B => { 
                self.modifier_mask |= MASK_META; 
                let is_continuous = (self.modifier_mask & SETTING_MIC_PTT) != 0;
                if is_continuous {
                    self.modifier_mask ^= MASK_META_MIC; // Continuous Mode: Instant Hardware Mute Toggle
                } else {
                    self.modifier_mask |= MASK_META_MIC;  // PTT Mode: Holding down opens microphone line
                }
                None 
            },
            0xDB => { 
                self.modifier_mask &= !MASK_META; 
                let is_continuous = (self.modifier_mask & SETTING_MIC_PTT) != 0;
                if !is_continuous {
                    self.modifier_mask &= !MASK_META_MIC; // PTT Mode: Releasing closes line instantly
                }
                None 
            },

            // Process Standard Key Press events (Make codes have high bit clear)
            code if (code & 0x80) == 0 => {
                let is_shifted = (self.modifier_mask & (MASK_LEFT_SHIFT | MASK_RIGHT_SHIFT)) != 0;
                let is_ctrl = (self.modifier_mask & MASK_CTRL) != 0;
                let is_alt = (self.modifier_mask & MASK_ALT) != 0;
                let is_meta = (self.modifier_mask & MASK_META) != 0;

                // =========================================================================
                // INTERCEPT LAYER 1: MULTI-MODIFIER ENVIRONMENTAL VARIABLES & TOKENS
                // =========================================================================
                if is_ctrl && is_meta {
                    match code {
                        0x48 => return Some(0x10), // Ctrl + Meta + Arrow Up: Live-Tune GIO Kappa Up
                        0x50 => return Some(0x11), // Ctrl + Meta + Arrow Down: Live-Tune GIO Kappa Down
                        0x19 => return Some(237),  // Ctrl + Meta + P: Instantly yield raw character 237 (φ)
                        0x1F => return Some(0x12), // Ctrl + Meta + S: Print Screen (Flashes VGA Snapshot Byte)
                        _ => return None,
                    }
                }

                // =========================================================================
                // INTERCEPT LAYER 2: INDUSTRY-STANDARD SHELL CONTROL COMMANDS
                // =========================================================================
                if is_ctrl {
                    match code {
                        0x2E => return Some(0x03), // Ctrl + C: Standard Copy (ASCII ETX clipboard command byte)
                        0x2F => return Some(0x16), // Ctrl + V: Standard Paste (ASCII SYN stream injection byte)
                        0x46 => return Some(0xCC), // Ctrl + Break/Pause: Triggers 517-byte Terminal Brake chord
                        0x26 => return Some(0x0C), // Ctrl + L: Form Feed control byte -> Triggers clear screen
                        _ => {}, 
                    }
                }

                // =========================================================================
                // INTERCEPT LAYER 3: DEDICATED ALT DIALS / INSTRUMENT OVERLAYS
                // =========================================================================
                if is_alt {
                    match code {
                        0x17 => return Some(0x83), // Alt + I: Local AI Intelligence Performance Overlay [0x03]
                        0x32 => return Some(0x84), // Alt + M: Motherboard Topology/PCI Bus Map [0x04]
                        0x2F => return Some(0x85), // Alt + V: Vision Spatial Sensor Tracker Frame [0x05]
                        0x30 => return Some(0x86), // CALLBACK STUB - Routes to Biometric Status display [0x06]
                        0x13 => return Some(0x87), // Alt + R: Robotics Kinetic Motor Coordinate Map [0x07]
                        0x21 => return Some(0x88), // CALLBACK STUB - Routes to Finance Ledger display [0x08]
                        0x2E => return Some(0x89), // Alt + C: Comms Pipeline Packet Monitor [0x09]
                        _ => return None,
                    }
                }

                // =========================================================================
                // CORE INTERCEPT LAYER 4: STANDARD REGIONAL QWERTY MATRIX MAPPINGS
                // =========================================================================
                match self.active_profile {
                    MatrixLayoutProfile::StandardQWERTY => self.map_qwerty_to_ascii(code, is_shifted),
                    MatrixLayoutProfile::StandardAZERTY => self.map_azerty_to_ascii(code, is_shifted),
                    MatrixLayoutProfile::StandardQWERTZ => self.map_qwertz_to_ascii(code, is_shifted),
                    _ => None,
                }
            },

            _ => None,
        }
    }

    /// Complete 1-to-1 US-QWERTY Translation Layout
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
        if port == 0x68 { 
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
