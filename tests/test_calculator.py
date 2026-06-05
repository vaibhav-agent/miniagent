from agent import ask

def test_calculator():
    result = ask("What is 18% of 2450?")

    assert result.answer == "441"
    assert result.tool_used == "calculator"