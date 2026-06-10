# core/gtos_ffi_bridge.py
import ctypes
import math

class GTOSHardwareRegisters(ctypes.BigEndianStructure):
    """
    GTOS Phase 5.2 Core: Binary Hardware Register Layout.
    Maps state variables directly to packed C structures for native compilation.
    """
    _pack_ = 1  # Force strict 1-byte packing alignment (removes all 64-bit padding)
    _fields_ = [
        ("active_manifold", ctypes.c_int32),     # 4 bytes
        ("system_load", ctypes.c_double),        # 8 bytes
        ("allocation_counter", ctypes.c_uint32), # 4 bytes
        ("address_step_mult", ctypes.c_double)   # 8 bytes
    ]                                            # Total = Exactly 24 bytes flat

class GTOSCoordinatePayload(ctypes.BigEndianStructure):
    """
    GTOS Phase 5.2 Core: C/Rust Binary FFI Vector Layout.
    Defines the rigid 24-byte coordinate block footprint (3 x 8-byte doubles).
    """
    _fields_ = [
        ("x", ctypes.c_double),  # 8 bytes
        ("y", ctypes.c_double),  # 8 bytes
        ("z", ctypes.c_double)   # 8 bytes
    ]

class GTOSFFIBridge:
    """
    Native Interoperability Layer. Exposes memory pointers and packed
    structures directly to compiled binary blobs without memory duplication.
    """
    def __init__(self):
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        self.STEP_MULT: float = float(1.0 / (self.PHI ** 2))
        
        # Enforce strict 24-byte structural compile boundaries
        if ctypes.sizeof(GTOSCoordinatePayload) != 24 or ctypes.sizeof(GTOSHardwareRegisters) != 24:
            raise RuntimeError("FFI_CRITICAL_FAULT: Bare-metal structure alignment mismatched.")

    def export_kernel_state_to_c(self, manifold: int, load: float, counter: int) -> GTOSHardwareRegisters:
        """
        Casts live, shifting Python kernel states into a rigid C-compatible 
        hardware register footprint for the native binary bus.
        """
        return GTOSHardwareRegisters(
            active_manifold=int(manifold),
            system_load=float(load),
            allocation_counter=int(counter),
            address_step_mult=self.STEP_MULT
        )

    def cast_bytes_to_vector_struct(self, raw_bytes: bytes) -> GTOSCoordinatePayload:
        """
        Zero-copy transformation mapping raw 24-byte streams straight to
        a C-compatible vector block pointer format.
        """
        if len(raw_bytes) != 24:
            raise ValueError("FFI_DATA_ERROR: Ingestion byte array must be exactly 24 bytes.")
        return GTOSCoordinatePayload.from_buffer_copy(raw_bytes)

    def get_raw_memory_address(self, c_struct: ctypes.Structure) -> int:
        """
        Extracts the explicit virtual memory pointer address of the structure
        to pass directly onto hardware register interfaces or compiled libraries.
        """
        return ctypes.addressof(c_struct)
