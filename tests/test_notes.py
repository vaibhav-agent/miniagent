from agent import ask

def test_notes():
    result = ask("When is my physics viva?")

    assert result.tool_used == "notes_lookup"
