from typing import Literal, TypedDict

Category = Literal["access", "incident", "how_to", "other"]
Status = Literal["in_progress", "completed", "needs_human_review"]


class SupportState(TypedDict, total=False):
    user_id: str
    message: str
    category: Category
    draft_answer: str
    risk_reasons: list[str]
    requires_human_review: bool
    ticket_id: str | None
    ticket_required: bool
    status: Status
    final_answer: str
