from support_agent.risk import find_risk_reasons


def test_access_category_requires_review() -> None:
    assert find_risk_reasons("Please restore access", "access") == ["access_request"]


def test_production_outage_requires_review() -> None:
    assert find_risk_reasons("The production service has an outage", "incident") == [
        "production_incident"
    ]


def test_normal_how_to_request_does_not_require_review() -> None:
    assert find_risk_reasons("How do I update my profile?", "how_to") == []
