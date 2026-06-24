from pydantic import BaseModel
from typing import Literal, Optional
class AgentResult(BaseModel):
    answer: str
    tool_used: Literal["calculator", "notes_lookup", "none"]
    confident: bool

    expression: Optional[str] = None   
    source: Optional[str] = None       
class ToolChoice(BaseModel):
    tool: Literal["calculator", "notes_lookup", "none"]
    tool_input: str   