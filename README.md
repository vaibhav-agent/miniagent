# miniagent — a tiny AI agent you can actually understand

> **Read this first. This README is the contract.**
> It describes what *miniagent* does for the person using it — *before* a single
> line of code is written. You build the code to make this document true. If you
> later decide the behaviour should change, change this README first, then make
> the code match. The README always leads; the code always follows.

---

## 1. Who this is for and why it exists

You ask a question at the terminal. Some questions need a calculation, some need
a fact looked up in your own notes, and some the assistant can just answer.
**miniagent** is a small command-line assistant that figures out *which* of those
it needs, does it, and gives you a clear, predictable answer every time.

It is built from scratch — no agent framework — so you can see exactly how an AI
agent decides what to do. (This is the loop you described to me: messages, tools,
and memory, where the model only *chooses* the next tool and *you* write what each
tool actually does.)

## 2. Quickstart

```bash
# 1. clone your repo and enter it
git clone <your-private-repo-url>
cd miniagent

# 2. install
uv sync                      # or: pip install -r requirements.txt

# 3. set your model key
export ANTHROPIC_API_KEY=...   # never commit this

# 4. ask it something
uv run miniagent "What is 18% of 2,450?"
```

## 3. What the user sees (this is the behaviour you must build)

**A calculation question:**

```
$ uv run miniagent "What is 18% of 2,450?"

🤔 thinking… (chose tool: calculator)
✅ Answer: 441
   How I got it: calculator("2450 * 0.18") = 441
```

**A question about the user's own notes:**

```
$ uv run miniagent "When is my physics viva?"

🤔 thinking… (chose tool: notes_lookup)
✅ Answer: Your physics viva is on 12 June, 10:00 AM.
   Source: notes/college.md
```

**A question it can just answer:**

```
$ uv run miniagent "Give me a one-line definition of an embedding."

🤔 thinking… (no tool needed)
✅ Answer: An embedding is a list of numbers that represents the meaning of
   something so a computer can compare it to other things.
```

**A question it cannot answer:**

```
$ uv run miniagent "What will Nifty close at tomorrow?"

🤔 thinking…
🛑 I can't answer that reliably. I don't have a tool for live or future data.
```

## 4. The rules it must always follow (the contract)

1. **Every reply is structured, never free-form text the program can't trust.**
   Internally the agent must return an object that matches this shape, validated
   with **Pydantic** — if the model returns anything else, the program rejects it
   and retries rather than printing garbage:

   ```python
   class AgentResult(BaseModel):
       answer: str
       tool_used: Literal["calculator", "notes_lookup", "none"]
       confident: bool
   ```

2. **The model only decides; your code does.** The model picks the tool and its
   input. Your Python code runs the tool and feeds the result back. The model
   never does the arithmetic or invents a file's contents itself.

3. **When it doesn't know, it says so.** `confident: false` → it must tell the
   user it can't answer, not guess.

4. **It never loops forever.** Maximum 3 tool calls per question, then it answers
   with what it has (or admits it's stuck).

## 5. Definition of done

You're finished with v1 when *all* of these are true:

- [ ] The four example sessions in §3 work end to end.
- [ ] Every model reply is parsed through the Pydantic `AgentResult`; a malformed
      reply triggers one retry, then a clean error — never a crash.
- [ ] There is a `tests/` folder with a small **test harness** that checks the
      contract: feed in a known question, assert the right tool was chosen and the
      answer is correct. Include at least one test for the "can't answer" path.
- [ ] `README.md` still matches what the program actually does. (If you changed
      behaviour, you changed this file first.)

## 6. Not in scope for v1 (don't build these yet)

- Live web/internet data
- A chat UI or web app
- More than two tools
- Remembering past conversations across runs

Keep it small. Small and *fully understood* beats big and fuzzy.

---

*Why write the README before the code? Because you are not really coding for the
computer — you are coding for the person who will use this. Decide what their
experience should be first, agree on it, and then work backwards to build it.
That habit — customer first, contract first — is the difference between an
engineer and someone who just makes the computer do things.*