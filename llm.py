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

Return ONLY valid JSON.

Examples:

{"tool":"calculator","tool_input":"500 * 0.20"}

{"tool":"notes_lookup","tool_input":"physics viva"}

{"tool":"none","tool_input":""}
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
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            text = response.json()["response"]

            print("\nMODEL RAW OUTPUT:")
            print(text)

            return ToolChoice.model_validate_json(text)

        except Exception as e:

            print("\nLLM ERROR:")
            print(type(e).__name__)
            print(e)

    raise ValueError("Model failed twice")