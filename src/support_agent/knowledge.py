from support_agent.state import Category

GUIDANCE: dict[Category, str] = {
    "access": "Access changes require an authorization review.",
    "incident": "Check the service status and capture the error details.",
    "how_to": "Follow the standard troubleshooting procedure.",
    "other": "Please provide the affected system and observed error.",
}
