def test_health_endpoint_returns_ok(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_support_endpoint_rejects_short_message(client) -> None:
    response = client.post(
        "/support", json={"user_id": "candidate-test", "message": "no"}
    )

    assert response.status_code == 422


def test_support_endpoint_returns_public_response(client) -> None:
    response = client.post(
        "/support",
        json={
            "user_id": "candidate-test",
            "message": "Please restore my access to the finance workspace",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert {
        "category",
        "status",
        "answer",
        "ticket_required",
        "ticket_id",
    } == body.keys()
    assert not {
        "draft_answer",
        "risk_reasons",
        "requires_human_review",
        "final_answer",
    }.intersection(body)
