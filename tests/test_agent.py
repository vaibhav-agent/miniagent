"""
tests/test_agent.py

Contract tests for miniagent — validates the README's "definition of done":
  - Right tool is chosen
  - Answer is correct
  - confident flag matches outcome
  - "can't answer" path works cleanly

Run with:  pytest tests/ -v
"""

import pytest
from unittest.mock import patch
from models import AgentResult, ToolChoice


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_tool_choice(tool: str, tool_input: str) -> ToolChoice:
    return ToolChoice(tool=tool, tool_input=tool_input)


# ── Calculator tests ──────────────────────────────────────────────────────────

class TestCalculator:

    def test_percentage_basic(self):
        """18% of 2450 = 441 — the README example."""
        with patch("agent.choose_tool", return_value=make_tool_choice("calculator", "2450 * 0.18")):
            from agent import ask
            result = ask("What is 18% of 2450?")
        assert result.tool_used == "calculator"
        assert result.answer == "441"
        assert result.confident is True

    def test_percentage_new(self):
        """15% of 8500 = 1275 — a question the README never gave."""
        with patch("agent.choose_tool", return_value=make_tool_choice("calculator", "8500 * 0.15")):
            from agent import ask
            result = ask("What is 15% of 8500?")
        assert result.tool_used == "calculator"
        assert result.answer == "1275"
        assert result.confident is True

    def test_power(self):
        """2 to the power of 10 = 1024."""
        with patch("agent.choose_tool", return_value=make_tool_choice("calculator", "2**10")):
            from agent import ask
            result = ask("What is 2 to the power of 10?")
        assert result.tool_used == "calculator"
        assert result.answer == "1024"
        assert result.confident is True

    def test_grouped_arithmetic(self):
        """(450 + 550) * 3 = 3000."""
        with patch("agent.choose_tool", return_value=make_tool_choice("calculator", "(450+550)*3")):
            from agent import ask
            result = ask("What is (450 + 550) times 3?")
        assert result.tool_used == "calculator"
        assert result.answer == "3000"
        assert result.confident is True

    def test_yearly_salary(self):
        """72000 * 12 = 864000."""
        with patch("agent.choose_tool", return_value=make_tool_choice("calculator", "72000 * 12")):
            from agent import ask
            result = ask("If I earn 72000 per month, how much in a year?")
        assert result.tool_used == "calculator"
        assert result.answer == "864000"
        assert result.confident is True

    def test_invalid_expression(self):
        """Calculator returns an error string → confident=False."""
        with patch("agent.choose_tool", return_value=make_tool_choice("calculator", "import os")):
            from agent import ask
            result = ask("Run some code")
        assert result.tool_used == "calculator"
        assert result.confident is False


# ── Notes lookup tests ────────────────────────────────────────────────────────

class TestNotesLookup:

    def test_physics_viva_found(self):
        """Physics viva is in the notes file — should return it confidently."""
        with patch("agent.choose_tool", return_value=make_tool_choice("notes_lookup", "physics viva date")):
            with patch("agent.answer_from_notes", return_value="Your physics viva is on 12 June, 10:00 AM."):
                from agent import ask
                result = ask("When is my physics viva?")
        assert result.tool_used == "notes_lookup"
        assert result.confident is True
        assert "12 June" in result.answer or "June" in result.answer

    def test_answer_not_in_notes(self):
        """Query for something not in the notes → confident=False."""
        with patch("agent.choose_tool", return_value=make_tool_choice("notes_lookup", "chemistry exam")):
            with patch("agent.answer_from_notes", return_value="NOT_IN_NOTES"):
                from agent import ask
                result = ask("When is my chemistry exam?")
        assert result.tool_used == "notes_lookup"
        assert result.confident is False

    def test_notes_file_missing(self):
        """If the notes file doesn't exist, return confident=False with a clear message."""
        with patch("agent.choose_tool", return_value=make_tool_choice("notes_lookup", "physics viva")):
            with patch("tools.open", side_effect=FileNotFoundError):
                from agent import ask
                result = ask("When is my physics viva?")
        assert result.tool_used == "notes_lookup"
        assert result.confident is False


# ── Direct answer / "none" tool tests ────────────────────────────────────────

class TestDirectAnswer:

    def test_general_knowledge(self):
        """Embedding definition — no tool needed, model answers directly."""
        mock_answer = "An embedding is a list of numbers that represents meaning."
        with patch("agent.choose_tool", return_value=make_tool_choice("none", "")):
            with patch("agent.get_direct_answer", return_value=mock_answer):
                from agent import ask
                result = ask("Give me a one-line definition of an embedding.")
        assert result.tool_used == "none"
        assert result.confident is True
        assert result.answer == mock_answer

    def test_unanswerable_question(self):
        """Future market prediction → CANNOT_ANSWER → confident=False."""
        with patch("agent.choose_tool", return_value=make_tool_choice("none", "")):
            with patch("agent.get_direct_answer", return_value="CANNOT_ANSWER"):
                from agent import ask
                result = ask("What will Nifty close at tomorrow?")
        assert result.tool_used == "none"
        assert result.confident is False

    def test_capital_city(self):
        """Capital of France — answerable from general knowledge."""
        mock_answer = "The capital of France is Paris."
        with patch("agent.choose_tool", return_value=make_tool_choice("none", "")):
            with patch("agent.get_direct_answer", return_value=mock_answer):
                from agent import ask
                result = ask("What is the capital of France?")
        assert result.tool_used == "none"
        assert result.confident is True


# ── Tool selection failure tests ──────────────────────────────────────────────

class TestFailurePaths:

    def test_tool_selection_failure(self):
        """If the LLM fails to choose a tool, return confident=False cleanly — no crash."""
        with patch("agent.choose_tool", side_effect=ValueError("Model failed")):
            from agent import ask
            result = ask("What is 18% of 2450?")
        assert isinstance(result, AgentResult)
        assert result.confident is False
        assert result.tool_used == "none"

    def test_result_is_always_agentresult(self):
        """Every code path must return a validated AgentResult — never a crash."""
        with patch("agent.choose_tool", side_effect=Exception("Unexpected error")):
            from agent import ask
            result = ask("anything")
        assert isinstance(result, AgentResult)