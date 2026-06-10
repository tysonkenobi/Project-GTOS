import math
from typing import Dict, Any

class GTOSKernelMemoryController:
    def __init__(self, boundary_threshold: float = 0.10):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.BOUNDARY_LIMIT: float = boundary_threshold
        self.PHI_SIXTH_UNIT: float = 1.0 / (6.0 * (self.PHI ** 3))
        self.GOLDEN_ANGLE: float = 2.0 * math.pi * (1.0 - (1.0 / self.PHI))
        
        self.active_manifold_state: int = 1
        self.system_load: float = 0.0
        self.allocation_counter: int = 0
        self.geometric_fat: Dict[str, Dict[str, Any]] = {}

    def calculate_temporal_distance(self, load_state: float) -> float:
        return float((self.BOUNDARY_LIMIT - load_state) / self.PHI_SIXTH_UNIT)

    def allocate_file_seed(self, file_id: str, complexity_payload: str) -> Dict[str, Any]:
        self.allocation_counter += 1
        payload_len = len(complexity_payload)
        
        spatial_entropy = 0.0 if payload_len == 0 else (math.log(payload_len + 1) * 0.35) / payload_len
        self.system_load += spatial_entropy
        
        if self.system_load >= self.BOUNDARY_LIMIT:
            self.active_manifold_state = -1 if self.active_manifold_state == 1 else 1
            self.system_load = abs(self.BOUNDARY_LIMIT - self.system_load)
            action_status = "INVERSION"
        else:
            action_status = "STABLE"
            
        radius = math.sqrt(self.allocation_counter) * self.PHI
        theta = self.allocation_counter * self.GOLDEN_ANGLE
        
        t_distance = self.calculate_temporal_distance(self.system_load)
        warp = 1.0 + (1.0 / (abs(t_distance) + 1e-9))
        
        x = radius * math.cos(theta) * warp
        y = radius * math.sin(theta) * warp
        z = float(self.active_manifold_state) * (self.allocation_counter * self.PHI_SIXTH_UNIT)
        
        node_seed = {
            "coordinate_vector": (x, y, z),
            "temporal_weight_t": t_distance,
            "manifold_domain": self.active_manifold_state,
            "status": action_status
        }
        self.geometric_fat[file_id] = node_seed
        return node_seed

    def locate_file_seed(self, file_id: str) -> Dict[str, Any]:
        if file_id in self.geometric_fat:
            return self.geometric_fat[file_id]
        raise KeyError(f"GTOS_PANIC: {file_id} missing.")
