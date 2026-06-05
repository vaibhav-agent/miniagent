from agent import ask


def test_unknown():
    result = ask("What will Nifty close at tomorrow?")

    assert result.confident is False