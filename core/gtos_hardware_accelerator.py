# core/gtos_hardware_accelerator.py
import ctypes

class GTOSAcceleratorControlBlock(ctypes.BigEndianStructure):
    """
    GTOS Phase 5.2 Core: Hardware Accelerator Control Registers.
    Maps real-time GIO metrics directly to simulated hardware NPU/GPU 
    compute registers for deep parallel topology streaming.
    """
    _pack_ = 1  # Enforce strict 1-byte raw hardware packing boundary
    _fields_ = [
        ("command_trigger_flag", ctypes.c_uint8),  # 1 byte: 0x01 = RUN COMPUTE, 0x00 = IDLE
        ("active_manifold_state", ctypes.c_int8),  # 1 byte: Domain routing indicator (1 or -1)
        ("token_entropy_register", ctypes.c_double),# 8 bytes: Raw Shannon metric interface
        ("token_variance_register", ctypes.c_double) # 8 bytes: Statistical variance matrix pin
    ]                                               # Total = Exactly 18 bytes unpadded hardware space

class GTOSHardwareAcceleratorInterface:
    """
    Simulates bare-metal hardware register bus management. Coordinates
    offloading raw software vector loads to high-speed compute execution blocks.
    """
    def __init__(self):
        self.register_footprint_bytes: int = ctypes.sizeof(GTOSAcceleratorControlBlock)
        if self.register_footprint_bytes != 18:
            raise RuntimeError(f"ACCEL_ALIGN_FAULT: Footprint misaligned: {self.register_footprint_bytes}/18")

    def map_metrics_to_hardware_bus(self, command_bit: int, manifold: int, entropy: float, variance: float) -> GTOSAcceleratorControlBlock:
        """
        Direct Register Write: Commits raw GIO metrics onto the physical 
        accelerator pin layout, preparing the hardware engine for parallel computation.
        """
        return GTOSAcceleratorControlBlock(
            command_trigger_flag=int(command_bit) & 0xFF,
            active_manifold_state=int(manifold),
            token_entropy_register=float(entropy),
            token_variance_register=float(variance)
        )

    def trigger_npu_compute_cycle(self, control_block: GTOSAcceleratorControlBlock) -> str:
        """
        Executes a hardware execution step. Reads the control block registers 
        and validates if the hardware interface accepted the offloaded metrics loop.
        """
        if control_block.command_trigger_flag != 0x01:
            return "ACCEL_STATE: ACCELERATOR_IDLE_HOLDING"
            
        # Simulating hardware interrupt trapping for boundary checks
        if control_block.token_entropy_register > 2.5:
            return "ACCEL_INTERRUPT: GEOMETRIC_DIVERGENCE_TRAPPED"
            
        return "ACCEL_STATE: COMPUTE_SUCCESS_VECTOR_READY"
