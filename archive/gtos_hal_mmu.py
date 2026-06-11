# core/gtos_hal_mmu.py
import struct
from typing import Dict, Optional
from gtos_register_map import GTOSRegisterMap

class GTOSHardwareMMU:
    """
    GTOS Phase 6 Core: Hardware Abstraction Layer Memory Management Unit (Refactored).
    Simulates a physical hardware MMU, locking 24-byte serialized geometric 
    coordinate seeds into fixed, contiguous memory block slots with strict type enforcement.
    """
    def __init__(self, total_pages: int = 256):
        self.PAGE_SIZE_BYTES: int = 24 
        self.TOTAL_PAGES: int = int(total_pages) 
        self.physical_ram_bus: bytearray = bytearray(self.TOTAL_PAGES * self.PAGE_SIZE_BYTES) 
        self.register_map: GTOSRegisterMap = GTOSRegisterMap() 
        self.page_frame_registry: Dict[str, int] = {}
        self.next_free_page_frame: int = 0

    def write_coordinate_to_physical_ram(self, cell_id: str, packed_seed: bytes) -> bool:
        """
        HAL Bus Write: Intercepts a 24-byte binary seed and forces it into a 
        physical, sequential block address in the simulated memory hardware.
        """
        clean_seed = bytes(packed_seed)
        if len(clean_seed) != self.PAGE_SIZE_BYTES:
            return False 
            
        current_frame = int(self.next_free_page_frame)
        if current_frame >= self.TOTAL_PAGES:
            return False 

        # Calculate exact linear byte boundary offset on the memory bus using pure integer math
        start_address = current_frame * self.PAGE_SIZE_BYTES
        end_address = start_address + self.PAGE_SIZE_BYTES
        
        # Commit raw binary sequence to the contiguous byte array
        self.physical_ram_bus[start_address:end_address] = clean_seed
        
        # Register the hardware page mapping with a flattened string primitive key
        clean_key = str(cell_id)
        self.page_frame_registry[clean_key] = current_frame
        
        self.next_free_page_frame = current_frame + 1
        return True

    def read_coordinate_from_physical_ram(self, cell_id: str) -> Optional[bytes]:
        """
        HAL Bus Read: Locates the target hardware page frame, reads the 
        contiguous 24 bytes directly off the bus, and returns the binary seed.
        """
        clean_key = str(cell_id)
        if clean_key not in self.page_frame_registry:
            return None
            
        page_frame = int(self.page_frame_registry[clean_key])
        start_address = page_frame * self.PAGE_SIZE_BYTES
        end_address = start_address + self.PAGE_SIZE_BYTES
        
        return bytes(self.physical_ram_bus[start_address:end_address])
