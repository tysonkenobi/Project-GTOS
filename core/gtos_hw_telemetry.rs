/// Phase 10 Bare-Metal Hardware Telemetry Core
pub struct GTOSSiliconDiagnostic;

impl GTOSSiliconDiagnostic {
    /// Reads the raw Time Stamp Counter straight from the physical CPU registers
    #[inline(always)]
    pub unsafe fn read_cycle_stamp() -> u64 {
        let low: u32;
        let high: u32;
        core::arch::asm!(
            "rdtsc",
            lateout("eax") low,
            lateout("edx") high,
            options(nomem, nostack)
        );
        ((high as u64)  eax,
            lateout("ebx") ebx,
            lateout("ecx") ecx,
            lateout("edx") edx,
            options(nomem, nostack, preserves_flags)
        );
    }
}
