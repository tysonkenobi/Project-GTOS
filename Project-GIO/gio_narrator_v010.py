import numpy as np
from typing import Tuple, List, Dict, Any
from gio_v02 import GeometricInformationObserver

class PathRecountingWrapper:
    def __init__(self, observer: GeometricInformationObserver, vocabulary_mapping: List[str] = None):
        """
        vocabulary_mapping: A list where index matches token ID (for open weights) 
                            or None if using API string keys.
        """
        self.observer = observer
        self.vocab = vocabulary_mapping
        
        # History tracks
        self.trajectory_log = []     # List of state vectors
        self.metric_log = []         # List of compute_kappa Dicts
        self.token_history = []      # List of strings generated so far

    def push_step(self, current_state: np.ndarray, current_logits: np.ndarray, generated_token_str: str):
        """Passes information straight through to the core observer without altering it."""
        metrics = self.observer.compute_kappa(current_state, current_logits)
        
        # Save state snapshot and human-readable tracking token
        self.trajectory_log.append(current_state.copy())
        self.metric_log.append(metrics)
        self.token_history.append(generated_token_str)

    def detect_singularity(self) -> Tuple[bool, int]:
        """
        Scans history to see if a singularity occurred.
        Returns (True, index_of_deviation) if found, otherwise (False, -1).
        """
        if len(self.metric_log) < 3:
            return False, -1
            
        entropies = [m["entropy"] for m in self.metric_log]
        kappas = [m["kappa"] for m in self.metric_log]
        
        # Detection method 1: Sudden entropy spike
        for i in range(1, len(entropies)):
            entropy_acceleration = entropies[i] - entropies[i-1]
            # Threshold of 1.5 selected empirically; sensitivity parameter for further optimization
            if entropy_acceleration > 1.5:
                return True, i
    
        # Detection method 2: Sustained entropy collapse
        late_entropy = np.mean([entropies[i] for i in range(len(entropies)-5, len(entropies))])
        early_entropy = np.mean([entropies[i] for i in range(0, 5)])
    
        if early_entropy > 0 and (late_entropy / early_entropy) < 0.2:
            collapse_index = next(i for i in range(len(entropies)) if entropies[i] < early_entropy * 0.2)
            return True, collapse_index
            
        return False, -1

    def recount_path(self, divergence_index: int) -> str:
        """
        Uses the geometric logs to build a dynamic story of the breakdown.
        """
        total_steps = len(self.token_history)
        
        # 1. Isolate where things were stable vs where they broke
        stable_path = "".join(self.token_history[:divergence_index])
        broken_path = "".join(self.token_history[divergence_index:])
        
        # 2. Extract the physical metrics at the exact moment of failure
        failed_metrics = self.metric_log[divergence_index]
        
        # 3. Calculate total geometric distance traveled after the fracture
        start_failed_state = self.trajectory_log[divergence_index]
        final_state = self.trajectory_log[-1]
        dist = float(np.linalg.norm(final_state - start_failed_state))

        # 4. Construct a mathematically grounded explanation
        explanation = (
            f"I was processing the sequence normally up until: '{stable_path.strip()}'. "
            f"At that specific step, my internal entropy spiked sharply to {failed_metrics['entropy']:.2f}, "
            f"and my variance flattened to {failed_metrics['variance']:.2f}. "
            f"This caused a context degradation while attempting to parse the next tokens: '{broken_path.strip()}'. "
            f"Over the last {total_steps - divergence_index} tokens, my latent state drifted "
            f"by a geometric distance of {dist:.3f} into an ungrounded attractor loop, "
            f"causing me to lose clear spatial orientation of the sequence timeline."
        )
        return explanation
