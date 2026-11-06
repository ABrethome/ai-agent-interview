from support_agent.state import SupportState


def route_by_category(state: SupportState) -> str:
    return state.get("category", "other")


def route_by_risk(state: SupportState) -> str:
    if state.get("requires_human_review", False):
        return "ticket"
    return "respond"
