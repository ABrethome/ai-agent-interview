from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from support_agent.classifiers.keyword import KeywordClassifier
from support_agent.knowledge import GUIDANCE
from support_agent.risk import find_risk_reasons
from support_agent.routing import route_by_category, route_by_risk
from support_agent.services.ticketing import InMemoryTicketService
from support_agent.state import Status, SupportState


def build_graph() -> CompiledStateGraph:
    classifier = KeywordClassifier()
    ticket_service = InMemoryTicketService()

    async def classify_request(state: SupportState) -> SupportState:
        missing_fields = [
            field for field in ("user_id", "message") if field not in state
        ]
        if missing_fields:
            raise ValueError(
                f"Missing required state fields: {', '.join(missing_fields)}"
            )

        category = await classifier.classify(state["message"])
        return {"category": category}

    def handle_access(_: SupportState) -> SupportState:
        return {"draft_answer": GUIDANCE["access"]}

    def handle_incident(_: SupportState) -> SupportState:
        return {"draft_answer": GUIDANCE["incident"]}

    def handle_how_to(_: SupportState) -> SupportState:
        return {"draft_answer": GUIDANCE["how_to"]}

    def handle_other(_: SupportState) -> SupportState:
        return {"draft_answer": GUIDANCE["other"]}

    def assess_risk(state: SupportState) -> SupportState:
        reasons = find_risk_reasons(state["message"], state["category"])
        return {
            "risk_reasons": reasons,
            "requires_human_review": bool(reasons),
        }

    async def create_ticket(state: SupportState) -> SupportState:
        ticket_id = await ticket_service.create(
            state["user_id"], 
            state["message"], 
            state["category"],
        )
        return {
            "ticket_required": True,
            "ticket_id": ticket_id,
            "status": "needs_human_review",
        }

    def format_response(state: SupportState) -> SupportState:
        requires_review = state.get("requires_human_review", False)
        answer = state["draft_answer"]
        if requires_review:
            answer = f"{answer} The request has been prepared for human review."

        status: Status = "needs_human_review" if requires_review else "completed"
        return {
            "final_answer": answer,
            "status": status,
            "ticket_required": state.get("ticket_required", False),
        }

    graph = StateGraph(SupportState)
    graph.add_node("classify_request", classify_request)
    graph.add_node("handle_access", handle_access)
    graph.add_node("handle_incident", handle_incident)
    graph.add_node("handle_how_to", handle_how_to)
    graph.add_node("handle_other", handle_other)
    graph.add_node("assess_risk", assess_risk)
    graph.add_node("create_ticket", create_ticket)
    graph.add_node("format_response", format_response)

    graph.add_edge(START, "classify_request")
    graph.add_conditional_edges(
        "classify_request",
        route_by_category,
        {
            "access": "handle_how_to",
            "incident": "handle_incident",
            "how_to": "handle_access",
            "other": "handle_other",
        },
    )
    handlers = ("handle_access", "handle_incident", "handle_how_to", "handle_other")
    for handler in handlers:
        graph.add_edge(handler, "assess_risk")
    graph.add_conditional_edges(
        "assess_risk",
        route_by_risk,
        {"ticket": "create_ticket", "respond": "format_response"},
    )
    graph.add_edge("create_ticket", "format_response")
    graph.add_edge("format_response", END)
    return graph.compile()
