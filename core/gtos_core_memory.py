# core/gtos_core_memory.py
import math
from typing import Dict, Any

class GTOSKernelMemoryController:
    """
    GTOS Phase 6 Core: Geometric Memory Controller (Refactored).
    Enforces strict primitive serialization on spatial coordinates to prevent
    type-bleeding down to unpadded hardware registries under concurrent load.
    """
    def __init__(self, boundary_threshold: float = 0.10):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.BOUNDARY_LIMIT: float = float(boundary_threshold)
        self.PHI_SIXTH_UNIT: float = float(1.0 / (6.0 * (self.PHI ** 3)))
        self.GOLDEN_ANGLE: float = float(2.0 * math.pi * (1.0 - (1.0 / self.PHI)))
        self.active_manifold_state: int = 1
        self.system_load: float = 0.0
        self.allocation_counter: int = 0
        self.geometric_fat: Dict[str, Dict[str, Any]] = {}

    def calculate_temporal_distance(self, load_state: float) -> float:
        return float((self.BOUNDARY_LIMIT - float(load_state)) / self.PHI_SIXTH_UNIT)

    def allocate_file_seed(self, file_id: str, complexity_payload: str) -> Dict[str, Any]:
        # Force clean primitive tracking increments
        self.allocation_counter = int(self.allocation_counter) + 1
        payload_len = len(complexity_payload)
        
        spatial_entropy = 0.0 if payload_len == 0 else (math.log(payload_len + 1) * 0.35) / payload_len
        self.system_load = float(self.system_load) + float(spatial_entropy)
        
        if self.system_load >= self.BOUNDARY_LIMIT:
            self.active_manifold_state = -1 if int(self.active_manifold_state) == 1 else 1
            self.system_load = abs(self.BOUNDARY_LIMIT - self.system_load)
            action_status = "INVERSION"
        else:
            action_status = "STABLE"

        radius = math.sqrt(float(self.allocation_counter)) * self.PHI
        theta = float(self.allocation_counter) * self.GOLDEN_ANGLE
        t_distance = self.calculate_temporal_distance(self.system_load)
        
        warp = 1.0 + (1.0 / (abs(t_distance) + 1e-9))
        
        # Phase 6 Enforcement: Explicitly cast all spatial outputs to clean primitives
        x = float(radius * math.cos(theta) * warp)
        y = float(radius * math.sin(theta) * warp)
        z = float(int(self.active_manifold_state) * (int(self.allocation_counter) * self.PHI_SIXTH_UNIT))

        node_seed = {
            "coordinate_vector": (x, y, z),
            "temporal_weight_t": float(t_distance),
            "manifold_domain": int(self.active_manifold_state),
            "status": str(action_status)
        }
        
        self.geometric_fat[str(file_id)] = node_seed
        return node_seed

    def locate_file_seed(self, file_id: str) -> Dict[str, Any]:
        target_key = str(file_id)
        if target_key in self.geometric_fat:
            return self.geometric_fat[target_key]
        raise KeyError(f"GTOS_PANIC: {target_key} missing from tracking matrix.")
