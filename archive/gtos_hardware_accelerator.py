# core/gtos_hardware_accelerator.py
import ctypes

class GTOSAcceleratorControlBlock(ctypes.BigEndianStructure):
    """
    GTOS Phase 5.2 Core: Hardware Accelerator Control Registers.
    Maps real-time GIO metrics directly to simulated hardware NPU/GPU 
    compute registers for deep parallel topology streaming with strict packing.
    """
    _pack_ = 1 
    _fields_ = [
        ("command_trigger_flag", ctypes.c_uint8), 
        ("active_manifold_state", ctypes.c_int8), 
        ("token_entropy_register", ctypes.c_double),
        ("token_variance_register", ctypes.c_double) 
    ] 

class GTOSHardwareAcceleratorInterface:
    """
    Simulates bare-metal hardware register bus management.
    Coordinates offloading raw software vector loads to high-speed compute 
    execution blocks with absolute primitive type isolation.
    """
    def __init__(self):
        self.register_footprint_bytes: int = ctypes.sizeof(GTOSAcceleratorControlBlock)
        if self.register_footprint_bytes != 18:
            raise RuntimeError(f"ACCEL_ALIGN_FAULT: Footprint misaligned: {self.register_footprint_bytes}/18")

    def map_metrics_to_hardware_bus(self, command_bit: int, manifold: int, entropy: float, variance: float) -> GTOSAcceleratorControlBlock:
        """
        Direct Register Write: Commits raw GIO metrics onto the physical accelerator 
        pin layout, stripping out all high-level runtime metadata objects.
        """
        # Phase 6 Enforcement: Isolate values into pristine primitive variables
        clean_cmd = int(int(command_bit) & 0xFF)
        clean_manifold = int(manifold)
        clean_entropy = float(entropy)
        clean_variance = float(variance)

        return GTOSAcceleratorControlBlock(
            command_trigger_flag=clean_cmd,
            active_manifold_state=clean_manifold,
            token_entropy_register=clean_entropy,
            token_variance_register=clean_variance
        )

    def trigger_npu_compute_cycle(self, control_block: GTOSAcceleratorControlBlock) -> str:
        """
        Executes a hardware execution step.
        Reads the control block registers and validates metrics loop compliance.
        """
        if int(control_block.command_trigger_flag) != 0x01:
            return "ACCEL_STATE: ACCELERATOR_IDLE_HOLDING" 
            
        if float(control_block.token_entropy_register) > 2.5:
            return "ACCEL_INTERRUPT: GEOMETRIC_DIVERGENCE_TRAPPED" 
            
        return "ACCEL_STATE: COMPUTE_SUCCESS_VECTOR_READY"
