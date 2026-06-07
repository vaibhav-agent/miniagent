from models import AgentResult


def test_agent_result():
    result = AgentResult(
        answer="441",
        tool_used="calculator",
        confident=True
    )

    assert result.answer == "441"
    assert result.tool_used == "calculator"
    assert result.confident is True
    