import math
import numpy as np
from typing import Dict, Any, Tuple, List

class GTOSAnomalyDetector:
    """
    GTOS Phase 2.2 Core: Geometric Distance & Drift Threshold Classifier.
    Tracks spatial token node placements and calculates rolling vector 
    trajectory deviations to enforce compliance with harmonic boundary conditions.
    """
    def __init__(self, baseline_threshold: float = 3.5, window_size: int = 10):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.GOLDEN_ANGLE: float = 2.0 * math.pi * (1.0 - (1.0 / self.PHI))
        self.DRIFT_THRESHOLD: float = baseline_threshold
        
        # Physical Memory Window: Tracks rolling spatial drift velocity over time
        self.WINDOW_SIZE = window_size
        self.drift_velocity_history: List[float] = []

    def calculate_ideal_node_position(self, sequence_index: int) -> Tuple[float, float, float]:
        """
        Derives the mathematically pure reference coordinate vector for 
        a given sequence step index using the system's log-spiral matrix.
        """
        step = sequence_index + 1
        radius = math.sqrt(step) * self.PHI
        theta = step * self.GOLDEN_ANGLE
        
        # Pure theoretical baseline coordinates
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        z = float(step / (6.0 * (self.PHI ** 3)))
        
        return (x, y, z)

    def evaluate_vector_drift(self, actual_coords: Tuple[float, float, float], sequence_index: int) -> Dict[str, Any]:
        """
        Computes the absolute spatial Euclidean distance between the generated 
        token position and its ideal geometric reference anchor point.
        Tracks rolling drift momentum to catch slow context decay.
        """
        ideal_coords = self.calculate_ideal_node_position(sequence_index)
        
        # Compute exact vector difference delta using numpy
        v_actual = np.array(actual_coords)
        v_ideal = np.array(ideal_coords)
        spatial_distance = float(np.linalg.norm(v_actual - v_ideal))
        
        # OS REGULATION: Track rolling drift momentum to catch slow context decay
        self.drift_velocity_history.append(spatial_distance)
        if len(self.drift_velocity_history) > self.WINDOW_SIZE:
            self.drift_velocity_history.pop(0)
            
        # Calculate localized acceleration (rolling average of distance deviation)
        rolling_momentum = float(np.mean(self.drift_velocity_history))
        
        # Absolute Firewall Check: Trigger violation if single step breaches threshold
        # OR if the rolling average momentum indicates a sustained data bleed
        is_drifting = bool(spatial_distance > self.DRIFT_THRESHOLD or rolling_momentum > (self.DRIFT_THRESHOLD * 0.7))
        status_tag = "BOUNDS_VIOLATION_DETECTED" if is_drifting else "BOUNDS_NORMAL"
        
        return {
            "spatial_distance_delta": spatial_distance,
            "rolling_momentum_velocity": rolling_momentum,
            "reference_ideal_vector": ideal_coords,
            "is_drifting": is_drifting,
            "classification": status_tag
        }
