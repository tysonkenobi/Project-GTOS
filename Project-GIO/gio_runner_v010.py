from gio_v02 import BaseProcess, DriftProcess, GeometricInformationObserver
from gio_narrator_v010 import PathRecountingWrapper

if __name__ == "__main__":
    drift = DriftProcess()
    observer = GeometricInformationObserver()
    wrapper = PathRecountingWrapper(observer)
    
    steps = 100
    for t in range(steps):
        state, logits = drift.step(t, steps)
        wrapper.push_step(state, logits, f"token_{t}")
    
    found, idx = wrapper.detect_singularity()
    
    if found:
        print(f"Singularity detected at step {idx}")
        print(wrapper.recount_path(idx))
    else:
        print("No singularity detected in this run.")
