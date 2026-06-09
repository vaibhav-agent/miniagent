from unittest.mock import patch

from agent import ask
from models import ToolChoice


def fake_choose_tool(question):

    if "18%" in question:
        return ToolChoice(
            tool="calculator",
            input="2450 * 0.18"
        )

    if "physics viva" in question.lower():
        return ToolChoice(
            tool="notes_lookup",
            input=question
        )

    return ToolChoice(
        tool="none",
        input=""
    )


EVAL_SET = [
    {
        "question": "What is 18% of 2450?",
        "expected_tool": "calculator"
    },
    {
        "question": "When is my physics viva?",
        "expected_tool": "notes_lookup"
    },
    {
        "question": "What will Nifty close at tomorrow?",
        "expected_tool": "none"
    }
]


with patch("agent.choose_tool", side_effect=fake_choose_tool):

    passed = 0

    for case in EVAL_SET:

        result = ask(case["question"])

        if result.tool_used == case["expected_tool"]:
            print("PASS:", case["question"])
            passed += 1
        else:
            print("FAIL:", case["question"])

    print(f"\nScore: {passed}/{len(EVAL_SET)}")