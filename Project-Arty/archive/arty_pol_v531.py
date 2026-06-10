# ==============================================================================
# MODULE: arty_pol_v531_logged.py
# VERSION: v5.3.1-Logged-Production
# COMPLIANCE: PEP 8 / Zero-Hardcode Non-Disruptive Architecture
# DESCRIPTION: Unified simulation core that actively exports session telemetry.
# ==============================================================================

import math
import sys
import random
import json
from typing import Dict, Any, List

class NKSTParametricEngine:
    """
    NKST Core Engine (v5.2.2 Auto-Calibrated)
    Features an active scale factor adjustment to trigger state changes
    reliably when high-entropy tokens are encountered.
    """
    def __init__(self, baseline_temp: float = 0.8, alpha_scale: float = 0.35, 
                 horizon_limit: float = 1.0, vacuum_ground: float = 0.001, 
                 quarantine_attenuation: float = 0.10):
        self.VERSION: str = "5.2.2-AutoCalibrated"
        self.PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
        
        # Operational Boundaries - Fully Parametrized
        self.HORIZON_LIMIT: float = horizon_limit
        self.VACUUM_GROUND: float = vacuum_ground
        self.quarantine_attenuation: float = quarantine_attenuation
        
        # NKST FRAMEWORK USE: 1/phi^3 golden hardrive decay constant
        self.GOLDEN_HARDDRIVE_DECAY: float = float(1.0 / (self.PHI ** 3))
        
        # Runtime States
        self.alpha: float = alpha_scale
        self.system_load: float = 0.0
        self.baseline_temp: float = baseline_temp
        self.current_temp: float = baseline_temp
        
        # NKST FRAMEWORK USE: State tracking (1 = NORMAL_INFALL (i), -1 = INFINITE_SPIN (-i))
        self.spin_axis_mode: int = 1
        self.processed_tokens_history: List[Dict[str, Any]] = []

    def calculate_occams_razor_penalty(self, token: str) -> float:
        """
        NKST FRAMEWORK USE: Occams razor equation.
        Computes token complexity weight using an algebraic scale factor.
        """
        clean_token = "".join([c for c in token.lower() if c.isalnum()])
        token_len = len(clean_token)
        if token_len == 0:
            return 0.0
        
        base_complexity = (math.log(token_len + 1) * self.alpha) / token_len
        scale_factor = 1.0 / (1.0 + math.log(token_len + 1))
        
        return float(base_complexity * scale_factor)
    def evaluate_survivorship_bias(self, predictive_entropy: float) -> float:
        """
        NKST FRAMEWORK USE: Survivorship bias modelling.
        Evaluates historical patterns predictively to adjust step weights.
        """
        if not self.processed_tokens_history:
            return 1.0
            
        total_tokens = len(self.processed_tokens_history) + 1
        stable_tokens = sum(
            1 for x in self.processed_tokens_history 
            if "STABLE" in x["action"]
        )
        
        if (self.system_load + predictive_entropy) >= self.HORIZON_LIMIT:
            return float(stable_tokens / total_tokens)
            
        return float((stable_tokens + 1) / total_tokens)

    def process_token_step(self, step_idx: int, word: str) -> Dict[str, Any]:
        """
        NKST FRAMEWORK USE: Dynamic inversion loop (i -> -i) and phase transitions.
        Processes incoming data streams and triggers corrections at the horizon limit.
        """
        base_entropy = self.calculate_occams_razor_penalty(word)
        bias_weight = self.evaluate_survivorship_bias(base_entropy)
        step_entropy = base_entropy * bias_weight
        
        if self.spin_axis_mode == 1:
            self.system_load += step_entropy
            action = "COGNITIVE_STREAM_STABLE"
            
            if self.system_load >= self.HORIZON_LIMIT:
                # NKST FRAMEWORK USE: Oloid dzhanibekov flop inversion use
                self.spin_axis_mode = -1
                self.current_temp = 0.01
                action = "[!] DZHANIBEKOV FLOP: ENFORCING VECTOR INVERSION (i -> -i)"
        else:
            attenuated_input = step_entropy * self.quarantine_attenuation
            self.system_load = (self.system_load - self.GOLDEN_HARDDRIVE_DECAY) + attenuated_input
            action = "[>] SPIN CORRECTION FIELD ENGAGED"
            
            if self.system_load <= self.VACUUM_GROUND:
                # NKST FRAMEWORK USE: Oloid equilibrium restoration phase (-i -> i)
                self.spin_axis_mode = 1
                self.current_temp = self.baseline_temp
                action = "[*] OLOID EQUILIBRIUM RESTORED: COGNITIVE FLOW RECOVERY"
                
        if self.system_load < 0.0:
            self.system_load = 0.0
            
        payload = {
            "step": step_idx, "word": word, "s_w": step_entropy, "load": self.system_load,
            "temp": self.current_temp,
            "axis": "NORMAL_INFALL (i)" if self.spin_axis_mode == 1 else "INFINITE_SPIN (-i)",
            "action": action
        }
        self.processed_tokens_history.append(payload)
        return payload
class LiveTransformerSimulator:
    """
    Simulates an autoregressive generation loop where the engine's output
    temperature actively adjusts token selection paths.
    """
    def __init__(self, engine: NKSTParametricEngine):
        self.engine = engine
        self.vocabulary: Dict[str, List[str]] = {
            "FACTUAL": ["is", "a", "known", "scientific", "fact", "verified", "by", "data"],
            "HALLUCINATION": ["hyperdimensional-quantum-flux", "matrix-overdrive-biocentric", "unregulated-anomaly"]
        }

    def simulate_next_token(self, current_temp: float) -> str:
        if current_temp <= 0.01:
            return random.choice(self.vocabulary["FACTUAL"])
        if random.random() > 0.30:
            return random.choice(self.vocabulary["HALLUCINATION"])
        return random.choice(self.vocabulary["FACTUAL"])

    def run_generation_loop(self, max_steps: int = 12, export_filename: str = "nkst_session_log.json"):
        """
        NKST FRAMEWORK USE: Continuous loop execution showing phase changes.
        Actively dumps the resulting history log directly onto physical storage.
        """
        print("=" * 76)
        print(f" LIVE NKST TRANSFORMER SIMULATION ENGINE RUNTIME v5.3.1 ")
        print("=" * 76)
        
        current_word = "Initialization"
        
        for step in range(max_steps):
            res = self.engine.process_token_step(step, current_word)
            
            print(f"Step #{res['step']:02d} | Generated: '{res['word']:<32}' | "
                  f"Load: {res['load']:.3f}/{self.engine.HORIZON_LIMIT:.2f} | "
                  f"Axis: {res['axis']:<18} | "
                  f"Temp: {res['temp']:.3f}\n ↳ Action: {res['action']}")
            print("-" * 76)
            
            current_word = self.simulate_next_token(res['temp'])
            
        # ACTIVE LOG EXPORT FUNCTION CALL
        output_payload = {
            "engine_version": self.engine.VERSION,
            "configured_horizon": self.engine.HORIZON_LIMIT,
            "session_history": self.engine.processed_tokens_history
        }
        
        try:
            with open(export_filename, "w", encoding="utf-8") as f:
                json.dump(output_payload, f, indent=4)
            print(f"\n[SUCCESS] Session telemetry successfully exported to: ./{export_filename}\n")
        except IOError as e:
            print(f"\n[ERROR] Failed to save logging telemetry file: {e}\n")

if __name__ == "__main__":
    calibrated_engine = NKSTParametricEngine(horizon_limit=0.10)
    simulator = LiveTransformerSimulator(calibrated_engine)
    
    # Run the loop and specify the targeted local export filename
    simulator.run_generation_loop(max_steps=12, export_filename="nkst_session_log.json")
