# core/gtos_ai_driver.py
import ctypes

try:
    from gtos_hal_ai_compute import GTOSHALAIComputeDriver
except ImportError:
    # Fallback to keep the module completely decoupled if loaded independently
    GTOSHALAIComputeDriver = None

class GTOSAIDriver:
    """
    GTOS Phase 6.3 Core: Low-Latency Voice & AI Device Driver.
    Completely eliminates legacy subprocess execution leaks and string block 
    allocations by streaming tokens straight into contiguous hardware RAM layouts.
    """
    def __init__(self):
        self.model_tag = "llama3.2:1b"
        # Native VOICE Foundation: Bind directly to the low-level compute layer
        if GTOSHALAIComputeDriver is not None:
            self.compute_driver = GTOSHALAIComputeDriver()
        else:
            self.compute_driver = None

    def stream_inference_token(self, buffer_frame: ctypes.Structure, incoming_token: str) -> bool:
        """
        Unified Memory Paging: Wires the active token stream straight into the 
        contiguous memory frame payload space using low-level byte pointer writes.
        """
        if not incoming_token or not hasattr(buffer_frame, 'active_token_length'):
            return False
            
        token_bytes = incoming_token.encode('utf-8')
        new_length = buffer_frame.active_token_length + len(token_bytes)
        
        if new_length > buffer_frame.allocated_capacity:
            return False
            
        # Target payload address: skip initial 8 bytes of structural headers
        dest_address = ctypes.addressof(buffer_frame) + 8 + buffer_frame.active_token_length
        ctypes.memmove(dest_address, token_bytes, len(token_bytes))
        
        buffer_frame.active_token_length = new_length
        return True

    def extract_and_sanitize_vector(self, raw_logits) -> list:
        """
        Phase 6.3 Concurrency Overhaul: Intercepts multi-dimensional background 
        telemetry vectors (like numpy ndarrays) at the driver boundary. Sanitizes
        them into raw float primitives before they hit unpadded register loops.
        """
        if hasattr(raw_logits, "tolist"):
            return [float(x) for x in raw_logits.tolist()]
        if isinstance(raw_logits, (list, tuple)):
            return [float(x) for x in raw_logits]
        return [float(raw_logits)]
