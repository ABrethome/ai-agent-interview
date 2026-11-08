from fastapi import FastAPI

from support_agent.graph import build_graph
from support_agent.models import SupportRequest, SupportResponse

app = FastAPI(title="Support Triage Agent")
support_graph = build_graph()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/support", response_model=SupportResponse)
async def create_support_request(request: SupportRequest) -> SupportResponse:
    result = await support_graph.ainvoke(
        {"user_id": request.user_id, "message": request.message}
    )
    return SupportResponse(
        category=result["category"],
        status=result["status"],
        answer=result["final_answer"],
        ticket_required=result["ticket_required"],
        ticket_id=result.get("ticket_id"),
    )
