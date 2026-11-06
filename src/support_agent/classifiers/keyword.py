from support_agent.state import Category


class KeywordClassifier:
    async def classify(self, message: str) -> Category:
        normalized = message.lower()

        if "access" in normalized or "role" in normalized:
            return "access"
        if any(term in normalized for term in ("down", "outage", "unavailable")):
            return "incident"
        if any(
            term in normalized
            for term in ("how do i", "instructions", "guide")
        ):
            return "how_to"
        return "other"
