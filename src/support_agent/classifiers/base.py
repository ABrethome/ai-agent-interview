from typing import Protocol

from support_agent.state import Category


class Classifier(Protocol):
    async def classify(self, message: str) -> Category: ...
