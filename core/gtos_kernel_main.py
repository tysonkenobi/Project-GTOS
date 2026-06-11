# core/gtos_kernel_main.py
from typing import Dict, Any, Union
import numpy as np
import math

# Phase 1 to Phase 4 Core Logic Subsystems
from gtos_core_memory import GTOSKernelMemoryController
from gtos_token_bridge import GTOSTokenBridge
from vector_redirection import GTOSVectorRedirectionEngine
from gtos_storage_core import GTOSStorageCore
from anomaly_detection import GTOSAnomalyDetector

# Phase 5 Hardware Abstraction Layer Components
from gtos_hal_mmu import GTOSHardwareMMU
from gtos_hardware_accelerator import GTOSHardwareAcceleratorInterface

class GTOSKernelCoreExecutive:
    """
    GTOS Main Kernel Executive (v1.3.0 HAL-Accelerated).
    The central runtime hub that instantiates, links, and orchestrates all 
    verified geometric subsystem engines. Enforces strict dual-manifold 
    mathematical invariants and primitive types across unpadded hardware registers.
    """
    def __init__(self, boundary_threshold: float = 0.10, drift_threshold: float = 3.5):
        # 1. Core Mathematical Constants Injection
        self.PHI: float = float((1.0 + math.sqrt(5.0)) / 2.0)
        self.GOLDEN_ANGLE: float = float(2.0 * math.pi * (1.0 - (1.0 / self.PHI)))
        
        # 2. Instantiate Core Logic Subsystems
        self.memory = GTOSKernelMemoryController(boundary_threshold=boundary_threshold)
        self.token_bridge = GTOSTokenBridge(memory_controller=self.memory)
        self.fault_engine = GTOSVectorRedirectionEngine(buffer_size=16)
        self.storage = GTOSStorageCore()
        self.anomaly_detector = GTOSAnomalyDetector(baseline_threshold=drift_threshold, window_size=10)

        # 3. Instantiate Phase 5 Simulated Hardware Components
        self.hal_mmu = GTOSHardwareMMU(total_pages=256)
        self.accelerator = GTOSHardwareAcceleratorInterface()

        # Kernel State Invariants
        self.kernel_status = "BOOTED_ACCELERATION_READY"

    def system_write_file(self, file_id: str, data_payload: str) -> bytes:
        """
        Core API: Compresses a text payload to a 24-byte seed, and immediately 
        commits that seed to a physical page address inside the flat RAM bus.
        """
        packed_seed = self.storage.compress_payload_to_seed(file_id, data_payload)
        self.hal_mmu.write_coordinate_to_physical_ram(file_id, packed_seed)
        return packed_seed

    def system_read_file(self, file_id: str) -> Union[str, None]:
        """
        Core API: Locates the physical page address off the hardware memory bus, 
        extracts the raw 24 bytes, and runs the inverse geometric reconstruction.
        """
        hardware_bytes = self.hal_mmu.read_coordinate_from_physical_ram(file_id)
        if hardware_bytes is None:
            return None
        return self.storage.decompress_seed_to_payload(file_id)

    def system_process_math(self, numerator: float, denominator: float) -> Union[float, int]:
        """
        Core API: Safe arithmetic route passing faults to the cyclic buffer.
        Wired: Captures ZeroDivision faults, sets the low-level I/O registers, 
        and maps the explicit hexadecimal interrupt execution vector.
        """
        execution_result = self.fault_engine.execute_core_division(numerator, denominator)
        
        # If a dictionary is returned, the math engine caught an exception trap
        if isinstance(execution_result, dict):
            # Phase 6.3 Dual-Manifold Error Isolation: Route fault directly via register map
            clean_numerator = float(numerator)
            vector_address = self.hal_mmu.register_map.trigger_hardware_interrupt("ZERO_DIVISION_FAULT", clean_numerator)
            return vector_address 
            
        return float(execution_result)

    def system_ingest_token(self, token_str: str, raw_logits: np.ndarray) -> str:
        """
        Core API: Intercepts token vectors and offloads them to unpadded hardware registers.
        Wired: Evaluates Shannon entropy, verifies dual-manifold drift limits, 
        and triggers a simulated hardware accelerator cycle step.
        """
        # Step A: Process raw software routing vectors
        route_report = self.token_bridge.intercept_and_route_token(token_str, raw_logits)
        
        # Unpack flat spatial coordinate primitives to bypass high-level container noise
        cx = float(route_report["coord_x"])
        cy = float(route_report["coord_y"])
        cz = float(route_report["coord_z"])
        assigned_vector = (cx, cy, cz)
        
        sequence_step = int(len(self.token_bridge.token_registry)) - 1

        # Step B: Check spatial drift via dual-manifold firewall limits
        firewall_report = self.anomaly_detector.evaluate_vector_drift(assigned_vector, sequence_step)
        
        if firewall_report["classification"] == "BOUNDS_VIOLATION_DETECTED":
            # Fire the hardware interrupt lines for a spatial boundary trap
            self.hal_mmu.register_map.trigger_hardware_interrupt("SPATIAL_FIREWALL_BREACH", 0.0)

        # Step C: Direct Hardware Offloading via Golden Space Invariants
        clean_manifold = int(route_report["manifold_domain"])
        clean_entropy = float(route_report["entropy"])
        clean_variance = float(route_report["variance"])

        # Pack raw metrics into the unpadded 18-byte accelerator control registers
        control_block = self.accelerator.map_metrics_to_hardware_bus(
            command_bit=1, 
            manifold=clean_manifold,
            entropy=clean_entropy,
            variance=clean_variance
        )

        # Trigger physical hardware NPU loop cycle response
        hardware_response = self.accelerator.trigger_npu_compute_cycle(control_block)
        return str(hardware_response)
