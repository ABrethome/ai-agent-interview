# Support Triage Agent

## Business context

This repository contains a small internal IT support triage agent. It classifies incoming support requests, drafts guidance, assesses whether human review is appropriate, and can prepare a simulated support ticket.

The application is a local exercise, which mocks an agent. No external API made.

## Functional behavior

The `POST /support` endpoint accepts a user ID and a message. The agent classifies the request as `access`, `incident`, `how_to`, or `other`, prepares category-specific guidance, and returns a public response. Requests requiring review receive a deterministic simulated ticket ID.

## Setup

```bash
uv sync
```

## Visualize the graph with LangGraph Studio

From the repository root:

```bash
LANGGRAPH_CLI_NO_ANALYTICS=1 uv run langgraph dev --no-browser
```

Open [LangGraph Studio](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)
and select `support_triage` to view the nodes and conditional edges. Studio may
require signing in to LangSmith. The graph runs locally, without a model API key;
the [CLI configuration](./langgraph.json) disables LangSmith tracing.

To step through a run, supply this graph input in Studio:

```json
{
  "user_id": "studio-test",
  "message": "How do I connect to the office Wi-Fi?"
}
```

The CLI serves a separate development API at `http://127.0.0.1:2024`
and reloads graph changes automatically; it does not replace the FastAPI
`/support` endpoint. Stop it with `Ctrl+C`.


## Tests and lint

```bash
uv run pytest
uv run ruff check .
```

## Run the application

```bash
uv run uvicorn support_agent.api:app --reload
```

The service is available at `http://127.0.0.1:8000`. 

Docs: http://127.0.0.1:8000/docs

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Support request:

```bash
curl -X POST http://127.0.0.1:8000/support \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "candidate-test",
    "message": "Please restore my access to the finance workspace"
  }'
```

## Initial coding exercise

User has reported that the support endpoint returns inconsistent guidance for some requests from the Support Triage Agent in Production. Understand then investigate the repository to debug.

You may use GitHub Copilot or another coding assistant. You remain responsible for understanding and validating every change. Think aloud as you work. You do not need to fix or redesign everything; explain how you prioritize and the trade-offs behind your decisions. Preserve the public API contract and do not have tests call a live model provider.

User-reported issue with the following request via Service Desk:
User: "Please restore my permission to the finance workspace".
Obtained: 
```
{
  "category": "other",
  "status": "completed",
  "answer": "Please provide the affected system and observed error.",
  "ticket_required": false,
  "ticket_id": null
}
```
User-expected category `access`.

## Initial definition of done

- You can reproduce and explain the observed issue.
- You find evidences behind your diagnosis.
- You propose changes that are proportionate.
- You propose means to avoid the observed issue in the future
