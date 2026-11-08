from typing import Literal

from pydantic import BaseModel, Field

from support_agent.state import Category


class SupportRequest(BaseModel):
    user_id: str = Field(min_length=1)
    message: str = Field(min_length=3, max_length=4000)


class SupportResponse(BaseModel):
    category: Category
    status: Literal["completed", "needs_human_review"]
    answer: str
    ticket_required: bool
    ticket_id: str | None = None
