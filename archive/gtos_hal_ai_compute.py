# core/gtos_hal_ai_compute.py
import ctypes

class GTOSUnifiedTokenBuffer(ctypes.Structure):
    """
    GTOS Phase 5.3 Core: Unified Memory Space Simulator.
    Allocates a rigid 512-byte contiguous memory footprint to stream raw token 
    text strings directly over low-level hardware registers.
    """
    _pack_ = 1 
    _fields_ = [
        ("allocated_capacity", ctypes.c_uint32), 
        ("active_token_length", ctypes.c_uint32),
        ("raw_byte_payload", ctypes.c_char * 504)
    ] 

class GTOSHALAIComputeDriver:
    """
    Abstract Unified Memory compute interface.
    Direct-maps token streams into unfragmented byte allocations to isolate 
    bare-metal hardware execution at the Python/Machine language boundary.
    """
    def __init__(self):
        self.buffer_footprint_bytes: int = ctypes.sizeof(GTOSUnifiedTokenBuffer)
        if self.buffer_footprint_bytes != 512:
            raise RuntimeError(f"HAL_AI_FAULT: Struct size misaligned: {self.buffer_footprint_bytes}/512")

    def allocate_unified_frame(self) -> GTOSUnifiedTokenBuffer:
        frame = GTOSUnifiedTokenBuffer()
        frame.allocated_capacity = 504
        frame.active_token_length = 0
        return frame

    def stream_token_to_hardware(self, buffer_frame: GTOSUnifiedTokenBuffer, incoming_token: str) -> bool:
        """
        Direct Memory Access (DMA) Emulation: Uses native memmove to write directly 
        into the struct memory block without shifting dynamic string memory.
        """
        if not hasattr(buffer_frame, 'active_token_length'):
            return False

        # Phase 6.3 Concurrency Sanitization: Ensure clean text encoding string conversion
        token_bytes = str(incoming_token).encode('utf-8', errors='ignore')
        
        # Explicitly cast to plain integer primitive to prevent type-bleeding
        current_len = int(buffer_frame.active_token_length)
        new_length = current_len + len(token_bytes)
        
        if new_length > int(buffer_frame.allocated_capacity):
            return False 

        dest_memory_address = ctypes.addressof(buffer_frame) + 8 + current_len
        ctypes.memmove(dest_memory_address, token_bytes, len(token_bytes))
        
        # Force strict integer primitive assignment back to the unpadded ctypes register field
        buffer_frame.active_token_length = int(new_length)
        return True

    def read_clean_payload(self, buffer_frame: GTOSUnifiedTokenBuffer) -> str:
        """
        Extracts and decodes only the actively populated byte slice from the rigid hardware memory space.
        """
        active_len = int(buffer_frame.active_token_length)
        active_bytes = buffer_frame.raw_byte_payload[:active_len]
        return active_bytes.decode('utf-8', errors='ignore')
