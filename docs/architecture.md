# Architecture — AI Decision Council

## High-level flow

```
Client (React / curl / Swagger)
        |
        v
FastAPI  (backend/main_api.py)
        |
        +--> Auth helpers (JSON file store under backend/)
        |
        v
Agent pool (Neutral / Positive / Skeptic / Risk Expert)
        |
        +--> Optional LangGraph orchestrator (backend/orchestration/)
        |
        v
Consensus helpers (backend/agents/consensus_manager.py)
        |
        v
Response models (+ optional HTML/PDF report export)

LLM calls go through DirectHFManager -> OpenRouter HTTP API.
If no OPENROUTER_API_KEY is set, agents use local fallback text.
```

## Main packages

| Path | Role |
|------|------|
| `backend/main_api.py` | HTTP API, lifespan, auth, decision routes |
| `backend/config.py` | Settings from environment / `.env` |
| `backend/agents/` | Agent personas, consensus, reporting helpers |
| `backend/orchestration/` | LangGraph workflow |
| `backend/models/` | OpenRouter client |
| `backend/evaluation/` | Response quality helpers |
| `backend/technical_depth/` | Benchmarking; web search currently disabled |
| `frontend/src/` | React UI (local; not in Docker Compose yet) |

## Config

All runtime secrets and tunables load from environment variables via pydantic-settings.
See `.env.example`.
