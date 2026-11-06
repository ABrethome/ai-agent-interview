import pytest

from support_agent.classifiers.keyword import KeywordClassifier


@pytest.fixture
def classifier() -> KeywordClassifier:
    return KeywordClassifier()


@pytest.mark.asyncio
async def test_classifies_access_request(classifier: KeywordClassifier) -> None:
    result = await classifier.classify("I need access to the finance workspace")
    assert result == "access"


@pytest.mark.asyncio
async def test_classifies_permission_request_as_access(
    classifier: KeywordClassifier,
) -> None:
    assert (
        await classifier.classify(
            "Please restore my permission to the finance workspace"
        )
        == "access"
    )


@pytest.mark.asyncio
async def test_classifies_incident(classifier: KeywordClassifier) -> None:
    assert await classifier.classify("The reporting service is down") == "incident"


@pytest.mark.asyncio
async def test_classifies_how_to(classifier: KeywordClassifier) -> None:
    assert await classifier.classify("How do I update my profile?") == "how_to"


@pytest.mark.asyncio
async def test_classifies_unknown_request_as_other(
    classifier: KeywordClassifier,
) -> None:
    assert await classifier.classify("I have a question") == "other"
