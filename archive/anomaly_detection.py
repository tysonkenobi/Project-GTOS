# core/anomaly_detection.py
import math
import numpy as np
from typing import Dict, Any, Tuple, List

class GTOSAnomalyDetector:
    """
    GTOS Phase 6 Core: Geometric Distance & Drift Threshold Classifier (Refactored).
    Enforces strict serialization on tracking parameters to guarantee 
    unpadded primitive alignment for hardware registers under parallel load.
    """
    def __init__(self, baseline_threshold: float = 3.5, window_size: int = 10):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.GOLDEN_ANGLE: float = float(2.0 * math.pi * (1.0 - (1.0 / self.PHI)))
        self.DRIFT_THRESHOLD: float = float(baseline_threshold)
        self.WINDOW_SIZE: int = int(window_size)
        self.drift_velocity_history: List[float] = []

    def calculate_ideal_node_position(self, sequence_index: int) -> Tuple[float, float, float]:
        """
        Derives the mathematically pure reference coordinate vector for a given sequence step.
        """
        step = int(sequence_index) + 1
        radius = math.sqrt(float(step)) * self.PHI
        theta = float(step) * self.GOLDEN_ANGLE
        
        x = float(radius * math.cos(theta))
        y = float(radius * math.sin(theta))
        z = float(step / (6.0 * (self.PHI ** 3)))
        return (x, y, z)

    def evaluate_vector_drift(self, actual_coords: Tuple[float, float, float], sequence_index: int) -> Dict[str, Any]:
        """
        Computes absolute spatial distance deviations and flattens parameters into raw primitives.
        """
        # Unpack incoming coordinate tuples explicitly to destroy thread type wrappers
        act_x, act_y, act_z = actual_coords
        clean_actual = (float(act_x), float(act_y), float(act_z))
        
        ideal_coords = self.calculate_ideal_node_position(sequence_index)
        id_x, id_y, id_z = ideal_coords

        v_actual = np.array(clean_actual, dtype=np.float64)
        v_ideal = np.array(ideal_coords, dtype=np.float64)
        spatial_distance = float(np.linalg.norm(v_actual - v_ideal))

        self.drift_velocity_history.append(spatial_distance)
        if len(self.drift_velocity_history) > self.WINDOW_SIZE:
            self.drift_velocity_history.pop(0)

        rolling_momentum = float(np.mean(self.drift_velocity_history))

        is_drifting = bool(spatial_distance > self.DRIFT_THRESHOLD or rolling_momentum > (self.DRIFT_THRESHOLD * 0.7))
        status_tag = "BOUNDS_VIOLATION_DETECTED" if is_drifting else "BOUNDS_NORMAL"

        return {
            "spatial_distance_delta": float(spatial_distance),
            "rolling_momentum_velocity": float(rolling_momentum),
            "ref_ideal_x": float(id_x),
            "ref_ideal_y": float(id_y),
            "ref_ideal_z": float(id_z),
            "is_drifting": is_drifting,
            "classification": str(status_tag)
        }
