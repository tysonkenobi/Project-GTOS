from typing import Dict, Any, Union
import numpy as np

# Phase 1 to Phase 3 Imports
from gtos_core_memory import GTOSKernelMemoryController
from gtos_token_bridge import GTOSTokenBridge
from vector_redirection import GTOSVectorRedirectionEngine
from gtos_storage_core import GTOSStorageCore
from anomaly_detection import GTOSAnomalyDetector

# New Phase 5.1 Hardware Abstraction Layer Import
from gtos_hal_mmu import GTOSHardwareMMU

class GTOSKernelCoreExecutive:
    """
    GTOS Main Kernel Executive (v1.2.0 HAL-Integrated).
    The central runtime hub that instantiates, links, and orchestrates all
    verified geometric subsystem engines and maps data to the physical MMU bus.
    """
    def __init__(self, boundary_threshold: float = 0.10, drift_threshold: float = 3.5):
        # 1. Instantiate Core Logic Subsystems
        self.memory = GTOSKernelMemoryController(boundary_threshold=boundary_threshold)
        self.token_bridge = GTOSTokenBridge(memory_controller=self.memory)
        self.fault_engine = GTOSVectorRedirectionEngine(buffer_size=16)
        self.storage = GTOSStorageCore()
        self.anomaly_detector = GTOSAnomalyDetector(baseline_threshold=drift_threshold, window_size=10)
        
        # 2. Instantiate Phase 5.1 Simulated Hardware Memory Chip (256 pages * 24 bytes)
        self.hal_mmu = GTOSHardwareMMU(total_pages=256)

        # Kernel State Invariants
        self.kernel_status = "BOOTED_EXECUTION_READY"

    def system_write_file(self, file_id: str, data_payload: str) -> bytes:
        """
        Core API: Compresses a text payload to a 24-byte seed, and immediately
        commits that seed to a physical page address inside the flat RAM bus.
        """
        # Step A: Pack text string down into a rigid 24-byte binary seed
        packed_seed = self.storage.compress_payload_to_seed(file_id, data_payload)
        
        # Step B: Direct HAL Intercept — Route the raw binary seed straight onto the physical array bus
        self.hal_mmu.write_coordinate_to_physical_ram(file_id, packed_seed)
        
        return packed_seed

    def system_read_file(self, file_id: str) -> Union[str, None]:
        """
        Core API: Locates the physical page address off the hardware memory bus,
        extracts the raw 24 bytes, and runs the inverse geometric reconstruction.
        """
        # Step A: Query the physical byte array bus directly via the HAL MMU
        hardware_bytes = self.hal_mmu.read_coordinate_from_physical_ram(file_id)
        
        if hardware_bytes is None:
            return None
            
        # Step B: Pass the extracted hardware bytes back to the decompression table
        return self.storage.decompress_seed_to_payload(file_id)

    def system_process_math(self, numerator: float, denominator: float) -> Union[float, Dict[str, Any]]:
        """ Core API: Safe arithmetic route passing faults to the cyclic buffer. """
        return self.fault_engine.execute_core_division(numerator, denominator)

    def system_ingest_token(self, token_str: str, raw_logits: np.ndarray) -> Dict[str, Any]:
        """ Core API: Bridges ingestion and firewall checks simultaneously. """
        route_report = self.token_bridge.intercept_and_route_token(token_str, raw_logits)
        assigned_vector = route_report["assigned_coordinates"]
        sequence_step = len(self.token_bridge.token_registry) - 1
        
        firewall_report = self.anomaly_detector.evaluate_vector_drift(assigned_vector, sequence_step)
        
        return {
            "token": token_str,
            "coordinates": assigned_vector,
            "manifold_domain": route_report["manifold_domain"],
            "spatial_drift": firewall_report["spatial_distance_delta"],
            "rolling_momentum": firewall_report["rolling_momentum_velocity"],
            "firewall_classification": firewall_report["classification"]
        }
