from agent import ask
from models import ToolChoice
import agent


def test_unknown():

    agent.choose_tool = lambda question: ToolChoice(
        tool="none",
        input=""
    )

    result = ask("What will Nifty close at tomorrow?")

    assert result.tool_used == "none"