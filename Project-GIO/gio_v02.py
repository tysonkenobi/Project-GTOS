# ==============================================================================
# MODULE: geometric_observer_core.py
# VERSION: v0.2.0-Research-Clean
# TYPE: Passive Latent-State Instability Probe
# DESCRIPTION: Compares latent state drift vs output distribution instability
#              across baseline and perturbed stochastic processes.
# ==============================================================================

import math
import numpy as np
from typing import Dict, List, Tuple


# ==============================================================================
# OBSERVER CORE
# ==============================================================================

class GeometricInformationObserver:
    """
    Passive diagnostic probe for measuring:
    - latent state drift
    - output distribution entropy
    - logit variance stability
    """

    def __init__(self):
        self.previous_state = None

    def state_drift_energy(self, current: np.ndarray) -> float:
        """
        Squared L2 distance between consecutive latent states.
        Interpreted as 'state movement intensity'.
        """
        if self.previous_state is None:
            self.previous_state = current.copy()
            return 0.0

        delta = current - self.previous_state
        energy = float(np.dot(delta, delta))
        self.previous_state = current.copy()
        return energy

    def softmax(self, logits: np.ndarray) -> np.ndarray:
        shifted = logits - np.max(logits)
        exp_vals = np.exp(shifted)
        return exp_vals / np.sum(exp_vals)

    def entropy(self, probs: np.ndarray) -> float:
        return float(-np.sum(probs * np.log2(probs + 1e-12)))

    def variance(self, logits: np.ndarray) -> float:
        return float(np.var(logits))

    def compute_kappa(self, state: np.ndarray, logits: np.ndarray) -> Dict[str, float]:
        """
        Unified instability score.

        Kappa_t increases when:
        - latent state shifts rapidly
        - output distribution becomes uncertain
        """

        drift = self.state_drift_energy(state)

        probs = self.softmax(logits)
        h = self.entropy(probs)
        v = self.variance(logits)

        kappa = (drift * (1.0 + h)) / (1.0 + math.log1p(v))

        return {
            "kappa": float(kappa),
            "drift": float(drift),
            "entropy": float(h),
            "variance": float(v)
        }


# ==============================================================================
# SYNTHETIC PROCESS MODELS
# ==============================================================================

class BaseProcess:
    """
    Low-noise latent dynamics (baseline regime).
    """

    def __init__(self, dim: int = 64, vocab: int = 20, seed: int = 0):
        np.random.seed(seed)
        self.state = np.random.normal(0, 0.1, dim)
        self.W = np.random.normal(0, 1.0, (vocab, dim))

    def step(self, t: int, T: int):
        noise = np.random.normal(0, 0.05, self.state.shape)
        self.state = 0.95 * self.state + noise
        logits = self.W @ self.state
        return self.state.copy(), logits


class DriftProcess(BaseProcess):
    """
    Same system, but with progressive instability injection.
    """

    def step(self, t: int, T: int):
        progress = t / T

        noise = np.random.normal(0, 0.05, self.state.shape)

        if progress > 0.5:
            noise += np.random.normal(0.3, 0.15, self.state.shape) * (progress ** 2)

        self.state = 0.92 * self.state + noise
        logits = self.W @ self.state
        return self.state.copy(), logits


# ==============================================================================
# EXPERIMENT RUNNER
# ==============================================================================

def run_experiment(steps: int = 20):
    baseline = BaseProcess()
    drift = DriftProcess()

    obs_a = GeometricInformationObserver()
    obs_b = GeometricInformationObserver()

    print("\n=== LATENT STABILITY COMPARISON EXPERIMENT v0.2 ===\n")

    results = []

    for t in range(steps):

        sa, la = baseline.step(t, steps)
        sb, lb = drift.step(t, steps)

        ka = obs_a.compute_kappa(sa, la)
        kb = obs_b.compute_kappa(sb, lb)

        label_a = "BASELINE"
        label_b = "DRIFT"

        print(
            f"Step {t:02d} | "
            f"A(Kappa={ka['kappa']:.3f}, H={ka['entropy']:.3f}) "
            f"{label_a} || "
            f"B(Kappa={kb['kappa']:.3f}, H={kb['entropy']:.3f}) "
            f"{label_b}"
        )

        results.append({
            "t": t,
            "baseline": ka,
            "drift": kb
        })

    return results


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    run_experiment(steps=20)
