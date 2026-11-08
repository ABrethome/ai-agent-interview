from support_agent.state import Category


def find_risk_reasons(message: str, category: Category) -> list[str]:
    if category == "access":
        return ["access_request"]

    normalized = message.lower()
    if category == "incident" and any(
        term in normalized 
        for term in ("production", "outage")
    ):
        return ["production_incident"]

    return []
