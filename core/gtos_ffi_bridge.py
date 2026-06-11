# core/gtos_ffi_bridge.py
import ctypes
import math

class GTOSHardwareRegisters(ctypes.BigEndianStructure):
    """
    GTOS Phase 5.2 Core: Binary Hardware Register Layout.
    Maps state variables directly to packed C structures for native compilation.
    """
    _pack_ = 1 
    _fields_ = [
        ("active_manifold", ctypes.c_int32), 
        ("system_load", ctypes.c_double), 
        ("allocation_counter", ctypes.c_uint32), 
        ("address_step_mult", ctypes.c_double) 
    ] 

class GTOSCoordinatePayload(ctypes.BigEndianStructure):
    """
    GTOS Phase 5.2 Core: C/Rust Binary FFI Vector Layout.
    Defines the rigid 24-byte coordinate block footprint (3 x 8-byte doubles).
    """
    _fields_ = [
        ("x", ctypes.c_double), 
        ("y", ctypes.c_double), 
        ("z", ctypes.c_double) 
    ]

class GTOSFFIBridge:
    """
    Native Interoperability Layer.
    Exposes memory pointers and packed structures directly to compiled binary blobs without memory duplication.
    """
    def __init__(self):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.STEP_MULT: float = float(1.0 / (self.PHI ** 2)) 
        if ctypes.sizeof(GTOSCoordinatePayload) != 24 or ctypes.sizeof(GTOSHardwareRegisters) != 24:
            raise RuntimeError("FFI_CRITICAL_FAULT: Bare-metal structure alignment mismatched.")

    def export_kernel_state_to_c(self, manifold: int, load: float, counter: int) -> GTOSHardwareRegisters:
        return GTOSHardwareRegisters(
            active_manifold=int(manifold),
            system_load=float(load),
            allocation_counter=int(counter),
            address_step_mult=self.STEP_MULT
        )

    def cast_bytes_to_vector_struct(self, raw_bytes: bytes) -> GTOSCoordinatePayload:
        if len(raw_bytes) != 24:
            raise ValueError("FFI_DATA_ERROR: Ingestion byte array must be exactly 24 bytes.")
        return GTOSCoordinatePayload.from_buffer_copy(raw_bytes)

    def get_raw_memory_address(self, c_struct: ctypes.Structure) -> int:
        return ctypes.addressof(c_struct)

    def get_token_payload_pointer(self, buffer_frame: ctypes.Structure) -> int:
        """
        Phase 6.2 Zero-Copy Tracking: Extracts the raw virtual memory pointer 
        address of the active character array segment, completely skipping 
        the initial 8 bytes of control header tracking configurations.
        """
        return ctypes.addressof(buffer_frame) + 8
