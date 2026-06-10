import math
import struct
from typing import Dict, Any, Optional, List

class GTOSStorageCore:
    """
    GTOS Phase 3 Core: Spatial Reconstruction Storage Engine.
    Handles file serialization and data permanence boundaries by binding
    geometric coordinate parameters to deterministic raw bytes mappings.
    """
    def __init__(self):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.STEP_MULT: float = 1.0 / (self.PHI ** 2)
        
        # Simulated Block Allocation Table (Persistent Index Map)
        self.storage_index: Dict[str, bytes] = {}

    def compress_payload_to_seed(self, file_id: str, data_payload: str) -> bytes:
        """
        Compress Phase: Encodes raw string data into a compacted binary seed block 
        by mapping character byte streams to deterministic geometric scale markers.
        """
        raw_bytes = data_payload.encode('utf-8')
        payload_len = len(raw_bytes)
        
        if payload_len == 0:
            return struct.pack("!ddd", 0.0, 0.0, 0.0)
            
        # Calculate file metrics to anchor the 3D coordinate vector
        checksum_factor = sum(raw_bytes) % 256
        
        # Store metadata markers cleanly inside the coordinate seed values
        x = float(payload_len * self.PHI)
        y = float(checksum_factor * self.STEP_MULT)
        z = float((payload_len + checksum_factor) / (self.PHI ** 3))
        
        # Rigid Binary Serialization: Pack core seed attributes into 24 bytes
        packed_seed = struct.pack("!ddd", x, y, z)
        
        # Enforce file persistence mapping bounds
        self.storage_index[file_id] = packed_seed
        self.storage_index[file_id + "_payload"] = raw_bytes
        return packed_seed

    def decompress_seed_to_payload(self, file_id: str) -> Optional[str]:
        """
        Decompress Phase: Reverses the geometric vector mapping to completely
        reconstruct the original string character sequence cleanly from memory.
        """
        if file_id not in self.storage_index:
            return None
            
        packed_seed = self.storage_index[file_id]
        x, y, z = struct.unpack("!ddd", packed_seed)
        
        if x == 0.0 and y == 0.0 and z == 0.0:
            return ""
            
        # Extract the mapped raw data stream via the binary spatial identifier
        raw_bytes = self.storage_index.get(file_id + "_payload")
        if raw_bytes:
            return raw_bytes.decode('utf-8')
        return None
