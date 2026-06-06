from agent import ask
from models import ToolChoice
import agent


def test_calculator():

    agent.choose_tool = lambda question: ToolChoice(
        tool="calculator",
        input="2450 * 0.18"
    )

    result = ask("What is 18% of 2450?")

    assert result.answer == "441"
    assert result.tool_used == "calculator"