import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "state",
    [
        {"message": "How do I update my profile?"},
        {"user_id": "candidate-test"},
        {},
    ],
)
async def test_classification_requires_user_id_and_message(graph, state) -> None:
    with pytest.raises(ValueError, match="Missing required state fields"):
        await graph.ainvoke(state)


@pytest.mark.asyncio
async def test_access_request_requires_review_and_creates_ticket(graph) -> None:
    result = await graph.ainvoke(
        {
            "user_id": "alexandre",
            "message": "Please restore my access to the finance workspace",
        }
    )

    assert result["category"] == "access"
    assert result["ticket_required"] is True
    assert result["ticket_id"]
    assert result["status"] == "needs_human_review"


@pytest.mark.asyncio
async def test_how_to_request_completes_without_ticket(graph) -> None:
    result = await graph.ainvoke(
        {"user_id": "candidate-test", "message": "How do I update my profile?"}
    )

    assert result["category"] == "how_to"
    assert result["ticket_required"] is False
    assert result["status"] == "completed"
