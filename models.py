from pydantic import BaseModel
from typing import Literal


class AgentResult(BaseModel):
    answer: str
    tool_used: Literal["calculator", "notes_lookup", "none"]
    confident: bool


class ToolChoice(BaseModel):
    tool: Literal["calculator", "notes_lookup", "none"]
    input: str