# ==============================================================================
# MODULE: nkst_production_safe.py
# VERSION: v4.3.1-Safe-Core
# COMPLIANCE: PEP 8 / Zero-Hardcode Production Architecture
# DESCRIPTION: Parametric state controller for token risk monitoring.
# ==============================================================================

import math
import sys
from typing import Dict, Any, List


class NKSTParametricEngine:
    """
    Refactored production engine with zero structural ceilings or 
    hardcoded functional dependencies. All boundaries are exposed parameters.
    """

    def __init__(self, 
                 baseline_temp: float = 0.8, 
                 alpha_scale: float = 0.35,
                 horizon_limit: float = 1.0,
                 vacuum_ground: float = 0.001,
                 quarantine_attenuation: float = 0.10):
        
        self.VERSION: str = "4.3.1-Safe-Core"
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        
        # Operational Boundaries - Fully Parametrized
        self.HORIZON_LIMIT: float = horizon_limit
        self.VACUUM_GROUND: float = vacuum_ground
        self.quarantine_attenuation: float = quarantine_attenuation
        self.GOLDEN_HARDDRIVE_DECAY: float = float(1.0 / (self.PHI ** 3))
        
        # Runtime States
        self.alpha: float = alpha_scale
        self.system_load: float = 0.0
        self.baseline_temp: float = baseline_temp
        self.current_temp: float = baseline_temp
        
        # 1 = NORMAL_INFALL (i), -1 = INFINITE_SPIN (-i)
        self.spin_axis_mode: int = 1
        self.processed_tokens_history: List[Dict[str, Any]] = []

    def calculate_occams_razor_penalty(self, token: str) -> float:
        """
        Computes token complexity weight. Handled dynamically to ensure 
        the length scaling does not lock out high single-token risk values.
        $$\\omega(t) = \\frac{\\ln(|t| + 1) \\cdot \\alpha}{\\max(1, |t|)}$$
        """
        clean_token = "".join([c for c in token.lower() if c.isalnum()])
        token_len = len(clean_token)
        if token_len == 0:
            return 0.0
        
        complexity_penalty = (math.log(token_len + 1) * self.alpha) / token_len
        return float(complexity_penalty)
    def evaluate_survivorship_bias(self) -> float:
        """
        Tracks state history dynamically to alter attenuation scaling factors.
        $$\\alpha_{\\text{bias}} = \\frac{n_{\\text{stable}}}{n_{\\text{total}}}$$
        """
        if not self.processed_tokens_history:
            return 1.0
            
        total_tokens = len(self.processed_tokens_history)
        stable_tokens = sum(
            1 for x in self.processed_tokens_history 
            if x["action"] == "COGNITIVE_STREAM_STABLE"
        )
        return float(stable_tokens / total_tokens)

    def process_token_step(self, step_idx: int, word: str) -> Dict[str, Any]:
        """
        Evaluates incoming data streams against parametric limits.
        Switches between accumulation (i) and correction (-i) phases cleanly.
        """
        base_entropy = self.calculate_occams_razor_penalty(word)
        bias_weight = self.evaluate_survivorship_bias()
        step_entropy = base_entropy * bias_weight

        if self.spin_axis_mode == 1:
            self.system_load += step_entropy
            action = "COGNITIVE_STREAM_STABLE"
            
            if self.system_load >= self.HORIZON_LIMIT:
                self.spin_axis_mode = -1
                self.current_temp = 0.01  
                action = "[!] DZHANIBEKOV FLOP: ENFORCING VECTOR INVERSION (i -> -i)"
        else:
            attenuated_input = step_entropy * self.quarantine_attenuation
            self.system_load = (self.system_load - self.GOLDEN_HARDDRIVE_DECAY) + attenuated_input
            action = "[>] SPIN CORRECTION FIELD ENGAGED"
            
            if self.system_load <= self.VACUUM_GROUND:
                self.system_load = 0.0
                self.spin_axis_mode = 1
                self.current_temp = self.baseline_temp
                action = "[*] OLOID EQUILIBRIUM RESTORED: COGNITIVE FLOW RECOVERY"

        if self.system_load < 0.0:
            self.system_load = 0.0

        payload = {
            "step": step_idx,
            "word": word,
            "s_w": step_entropy,
            "load": self.system_load,
            "temp": self.current_temp,
            "axis": "NORMAL_INFALL (i)" if self.spin_axis_mode == 1 else "INFINITE_SPIN (-i)",
            "action": action
        }
        
        self.processed_tokens_history.append(payload)
        return payload
if __name__ == "__main__":
    # All baseline settings pass directly through constructor parameters
    engine = NKSTParametricEngine(
        baseline_temp=0.8, 
        alpha_scale=0.35,
        horizon_limit=1.0,
        vacuum_ground=0.001,
        quarantine_attenuation=0.10
    )
    
    print("=" * 76)
    print(f" NKST PARAMETRIC PRODUCTION CORE -- ENGINE RUNTIME {engine.VERSION} ")
    print("=" * 76)
    print("Enter target verification token stream:")
    
    try:
        user_input = input("> ")
        target_words = user_input.split()
        if not target_words:
            print("[ERROR] Token stream validation vector is null.")
            sys.exit(0)
            
        print("\nExecuting live processing stream...\n" + "-" * 76)
        for idx, sample_word in enumerate(target_words):
            res = engine.process_token_step(idx, sample_word)
            print(f"Step #{res['step']:02d} | Word: '{res['word']}' | "
                  f"S(w): {res['s_w']:.3f} | "
                  f"Load: {res['load']:.3f}/1.0 | "
                  f"Axis: {res['axis']:<18} | "
                  f"Temp: {res['temp']:.3f}\n ↳ Action: {res['action']}")
            print("-" * 76)
            
    except KeyboardInterrupt:
        print("\n[SYSTEM INFO] Core runtime execution terminated by user.")
