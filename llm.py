import os

from anthropic import Anthropic
from dotenv import load_dotenv

from models import ToolChoice

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


SYSTEM_PROMPT = """
You are a tool-selection agent.

Available tools:

calculator
- arithmetic
- percentages
- numerical calculations

notes_lookup
- questions about stored notes
- exams
- viva schedules

none
- use when no available tool can help

Return ONLY JSON.

Return ONLY valid JSON.

Do not use markdown.
Do not use code fences.
Do not explain your answer.

Example:

{"tool":"calculator","input":"2450 * 0.18"}
"""


def choose_tool(question: str) -> ToolChoice:

    for _ in range(2):

        try:

            response = client.messages.create(
                model="claude-sonnet-4-0",
                max_tokens=100,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            text = response.content[0].text

            return ToolChoice.model_validate_json(text)

        except Exception:
            pass

    raise ValueError(
        "Model failed to produce valid ToolChoice"
    )