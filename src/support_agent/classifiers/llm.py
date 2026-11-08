from typing import Protocol

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from support_agent.state import Category


class AsyncChatModel(Protocol):
    async def ainvoke(self, input: list[BaseMessage]) -> BaseMessage: ...


class LlmClassifier:
    def __init__(self, model: AsyncChatModel) -> None:
        self._model = model

    async def classify(self, message: str) -> Category:
        response = await self._model.ainvoke(
            [
                SystemMessage(
                    content=(
                        "Classify the support request as access, incident, "
                        "how_to, or other. Return only the category."
                    )
                ),
                HumanMessage(content=message),
            ]
        )
        content = response.content
        if not isinstance(content, str):
            raise ValueError("Classifier response must contain a text category")

        category = content.strip().lower()
        if category not in ("access", "incident", "how_to", "other"):
            raise ValueError(f"Invalid classifier category: {content!r}")
        return category  # type: ignore[return-value]
