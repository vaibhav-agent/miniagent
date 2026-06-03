from pydantic import BaseModel
from typing import Literal

class AgentResult(BaseModel):
    answer: str
    tool_used: Literal["calculator", "notes_lookup", "none"]
    confident: bool