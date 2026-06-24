# print("===LLM.PY LOADED===")

# import os
# import re
# import requests
# from dotenv import load_dotenv
# from models import ToolChoice

# load_dotenv()

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL = "gemma2:2b"
# TIMEOUT = 30
# MAX_RETRIES = 3

# TOOL_SELECTION_PROMPT = """\
# You are a tool-selection agent. Given a question, pick one tool.

# Tools:
# - calculator   : arithmetic, percentages, any math
# - notes_lookup : questions about the user's personal notes or schedule
# - none         : questions answerable from general knowledge, OR unanswerable questions

# Rules:
# 1. Reply with ONLY a JSON object — no explanation, no markdown fences.
# 2. Use exactly these keys: "tool" and "tool_input".
# 3. "tool" must be one of: calculator, notes_lookup, none
# 4. "tool_input" is the expression or search query (empty string for none).

# Q: What is 18% of 2450?
# {{"tool": "calculator", "tool_input": "2450 * 0.18"}}

# Q: When is my physics viva?
# {{"tool": "notes_lookup", "tool_input": "physics viva date"}}

# Q: Give me a one-line definition of an embedding.
# {{"tool": "none", "tool_input": ""}}

# Q: What will Nifty close at tomorrow?
# {{"tool": "none", "tool_input": ""}}

# Q: {question}
# """

# DIRECT_ANSWER_PROMPT = """\
# Answer the following question in one or two sentences.
# If you genuinely cannot answer (future data, predictions, live prices), reply with exactly: CANNOT_ANSWER

# Question: {question}
# """

# NOTES_ANSWER_PROMPT = """\
# Below are the user's notes. Answer their question using only what is in the notes.
# If the answer is not in the notes, reply with exactly: NOT_IN_NOTES

# Question: {query}

# Notes:
# {content}
# """


# def _post(prompt: str) -> str:
#     print("[llm] _post: sending request...")
#     try:
#         payload = {"model": MODEL, "prompt": prompt, "stream": False}
#         response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
#         print(f"[llm] _post: got HTTP {response.status_code}")
#         response.raise_for_status()
#         data = response.json()
#         print(f"[llm] _post: response keys: {list(data.keys())}")
#         text = data["response"].strip()
#         print(f"[llm] _post: response text: {repr(text)}")
#         return text
#     except Exception as e:
#         print(f"[llm] _post EXCEPTION: {type(e).__name__}: {e}")
#         raise


# def _extract_json(raw: str) -> str:
#     match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
#     if match:
#         return match.group(0)
#     raise ValueError(f"No JSON found: {repr(raw)}")


# def choose_tool(question: str) -> ToolChoice:
#     print(f"[llm] choose_tool: question={repr(question)}")
#     prompt = TOOL_SELECTION_PROMPT.format(question=question)
#     for attempt in range(1, MAX_RETRIES + 1):
#         raw = ""
#         try:
#             raw = _post(prompt)
#             print(f"[llm] attempt {attempt} raw: {repr(raw)}")
#             json_str = _extract_json(raw)
#             print(f"[llm] extracted: {json_str}")
#             return ToolChoice.model_validate_json(json_str)
#         except Exception as e:
#             print(f"[llm] attempt {attempt} FAILED: {type(e).__name__}: {e}")
#             if attempt == MAX_RETRIES:
#                 raise ValueError(f"All attempts failed. Last raw: {repr(raw)}")


# def get_direct_answer(question: str) -> str:
#     prompt = DIRECT_ANSWER_PROMPT.format(question=question)
#     for attempt in range(1, MAX_RETRIES + 1):
#         try:
#             raw = _post(prompt)
#             print(f"[llm] direct_answer: {repr(raw)}")
#             return raw
#         except Exception as e:
#             print(f"[llm] attempt {attempt} FAILED: {type(e).__name__}: {e}")
#             if attempt == MAX_RETRIES:
#                 raise ValueError("Direct answer failed")


# def answer_from_notes(query: str, content: str) -> str:
#     prompt = NOTES_ANSWER_PROMPT.format(query=query, content=content)
#     for attempt in range(1, MAX_RETRIES + 1):
#         try:
#             raw = _post(prompt)
#             print(f"[llm] notes_answer: {repr(raw)}")
#             return raw
#         except Exception as e:
#             print(f"[llm] attempt {attempt} FAILED: {type(e).__name__}: {e}")
#             if attempt == MAX_RETRIES:
#                 raise ValueError("Notes answer failed")

import os
import re
import requests
from dotenv import load_dotenv
from models import ToolChoice

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma2:2b"
TIMEOUT = 30
MAX_RETRIES = 3

TOOL_SELECTION_PROMPT = """\
You are a tool-selection agent. Given a question, pick one tool.

Tools:
- calculator   : arithmetic, percentages, any math
- notes_lookup : questions about the user's personal notes or schedule
- none         : questions answerable from general knowledge, OR unanswerable questions

Rules:
1. Reply with ONLY a JSON object — no explanation, no markdown fences.
2. Use exactly these keys: "tool" and "tool_input".
3. "tool" must be one of: calculator, notes_lookup, none
4. "tool_input" is the expression or search query (empty string for none).

Q: What is 18% of 2450?
{{"tool": "calculator", "tool_input": "2450 * 0.18"}}

Q: When is my physics viva?
{{"tool": "notes_lookup", "tool_input": "physics viva date"}}

Q: Give me a one-line definition of an embedding.
{{"tool": "none", "tool_input": ""}}

Q: What will Nifty close at tomorrow?
{{"tool": "none", "tool_input": ""}}

Q: {question}
"""

DIRECT_ANSWER_PROMPT = """\
Answer the following question in one or two sentences.
If you genuinely cannot answer (future data, predictions, live prices), reply with exactly: CANNOT_ANSWER

Question: {question}
"""

NOTES_ANSWER_PROMPT = """\
Below are the user's notes. Answer their question using only what is in the notes.
If the answer is not in the notes, reply with exactly: NOT_IN_NOTES

Question: {query}

Notes:
{content}
"""


def _post(prompt: str) -> str:
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()["response"].strip()


def _extract_json(raw: str) -> str:
    match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError(f"No JSON found in model output: {repr(raw)}")


def choose_tool(question: str) -> ToolChoice:
    prompt = TOOL_SELECTION_PROMPT.format(question=question)
    for attempt in range(1, MAX_RETRIES + 1):
        raw = ""
        try:
            raw = _post(prompt)
            json_str = _extract_json(raw)
            return ToolChoice.model_validate_json(json_str)
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise ValueError(f"Tool selection failed after {MAX_RETRIES} attempts: {e}")


def get_direct_answer(question: str) -> str:
    prompt = DIRECT_ANSWER_PROMPT.format(question=question)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return _post(prompt)
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise ValueError(f"Direct answer failed: {e}")


def answer_from_notes(query: str, content: str) -> str:
    prompt = NOTES_ANSWER_PROMPT.format(query=query, content=content)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return _post(prompt)
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise ValueError(f"Notes answer failed: {e}")