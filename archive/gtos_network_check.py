import json
import urllib.request

endpoint = "http://127.0.0"
payload = {"model": "llama3.2:1b", "prompt": "test", "stream": False}
data = json.dumps(payload).encode("utf-8")

req = urllib.request.Request(
    endpoint, 
    data=data, 
    headers={"Content-Type": "application/json", "User-Agent": "Diagnostic/1.0"}
)

print("[Diagnostic] Attempting Python loopback transport handshake...")
try:
    with urllib.request.urlopen(req, timeout=5) as response:
        print("[SUCCESS] Response received from Ollama server!")
except Exception as e:
    import traceback
    print("\n🚨 UNMASKED PYTHON ERROR ENCOUNTERED:")
    traceback.print_exc()
