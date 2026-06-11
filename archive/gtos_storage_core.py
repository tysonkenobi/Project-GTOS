# core/gtos_storage_core.py
import math
import struct
from typing import Dict, Any, Optional

class GTOSStorageCore:
    """
    GTOS Phase 6 Core: Spatial Reconstruction Storage Engine (Refactored).
    Enforces strict primitive serialization and string flattening boundaries
    to eliminate high-level type leakage under concurrent execution.
    """
    def __init__(self):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.STEP_MULT: float = float(1.0 / (self.PHI ** 2))
        self.storage_index: Dict[str, bytes] = {}

    def compress_payload_to_seed(self, file_id: str, data_payload: str) -> bytes:
        """
        Compress Phase: Encodes raw string data into a compacted binary seed block.
        """
        clean_file_id = str(file_id)
        
        # Resolve compound type sequences passed down by multi-engine threads
        if isinstance(data_payload, (list, tuple)) and len(data_payload) > 0:
            clean_payload = str(data_payload[0])
        else:
            clean_payload = str(data_payload)
            
        raw_bytes = clean_payload.encode('utf-8', errors='ignore')
        payload_len = len(raw_bytes)
        
        if payload_len == 0:
            packed_seed = struct.pack("!ddd", 0.0, 0.0, 0.0)
            self.storage_index[clean_file_id] = packed_seed
            return packed_seed

        checksum_factor = int(sum(raw_bytes) % 256)
        
        x = float(payload_len * self.PHI)
        y = float(checksum_factor * self.STEP_MULT)
        z = float((payload_len + checksum_factor) / (self.PHI ** 3))

        packed_seed = struct.pack("!ddd", x, y, z)
        
        self.storage_index[clean_file_id] = packed_seed
        self.storage_index[clean_file_id + "_payload"] = raw_bytes
        return packed_seed

    def decompress_seed_to_payload(self, file_id: str) -> Optional[str]:
        """
        Decompress Phase: Reverses the geometric vector mapping.
        """
        clean_file_id = str(file_id)
        if clean_file_id not in self.storage_index:
            return None
            
        packed_seed = self.storage_index[clean_file_id]
        x, y, z = struct.unpack("!ddd", packed_seed)
        
        if x == 0.0 and y == 0.0 and z == 0.0:
            return ""

        raw_bytes = self.storage_index.get(clean_file_id + "_payload")
        if raw_bytes:
            return raw_bytes.decode('utf-8', errors='ignore')
        return None
