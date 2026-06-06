from models import AgentResult
from llm import choose_tool
from tools import calculator, notes_lookup


def execute_tool(tool_name: str, tool_input: str) -> str:

    if tool_name == "calculator":
        return calculator(tool_input)

    if tool_name == "notes_lookup":
        return notes_lookup(tool_input)

    return "No tool used."


def ask(question: str) -> AgentResult:

    try:
        choice = choose_tool(question)

    except Exception:
        return AgentResult(
            answer="Tool selection failed.",
            tool_used="none",
            confident=False
        )

    try:
        result = execute_tool(
            choice.tool,
            choice.input
        )

        return AgentResult(
            answer=result,
            tool_used=choice.tool,
            confident=True
        )

    except Exception:

        return AgentResult(
            answer="Tool execution failed.",
            tool_used=choice.tool,
            confident=False
        )