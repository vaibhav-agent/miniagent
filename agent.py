from models import AgentResult
from tools import calculator, notes_lookup
from llm import choose_tool


def ask(question: str) -> AgentResult:

    try:
        choice = choose_tool(question)

    except Exception:

        return AgentResult(
            answer="Model failed to choose a tool.",
            tool_used="none",
            confident=False,
        )

    try:

        if choice.tool == "calculator":

            answer = calculator(choice.tool_input)

            return AgentResult(
                answer=answer,
                tool_used="calculator",
                confident=True,
            )

        elif choice.tool == "notes_lookup":

            answer = notes_lookup(choice.tool_input)

            return AgentResult(
                answer=answer,
                tool_used="notes_lookup",
                confident=True,
            )

        return AgentResult(
            answer="I can't answer that reliably.",
            tool_used="none",
            confident=False,
        )

    except Exception:

        return AgentResult(
            answer="Tool execution failed.",
            tool_used=choice.tool,
            confident=False,
        )