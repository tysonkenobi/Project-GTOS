import math
import numpy as np
from typing import Dict, Any, Tuple, List
from gtos_core_memory import GTOSKernelMemoryController

class GTOSTokenBridge:
    def __init__(self, memory_controller: GTOSKernelMemoryController):
        self.kernel = memory_controller
        self.entropy_history: List[float] = []
        self.variance_history: List[float] = []
        self.token_registry: List[str] = []

    def evaluate_token_entropy(self, logits: np.ndarray) -> Tuple[float, float]:
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        entropy = float(-np.sum(probs * np.log(probs + 1e-12)))
        variance = float(np.var(probs))
        return entropy, variance

    def intercept_and_route_token(self, token_str: str, raw_logits: np.ndarray) -> Dict[str, Any]:
        entropy, variance = self.evaluate_token_entropy(raw_logits)
        self.entropy_history.append(entropy)
        self.variance_history.append(variance)
        self.token_registry.append(token_str)
        
        is_divergent = False
        kernel_intervention = "STREAM_PURE"
        
        if len(self.entropy_history) > 1:
            if (self.entropy_history[-1] - self.entropy_history[-2]) > 1.5:
                is_divergent = True
                kernel_intervention = "ENTROPY_SPIKE"
                
        if len(self.entropy_history) >= 6 and not is_divergent:
            early_entropy = np.mean(self.entropy_history[:3])
            late_entropy = np.mean(self.entropy_history[-3:])
            if early_entropy > 0 and (late_entropy / early_entropy) < 0.2:
                is_divergent = True
                kernel_intervention = "ATTRACTOR_LOOP"

        if not is_divergent:
            allocation = self.kernel.allocate_file_seed(f"token_{len(self.token_registry):03d}", token_str)
            coordinates = allocation["coordinate_vector"]
            domain = allocation["manifold_domain"]
        else:
            radius = math.sqrt(len(self.token_registry)) * self.kernel.PHI
            theta = len(self.token_registry) * self.kernel.GOLDEN_ANGLE
            x = radius * math.cos(theta) * 0.10
            y = radius * math.sin(theta) * 0.10
            z = -float(len(self.token_registry) * self.kernel.PHI_SIXTH_UNIT)
            coordinates = (x, y, z)
            domain = -1
            
        return {
            "token": token_str,
            "entropy": entropy,
            "variance": variance,
            "assigned_coordinates": coordinates,
            "manifold_domain": domain,
            "status": kernel_intervention
        }
