"""
Run this first: python diagnose.py
It tests Ollama directly, outside of any agent code.
"""
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma2:2b"

print("=== Step 1: Raw Ollama call ===")
try:
    payload = {
        "model": MODEL,
        "prompt": 'Reply with only this JSON, nothing else: {"tool": "calculator", "tool_input": "2450 * 0.18"}',
        "stream": False,
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=30)
    print(f"HTTP status: {r.status_code}")
    print(f"Raw response body:\n{r.text[:2000]}")
    print()

    data = r.json()
    print(f"Parsed JSON keys: {list(data.keys())}")
    print(f"'response' field: {repr(data.get('response', 'KEY MISSING'))}")

except Exception as e:
    print(f"EXCEPTION: {type(e).__name__}: {e}")

print("\n=== Step 2: Pydantic parse test ===")
try:
    from models import ToolChoice
    test = '{"tool": "calculator", "tool_input": "2450 * 0.18"}'
    result = ToolChoice.model_validate_json(test)
    print(f"Pydantic parse OK: {result}")
except Exception as e:
    print(f"Pydantic FAILED: {type(e).__name__}: {e}")