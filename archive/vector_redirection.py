# core/vector_redirection.py
import math
from typing import Dict, Any, Union, List

class GTOSVectorRedirectionEngine:
    """
    GTOS Phase 6 Core: Vector Redirection Engine (Refactored).
    Enforces strict primitive serialization on fault interception variables
    to prevent type leakage into unpadded machine-language registers.
    """
    def __init__(self, buffer_size: int = 16):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.BUFFER_SIZE: int = int(buffer_size)
        self.cyclic_buffer: List[Any] = [None] * self.BUFFER_SIZE
        self.write_pointer: int = 0

    def execute_core_division(self, numerator: float, denominator: float) -> Union[float, Dict[str, Any]]:
        try:
            # Force primitive float casting to strip any numpy/tuple wrapping noise
            return float(float(numerator) / float(denominator))
        except ZeroDivisionError:
            return self.convert_fault_to_cyclic_loop(float(numerator))

    def convert_fault_to_cyclic_loop(self, failed_numerator: float) -> Dict[str, Any]:
        self.cyclic_buffer = [None] * self.BUFFER_SIZE
        self.write_pointer = 0
        address_step_multiplier = float(1.0 / (self.PHI ** 2))
        
        return {
            "status": "CYCLIC_LOOP_ACTIVE",
            "fault_origin_value": float(failed_numerator),
            "address_step_multiplier": float(address_step_multiplier),
            "execution_state": "RUNNING_CYCLIC_BUFFER"
        }

    def push_to_fault_buffer(self, loop_state: Dict[str, Any], data_stream: str) -> int:
        step_modifier = float(loop_state["address_step_multiplier"])
        calculated_index = int((int(self.write_pointer) + step_modifier) * 10) % self.BUFFER_SIZE
        
        self.cyclic_buffer[calculated_index] = str(data_stream)
        self.write_pointer = (int(self.write_pointer) + 1) % self.BUFFER_SIZE
        return int(calculated_index)
