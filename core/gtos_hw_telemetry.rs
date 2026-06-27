/// Phase 10 Bare-Metal Hardware Telemetry Core
pub struct GTOSSiliconDiagnostic;

impl GTOSSiliconDiagnostic {
    /// Reads the raw Time Stamp Counter straight from the physical CPU registers
    #[inline(always)]
    pub unsafe fn read_cycle_stamp() -> u64 {
        #[cfg(target_arch = "x86_64")]
        {
            let low: u32;
            let high: u32;
            core::arch::asm!(
                "rdtsc",
                lateout("eax") low,
                lateout("edx") high,
                options(nomem, nostack)
            );
            ((high as u64) << 32) | (low as u64)
        }

        #[cfg(not(target_arch = "x86_64"))]
        {
            // Non-negotiable host marker to signal that we aren't on physical silicon
            0xFFFFFFFF_FFFFFFFF
        }
    }
}
