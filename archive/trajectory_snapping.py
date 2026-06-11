import math
from typing import Dict, Any, List

class GTOSTrajectorySnapper:
    """
    GTOS Phase 2.2 Core: Geometric Vector Realignment Engine.
    Intercepts anomalous data strings flagged by the memory firewall and applies
    forceful data sanitization by restoring the text payload to a stable baseline state.
    """
    def __init__(self, history_capacity: int = 10):
        self.history_capacity = history_capacity
        self.stable_context_buffer: List[str] = []

    def register_safe_state(self, valid_payload: str) -> None:
        self.stable_context_buffer.append(valid_payload)
        if len(self.stable_context_buffer) > self.history_capacity:
            self.stable_context_buffer.pop(0)

    def scrub_and_snap_payload(self, current_payload: str, firewall_report: Dict[str, Any]) -> str:
        if firewall_report.get("classification") == "BOUNDS_VIOLATION_DETECTED":
            if self.stable_context_buffer:
                return self.stable_context_buffer[-1]
            return "RECOVERY_FALLBACK_CORE_RESET"
            
        self.register_safe_state(current_payload)
        return current_payload
