from agent import ask
from models import ToolChoice
import agent


def test_notes():

    agent.choose_tool = lambda question: ToolChoice(
        tool="notes_lookup",
        input="physics viva"
    )

    result = ask("When is my physics viva?")

    assert result.tool_used == "notes_lookup"