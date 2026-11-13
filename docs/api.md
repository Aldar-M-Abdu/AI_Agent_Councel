# API — AI Decision Council

Base URL (local): `http://localhost:8001`  
Interactive docs: `http://localhost:8001/docs`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Liveness check |
| POST | `/api/register` | Create local user |
| POST | `/api/login` | Login; returns access token |
| POST | `/api/logout` | Invalidate token |
| POST | `/api/chat` | Chat-style agent replies |
| POST | `/api/decision` | Parallel agent answers |
| POST | `/api/debate` | Alias of `/api/decision` |
| POST | `/api/decision-with-discussion` | Discussion + consensus flow |
| POST | `/api/orchestrated-debate` | Same handler as decision-with-discussion |
| POST | `/api/v2/orchestrated-debate` | LangGraph-orchestrated debate |
| POST | `/api/professional-decision` | Longer structured analysis path |
| GET | `/api/agents` | List agent metadata |
| GET | `/api/settings` | Read runtime settings |
| POST | `/api/settings` | Update runtime settings |
| POST | `/api/settings/reset` | Reset settings to defaults |
| GET | `/api/settings/models` | List known model options |
| GET | `/api/history` | User history (Bearer token) |
| POST | `/api/history/save` | Save a decision to history |
| GET | `/api/executive-dashboard/{request_id}` | Dashboard view for a prior request |
| POST | `/api/export-professional-report/{request_id}` | Export HTML/PDF/JSON |
| GET | `/api/download-report/{filename}` | Download a generated report file |

Primary demo endpoint: `POST /api/decision-with-discussion` with JSON body containing `user_text`.
