# core/gtos_hal_ai_compute.py
import ctypes

class GTOSUnifiedTokenBuffer(ctypes.Structure):
    """
    GTOS Phase 5.3 Core: Unified Memory Space Simulator.
    Allocates a rigid 512-byte contiguous memory footprint to stream 
    raw token text strings directly over low-level hardware registers.
    """
    _pack_ = 1  # Force strict 1-byte raw hardware packing boundary
    _fields_ = [
        ("allocated_capacity", ctypes.c_uint32), # 4 bytes: Static block ceiling
        ("active_token_length", ctypes.c_uint32),# 4 bytes: Direct byte pointer array index
        ("raw_byte_payload", ctypes.c_char * 504)# 504 bytes: Flat contiguous character array
    ]                                            # Total = Exactly 512 bytes unpadded memory space

class GTOSHALAIComputeDriver:
    """
    Abstract Unified Memory compute interface. Direct-maps token streams
    into unfragmented byte allocations to isolate bare-metal hardware execution.
    """
    def __init__(self):
        self.buffer_footprint_bytes: int = ctypes.sizeof(GTOSUnifiedTokenBuffer)
        if self.buffer_footprint_bytes != 512:
            raise RuntimeError(f"HAL_AI_FAULT: Struct size misaligned: {self.buffer_footprint_bytes}/512")

    def allocate_unified_frame(self) -> GTOSUnifiedTokenBuffer:
        """
        Simulates raw hardware register allocation, carving out a fresh
        512-byte unified memory segment on the device bus. Ctypes clears memory natively.
        """
        frame = GTOSUnifiedTokenBuffer()
        frame.allocated_capacity = 504
        frame.active_token_length = 0
        return frame

    def stream_token_to_hardware(self, buffer_frame: GTOSUnifiedTokenBuffer, incoming_token: str) -> bool:
        """
        Direct Memory Access (DMA) Emulation: Uses native memmove to write 
        directly into the struct memory block without shifting dynamic string memory.
        """
        token_bytes = incoming_token.encode('utf-8')
        new_length = buffer_frame.active_token_length + len(token_bytes)
        
        # Enforce strict memory boundary overflow checks
        if new_length > buffer_frame.allocated_capacity:
            return False  # Memory buffer limit breached (Trapped safely)
            
        # Calculate target memory address offset manually
        # Frame start address + 8 bytes (skipping the two 4-byte integers) + current index write offset
        dest_memory_address = ctypes.addressof(buffer_frame) + 8 + buffer_frame.active_token_length
        
        # Low-level direct memory copy from token array straight into destination layout
        ctypes.memmove(dest_memory_address, token_bytes, len(token_bytes))
        
        buffer_frame.active_token_length = new_length
        return True

    def read_clean_payload(self, buffer_frame: GTOSUnifiedTokenBuffer) -> str:
        """
        Extracts and decodes only the actively populated byte slice 
        from the rigid hardware memory space.
        """
        active_bytes = buffer_frame.raw_byte_payload[:buffer_frame.active_token_length]
        return active_bytes.decode('utf-8', errors='ignore')
