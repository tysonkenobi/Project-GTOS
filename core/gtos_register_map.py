from typing import Dict, Optional

class GTOSRegisterMap:
    """
    GTOS Phase 5.1 Core: Hardware Register Map Simulator.
    Defines explicit 8-bit/16-bit register tracking blocks to translate 
    exception redirection handlers into simulated hardware interrupt vectors.
    """
    def __init__(self):
        # 1. Base Hardware Address Mapping (Simulated I/O Control Space)
        self.REG_BASE_ADDR: int = 0x4000

        # 2. Hardcoded Hardware Register Offsets
        self.REG_CR0_STATUS: int = 0x00      # Control Register 0: System State & Manifold Domain Flag
        self.REG_IER_INTERRUPT: int = 0x01   # Interrupt Enable Register: Hardware Interrupt Mask Lines
        self.REG_IFR_FLAGS: int = 0x02       # Interrupt Flag Register: Stores triggered fault events
        self.REG_FVR_VAL: int = 0x04         # Fault Value Register: 16-bit space for failed numerators

        # 3. Raw Physical Register Hardware Memory (Simulated 8-byte Cache File)
        self.register_byte_array: bytearray = bytearray(8)

        # 4. Standardized Interrupt Vector Memory Addresses
        self.VECTOR_ARITHMETIC_FAULT: int = 0x000000A0
        self.VECTOR_BOUNDARY_VIOLATION: int = 0x000000B0

    def write_register_byte(self, offset: int, byte_value: int) -> bool:
        """ Low-Level Write: Enforces 8-bit unsigned integers into exact offset bytes. """
        if offset < 0 or offset >= len(self.register_byte_array):
            return False
        self.register_byte_array[offset] = int(byte_value) & 0xFF
        return True

    def read_register_byte(self, offset: int) -> int:
        """ Low-Level Read: Pulls a raw 8-bit byte directly off the register pin. """
        if offset < 0 or offset >= len(self.register_byte_array):
            return 0x00
        return self.register_byte_array[offset]

    def trigger_hardware_interrupt(self, fault_type: str, origin_value: float) -> int:
        """
        HAL Intercept Routine: Maps software errors to hardware bits. Shifts bits 
        inside the Status and Flag registers, saves raw context data, and returns 
        the correct compiled hexadecimal execution address pointer.
        """
        if fault_type == "ZERO_DIVISION_FAULT":
            # Set Bit 0 (Active Interrupt) and Bit 1 (Arithmetic Fault Type) in the Flag Register
            self.write_register_byte(self.REG_IFR_FLAGS, 0x03)
            
            # Map the failed float value directly into the 16-bit Fault Value Register space
            # (Truncated cleanly to 8-bit integer equivalent bounds for basic register demonstration)
            truncated_val = int(abs(origin_value)) & 0xFF
            self.write_register_byte(self.REG_FVR_VAL, truncated_val)
            
            return self.VECTOR_ARITHMETIC_FAULT
            
        elif fault_type == "SPATIAL_FIREWALL_BREACH":
            # Set Bit 0 (Active Interrupt) and Bit 2 (Firewall Breach Type) in the Flag Register
            self.write_register_byte(self.REG_IFR_FLAGS, 0x05)
            return self.VECTOR_BOUNDARY_VIOLATION
            
        return 0x00000000

    def clear_interrupt_flags(self) -> None:
        """ Hardware Reset: Flushes active flag bits back to stable zero states. """
        self.write_register_byte(self.REG_IFR_FLAGS, 0x00)
        self.write_register_byte(self.REG_FVR_VAL, 0x00)
