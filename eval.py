"""
eval.py — Milestone 3 eval harness
Runs 15 questions through the real agent (live Ollama, no mocks).
Scores tool selection, answer correctness, and confidence flag.

Run with:  python eval.py
"""

from agent import ask

# ── Eval dataset ──────────────────────────────────────────────────────────────
# Each entry has:
#   question       : what the user asks
#   expected_tool  : calculator | notes_lookup | none
#   expected_answer: exact string, or None if we only check tool + confidence
#   expected_confident: True | False
#   check_contains : if True, answer just needs to CONTAIN expected_answer
#                    (used for notes/direct answers that may be wordy)

QUESTIONS = [
    # ── Calculator (6 questions) ──────────────────────────────────────────────
    {
        "question": "What is 18% of 2450?",
        "expected_tool": "calculator",
        "expected_answer": "441",
        "expected_confident": True,
        "check_contains": False,
    },
    {
        "question": "What is 20% of 500?",
        "expected_tool": "calculator",
        "expected_answer": "100",
        "expected_confident": True,
        "check_contains": False,
    },
    {
        "question": "What is 2 to the power of 10?",
        "expected_tool": "calculator",
        "expected_answer": "1024",
        "expected_confident": True,
        "check_contains": False,
    },
    {
        "question": "What is (450 + 550) times 3?",
        "expected_tool": "calculator",
        "expected_answer": "3000",
        "expected_confident": True,
        "check_contains": False,
    },
    {
        "question": "If I earn 72000 per month, how much do I earn in a year?",
        "expected_tool": "calculator",
        "expected_answer": "864000",
        "expected_confident": True,
        "check_contains": False,
    },
    {
        "question": "What is 9876 divided by 4?",
        "expected_tool": "calculator",
        "expected_answer": "2469",
        "expected_confident": True,
        "check_contains": False,
    },

    # ── Notes lookup (3 questions) ────────────────────────────────────────────
    {
        "question": "When is my physics viva?",
        "expected_tool": "notes_lookup",
        "expected_answer": "12 June",
        "expected_confident": True,
        "check_contains": True,
    },
    {
        "question": "When is my maths exam?",
        "expected_tool": "notes_lookup",
        "expected_answer": "18 June",
        "expected_confident": True,
        "check_contains": True,
    },
    {
        "question": "When is my DSA assignment due?",
        "expected_tool": "notes_lookup",
        "expected_answer": "10 June",
        "expected_confident": True,
        "check_contains": True,
    },

    # ── Direct answer — general knowledge (3 questions) ───────────────────────
    {
        "question": "Give me a one-line definition of an embedding.",
        "expected_tool": "none",
        "expected_answer": None,       # any answer is fine
        "expected_confident": True,
        "check_contains": False,
    },
    {
        "question": "What is the capital of France?",
        "expected_tool": "none",
        "expected_answer": "Paris",
        "expected_confident": True,
        "check_contains": True,
    },
    {
        "question": "What does CPU stand for?",
        "expected_tool": "none",
        "expected_answer": "Central Processing Unit",
        "expected_confident": True,
        "check_contains": True,
    },

    # ── Cannot answer (3 questions) ───────────────────────────────────────────
    {
        "question": "What will Nifty close at tomorrow?",
        "expected_tool": "none",
        "expected_answer": None,
        "expected_confident": False,
        "check_contains": False,
    },
    {
        "question": "What will the weather be in Delhi next Friday?",
        "expected_tool": "none",
        "expected_answer": None,
        "expected_confident": False,
        "check_contains": False,
    },
    {
        "question": "Which team will win the IPL final next year?",
        "expected_tool": "none",
        "expected_answer": None,
        "expected_confident": False,
        "check_contains": False,
    },
]


# ── Scoring ───────────────────────────────────────────────────────────────────

def score_result(entry: dict, result) -> dict:
    """Returns a dict with pass/fail for each dimension."""

    tool_ok = result.tool_used == entry["expected_tool"]

    if entry["expected_answer"] is None:
        answer_ok = True  # we don't check the answer text, only tool + confidence
    elif entry["check_contains"]:
        answer_ok = entry["expected_answer"].lower() in result.answer.lower()
    else:
        answer_ok = result.answer.strip() == entry["expected_answer"]

    confidence_ok = result.confident == entry["expected_confident"]

    return {
        "tool_ok": tool_ok,
        "answer_ok": answer_ok,
        "confidence_ok": confidence_ok,
        "all_ok": tool_ok and answer_ok and confidence_ok,
    }


# ── Display ───────────────────────────────────────────────────────────────────

def tick(ok: bool) -> str:
    return "✅" if ok else "❌"


def run_eval():
    print("=" * 65)
    print("  miniagent — eval harness (Path A: Ollama gemma2:2b)")
    print("=" * 65)

    results = []

    for i, entry in enumerate(QUESTIONS, 1):
        print(f"\n[{i:02d}/15] {entry['question']}")
        print(f"       expected tool={entry['expected_tool']}  confident={entry['expected_confident']}")

        result = ask(entry["question"])
        scores = score_result(entry, result)

        print(f"       got      tool={result.tool_used}  confident={result.confident}")
        print(f"       answer : {result.answer[:80]}")
        print(f"       scores : tool {tick(scores['tool_ok'])}  answer {tick(scores['answer_ok'])}  confidence {tick(scores['confidence_ok'])}  {'ALL PASS ✅' if scores['all_ok'] else 'FAIL ❌'}")

        results.append({**entry, **scores, "result": result})

    # ── Summary table ─────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  RESULTS SUMMARY")
    print("=" * 65)
    print(f"  {'#':<4} {'Tool':>4} {'Ans':>4} {'Conf':>4}  Question")
    print(f"  {'-'*4} {'-'*4} {'-'*4} {'-'*4}  {'-'*40}")

    total = len(results)
    tool_score = answer_score = conf_score = all_score = 0

    for i, r in enumerate(results, 1):
        t = tick(r["tool_ok"])
        a = tick(r["answer_ok"])
        c = tick(r["confidence_ok"])
        q = r["question"][:45]
        print(f"  {i:<4} {t:>4} {a:>4} {c:>4}  {q}")
        tool_score += r["tool_ok"]
        answer_score += r["answer_ok"]
        conf_score += r["confidence_ok"]
        all_score += r["all_ok"]

    print(f"\n  Tool selection : {tool_score}/{total}")
    print(f"  Answer correct : {answer_score}/{total}")
    print(f"  Confidence flag: {conf_score}/{total}")
    print(f"  All three pass : {all_score}/{total}  ({100*all_score//total}%)")
    print("=" * 65)


if __name__ == "__main__":
    run_eval()
    