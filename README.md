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

Example request:

```bash
curl -X POST http://127.0.0.1:8000/support \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "candidate-test",
    "message": "Please restore my access to the finance workspace"
  }'
```

## Coding exercise

The support endpoint returns inconsistent guidance for some requests. Investigate the repository, restore a reliable baseline, and improve the implementation where you believe it is justified.

You may use GitHub Copilot or another coding assistant. You remain responsible for understanding and validating every change. Think aloud as you work. You do not need to fix or redesign everything; explain how you prioritize and the trade-offs behind your decisions. Preserve the public API contract and do not have tests call a live model provider.

## Constraints

- Keep behavior deterministic (this is a mock exercise) and tests independent of external services.
- Do not add real access changes, credential operations, or external ticketing calls.

## Definition of done

- You can explain the observed behavior and the evidence behind your diagnosis.
- Changes are proportionate, covered by meaningful tests, and preserve the public API contract.
- `uv run pytest` and `uv run ruff check .` have been run, and you can explain any remaining findings or risks.
- You have reviewed the final diff and can describe what you would prioritize next.
