from support_agent.state import Category


class KeywordClassifier:
    async def classify(self, message: str) -> Category:
        normalized = message.lower()

        # check if the message contains keywords for each category
        # e.g.: access, role and permission keywords should be routed to "access"
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
