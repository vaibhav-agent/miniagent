import requests

from models import ToolChoice


PROMPT = """
You are a tool selection agent.

Available tools:

calculator
- arithmetic
- percentages
- calculations

notes_lookup
- questions about stored notes

none
- if no tool can answer

Return ONLY JSON.

Example:

{"tool":"calculator","tool_input":"500 * 0.20"}
"""


def choose_tool(question: str) -> ToolChoice:

    payload = {
        "model": "gemma2:2b",
        "prompt": f"{PROMPT}\n\nQuestion: {question}",
        "stream": False,
    }

    for _ in range(2):

        try:

            response = requests.post(
                
                json=payload,
                timeout=30,
            )

            text = response.json()["response"]

            return ToolChoice.model_validate_json(text)

        except Exception:
            pass

    raise ValueError("Model failed twice")