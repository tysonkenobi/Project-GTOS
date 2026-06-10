import json
import urllib.request
from typing import Dict, Any, List

class GTOSTerimnalAIBridge:
    """
    GTOS Phase 4 Core: AI Ingestion Bridge.
    Connects the unified GTOS Kernel Core Executive to a locally running
    open-weights AI model, piping the output text directly into the 
    geometric memory layers.
    """
    def __init__(self, local_endpoint: str = "http://localhost:11434/api/generate"):
        self.endpoint = local_endpoint
        # Default target model running locally (e.g., Llama 3.2 1B or similar)
        self.model_tag = "llama3.2:1b"

    def query_local_model_stream(self, prompt_string: str) -> str:
        """
        Pipes a user prompt directly to the local AI engine.
        Returns the raw string output to be handed off to the GTOS Token Bridge.
        """
        payload = {
            "model": self.model_tag,
            "prompt": prompt_string,
            "stream": False
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.endpoint, 
                data=data, 
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "").strip()
                
        except Exception:
            # Silent Failover Baseline: Returns an ungrounded string to intentionally 
            # test the kernel's anomaly intercept systems if the local AI isn't booted.
            return "UNGROUNDED_FALLBACK_SIGNAL: SYSTEM ANOMALY RADIAL DRIFT DETECTED"
