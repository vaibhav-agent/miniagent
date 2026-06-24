from models import AgentResult
from tools import calculator, notes_lookup
from llm import choose_tool, get_direct_answer, answer_from_notes

def ask(question: str) -> AgentResult:
    """
    The agent loop — one question in, one structured AgentResult out.
    Flow:
        1. Ask the LLM which tool to use  (choose_tool)
        2. Run the tool in Python          (calculator / notes_lookup / none)
        3. If the tool fetches data,
           ask the LLM to interpret it    (get_direct_answer / answer_from_notes)
        4. Return a validated AgentResult
    The model only decides and interprets.
    Python runs every tool.  Never the other way around.
    """
    try:
        choice = choose_tool(question)
    except Exception as e:
        print(f"[agent] tool selection failed: {e}")
        return AgentResult(
            answer="I couldn't decide which tool to use. Please try again.",
            tool_used="none",
            confident=False,
        )

    print(f"\n[agent] chose tool: {choice.tool!r}  input: {choice.tool_input!r}")

    if choice.tool == "calculator":
        return _run_calculator(choice.tool_input)

    elif choice.tool == "notes_lookup":
        return _run_notes_lookup(question, choice.tool_input)

    else:
        # tool == "none": either a direct-knowledge question or unanswerable
        return _run_direct(question)

def _run_calculator(expression: str) -> AgentResult:
    """Python runs the calculator. The model never does the arithmetic."""
    try:
        result = calculator(expression)

        if result.startswith("Error:"):
            return AgentResult(
                answer=f"The calculation failed: {result}",
                tool_used="calculator",
                confident=False,
            )

        return AgentResult(
            answer=result,
            tool_used="calculator",
            confident=True,
            expression=expression,
        )

    except Exception as e:
        return AgentResult(
            answer=f"Calculator error: {e}",
            tool_used="calculator",
            confident=False,
        )


def _run_notes_lookup(question: str, query: str) -> AgentResult:
    """
    Python fetches the notes file.
    Then the LLM reads the contents and extracts the specific answer.
    """
    try:
        notes = notes_lookup(query)
        if notes["content"].startswith("Error:"):
            return AgentResult(
                answer=notes["content"],
                tool_used="notes_lookup",
                confident=False,
            )
        answer = answer_from_notes(question, notes["content"])
        if answer.strip() == "NOT_IN_NOTES":
            return AgentResult(
                answer="I found your notes but couldn't find the answer there.",
                tool_used="notes_lookup",
                confident=False,
            )
        return AgentResult(
            answer=answer,
            tool_used="notes_lookup",
            confident=True,
            source=notes["source"],
        )
    except Exception as e:
        return AgentResult(
            answer=f"Notes lookup failed: {e}",
            tool_used="notes_lookup",
            confident=False,
        )


def _run_direct(question: str) -> AgentResult:
    """
    For tool="none" — the model either answers from general knowledge
    or admits it cannot answer. These are two different outcomes.
    """
    try:
        answer = get_direct_answer(question)
        if answer.strip() == "CANNOT_ANSWER":
            return AgentResult(
                answer="I don't have a tool for this, and I can't answer it reliably.",
                tool_used="none",
                confident=False,
            )

        return AgentResult(
            answer=answer,
            tool_used="none",
            confident=True,
        )

    except Exception as e:
        return AgentResult(
            answer=f"Direct answer failed: {e}",
            tool_used="none",
            confident=False,
        )