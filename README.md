# AI Decision Council

Multi-agent decision-support API: specialist AI agents debate a question and return a structured recommendation.

## Overview

AI Decision Council is a portfolio project that simulates a small advisory board for complex decisions. A FastAPI backend runs four agents with different roles (neutral, optimistic, skeptical, risk-focused), optionally orchestrated with LangGraph, and calls LLMs through OpenRouter. A React UI supports interactive use. This repo demonstrates backend/AI engineering skills—it is not a certified enterprise product.

**Repository:** https://github.com/Aldar-M-Abdu/AI_Agent_Councel

## Demo

- Swagger UI: http://localhost:8001/docs (after starting the backend)
- Screenshot: `docs/swagger.png` *(add a real capture)*
- Short GIF: `docs/demo.gif` *(add a real recording)*

See `docs/DEMO_ASSETS.md` for how to add these files.

## Architecture

```
Client (React / curl / Swagger)
        │
        ▼
   FastAPI (backend/main_api.py)
        │
        ▼
   Orchestrator (LangGraph optional path)
        │
        ├── Neutral Agent
        ├── Positive Agent
        ├── Skeptic Agent
        └── Risk Expert Agent
        │
        ▼
   Consensus / discussion aggregation
        │
        ▼
   Reporter / response models → JSON (+ optional HTML/PDF export)

LLM provider: OpenRouter (backend/models/direct_hf_manager.py)
```

## Implemented features

- FastAPI backend: health, auth (register/login/logout), decision and settings endpoints
- Four specialist agents with OpenRouter-backed generation (text fallback if no API key)
- Multi-round flow: answers → peer discussion → consensus (`POST /api/decision-with-discussion`)
- LangGraph orchestration module and `POST /api/v2/orchestrated-debate`
- Consensus, decision-framework, and executive-report helpers under `backend/agents/`
- Local demo auth/history via JSON files (not a production store)
- React frontend (MUI): decision UI, auth, history, settings, export modal
- Config from environment via `.env` / pydantic-settings (see `.env.example`)
- Pytest suite with mocked OpenRouter client (`pytest -q`)
- Docker image + `docker compose` for the backend

## Planned / Roadmap (not implemented)

- Production database instead of JSON / in-memory stores
- Re-enabled web search (disabled; former Tavily path removed)
- Stronger session security (signed JWTs, production rate limiting)
- Demo screenshot/GIF assets (`docs/swagger.png`, `docs/demo.gif`)

## Tech stack

Python, FastAPI, Uvicorn, Pydantic · LangGraph / LangChain core · OpenRouter · React 18, MUI, Axios · python-dotenv · pytest listed (suite TBD)

## Quickstart

```bash
git clone https://github.com/Aldar-M-Abdu/AI_Agent_Councel.git
cd AI_Agent_Councel

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # set OPENROUTER_API_KEY

uvicorn backend.main_api:app --reload --host 0.0.0.0 --port 8001
```

Frontend (optional, local only): `cd frontend && npm install && npm start`

- API http://localhost:8001 · Docs http://localhost:8001/docs · UI http://localhost:3000  

### Docker (backend)

```bash
cp .env.example .env   # set OPENROUTER_API_KEY
docker compose up --build
```

- API: http://localhost:8001  
- Health: http://localhost:8001/api/health  
- Frontend is **not** included in Compose yet (CRA `public/` assets are missing, so it does not start with a simple one-command setup).

## API reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Liveness check |
| POST | `/api/register` / `/api/login` / `/api/logout` | Local auth |
| POST | `/api/chat` | Chat-style agent replies |
| POST | `/api/decision` | Parallel agent answers |
| POST | `/api/decision-with-discussion` | Discussion + consensus flow |
| POST | `/api/v2/orchestrated-debate` | LangGraph-orchestrated debate |
| POST | `/api/professional-decision` | Longer structured analysis path |
| GET | `/api/agents` | Agent metadata |
| GET/POST | `/api/settings` | Runtime settings |
| GET | `/api/history` | User history (auth) |

### Example: `POST /api/decision-with-discussion`

```json
{ "user_text": "Should we expand into a new market next year?" }
```

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "Should we expand into a new market next year?",
  "initial_responses": [
    { "agent_name": "Neutral Agent", "agent_type": "Neutral Advisor", "text_response": "..." }
  ],
  "discussions": [{ "agent_name": "Neutral Agent", "discussion": "..." }],
  "consensus_contributions": [
    { "agent_name": "Neutral Agent", "consensus_contribution": "..." }
  ],
  "final_recommendation": "Final recommendation based on discussion.",
  "discussion_file": "discussions/discussion_YYYYMMDD_HHMMSS.txt"
}
```

## Project structure

```
AI_Agent_Councel/
├── backend/
│   ├── agents/           # Agents, consensus, reporting helpers
│   ├── orchestration/    # LangGraph orchestrator
│   ├── evaluation/       # Meta-evaluation helpers
│   ├── models/           # OpenRouter client
│   ├── technical_depth/  # Benchmark / search stubs
│   ├── main_api.py
│   └── config.py
├── frontend/src/         # React app + components
├── docs/                 # architecture.md, api.md, demo placeholders
├── tests/                # Pytest suite (mocked LLM)
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── SECURITY_REPORT.md
└── README.md
```


## Testing

```bash
pip install -r requirements-dev.txt
pytest -q
```

Coverage includes health check, agent instantiation with a mocked OpenRouter client, consensus scoring (0–1), and `POST /api/decision-with-discussion`. Tests do **not** require a real `OPENROUTER_API_KEY`.

## What I learned

- Multi-agent pipelines (roles, discussion, consensus aggregation)
- FastAPI lifespan, dependencies, and typed response models
- Thin OpenRouter client with graceful fallback when no API key is set
- Separating implemented features from aspirational roadmap claims
- Keeping secrets out of git (`.env`, `.gitignore`, `.env.example`)

## License

MIT — see [LICENSE](LICENSE) (Copyright © 2025 Aldar Abdu).
