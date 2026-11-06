from typing import Protocol

from support_agent.state import Category


class TicketService(Protocol):
    async def create(self, user_id: str, message: str, category: Category) -> str: ...


class InMemoryTicketService:
    async def create(self, user_id: str, message: str, category: Category) -> str:
        return "TICKET-0001"
