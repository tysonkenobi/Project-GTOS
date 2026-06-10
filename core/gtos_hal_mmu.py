# core/gtos_hal_mmu.py
import struct
from typing import Dict, Optional
from gtos_register_map import GTOSRegisterMap

class GTOSHardwareMMU:
    """
    GTOS Phase 5.1 Core: Hardware Abstraction Layer Memory Management Unit.
    Simulates a physical hardware MMU, locking 24-byte serialized geometric coordinate seeds into fixed, contiguous memory block slots.
    """
    def __init__(self, total_pages: int = 256):
        self.PAGE_SIZE_BYTES: int = 24 # Rigid GTOS coordinate seed footprint
        self.TOTAL_PAGES: int = total_pages # Simulated Physical RAM Matrix (Contiguous Byte Array)
        
        # Simulated Physical RAM Matrix (Contiguous Byte Array)
        self.physical_ram_bus: bytearray = bytearray(self.TOTAL_PAGES * self.PAGE_SIZE_BYTES)
        
        # Low-level hardware registry instance attachment
        self.register_map: GTOSRegisterMap = GTOSRegisterMap()
        
        # Hardware Page Allocation Table: Maps Cell IDs to Physical Page Frames
        self.page_frame_registry: Dict[str, int] = {}
        self.next_free_page_frame: int = 0

    def write_coordinate_to_physical_ram(self, cell_id: str, packed_seed: bytes) -> bool:
        """
        HAL Bus Write: Intercepts a 24-byte binary seed and forces it into 
        a physical, sequential block address in the simulated memory hardware.
        """
        if len(packed_seed) != self.PAGE_SIZE_BYTES:
            return False  # Block size non-compliance trap
            
        if self.next_free_page_frame >= self.TOTAL_PAGES:
            return False  # Physical hardware memory exhaustion (Out of Pages)
            
        # Calculate exact linear byte boundary offset on the memory bus
        start_address = self.next_free_page_frame * self.PAGE_SIZE_BYTES
        end_address = start_address + self.PAGE_SIZE_BYTES
        
        # Commit raw binary sequence to the contiguous byte array
        self.physical_ram_bus[start_address:end_address] = packed_seed
        
        # Register the hardware page mapping
        self.page_frame_registry[cell_id] = self.next_free_page_frame
        self.next_free_page_frame += 1
        return True

    def read_coordinate_from_physical_ram(self, cell_id: str) -> Optional[bytes]:
        """
        HAL Bus Read: Locates the target hardware page frame, reads the 
        contiguous 24 bytes directly off the bus, and returns the binary seed.
        """
        if cell_id not in self.page_frame_registry:
            return None
            
        page_frame = self.page_frame_registry[cell_id]
        start_address = page_frame * self.PAGE_SIZE_BYTES
        end_address = start_address + self.PAGE_SIZE_BYTES
        
        # Extract direct memory bytes slice
        return bytes(self.physical_ram_bus[start_address:end_address])
