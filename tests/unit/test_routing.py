from support_agent.routing import route_by_category, route_by_risk


def test_access_category_returns_access_route() -> None:
    assert route_by_category({"category": "access"}) == "access"


def test_human_review_routes_to_ticket() -> None:
    assert route_by_risk({"requires_human_review": True}) == "ticket"


def test_no_human_review_routes_to_response() -> None:
    assert route_by_risk({"requires_human_review": False}) == "respond"
