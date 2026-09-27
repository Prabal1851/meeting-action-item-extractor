from pydantic import BaseModel, Field
from typing import Optional


class ActionItem(BaseModel):
    task: str = Field(description="The specific action or task to be done")
    owner: Optional[str] = Field(default=None, description="Person responsible; null if unclear")
    deadline: Optional[str] = Field(default=None, description="Deadline in YYYY-MM-DD if stated or inferable, else null")
    confidence: float = Field(description="0-1 score of extraction confidence", ge=0, le=1)
    raw_quote: str = Field(description="The exact sentence this was extracted from")


class ExtractionResult(BaseModel):
    action_items: list[ActionItem]