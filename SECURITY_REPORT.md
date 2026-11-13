# Security Report — Phase 1

**Project:** AI Decision Council (`AI_Agent_Councel`)  
**Date:** 2026-11-13  
**Scope:** Repository secret scan, env handling, gitignore hardening

---

## What was checked

1. Full-repo search for sensitive patterns: `sk-`, `api_key`, `OPENROUTER`, `SECRET`, `TOKEN`, `password`, `Bearer`
2. Whether `.env` (or `.env.*`) is tracked or present in git history as a committed file
3. Git history search for committed API key assignments (`OPENROUTER_API_KEY`, Hugging Face-style tokens)
4. Config loading path (`backend/config.py`, `backend/models/direct_hf_manager.py`)
5. Tracked runtime auth/session/history files

---

## What was found

| Finding | Severity | Details |
|---------|----------|---------|
| `.env` not committed | OK | No `.env` in the working tree or in `git ls-files`. No committed `.env` history. |
| Live OpenRouter / HF API keys | OK | No real `sk-…` / `hf_…` keys found in source or history. Matches for `sk-` were false positives (e.g. Swedish/English text containing “risk-”). |
| Weak default `secret_key` | Medium | `backend/config.py` previously hardcoded `secret_key = "change_this_secret"`. Field appears unused by auth today (custom token store), but was still a bad default. |
| Committed password hash | High | `backend/user_accounts.json` contained a real username (`aldar.abdu`) and PBKDF2 password hash. |
| Committed session token | High | `backend/user_sessions.json` contained a live-style access token for that user (expired by date, still sensitive). |
| Committed user history / discussions / reports | Medium | Runtime artifacts with personal decision content were tracked under `backend/user_history.json`, `backend/discussions/`, `backend/reports/`. |
| Auth “Bearer” / password usage in code | Info | Expected application code (JWT-like session header, login form). Not secrets. |
| API key loading | OK | OpenRouter key is read via `os.getenv("OPENROUTER_API_KEY")` (and legacy `HF_TOKEN`) in `direct_hf_manager.py`, and via pydantic-settings in `config.py`. |

---

## What was fixed

1. **`.gitignore`** updated to ensure at least:
   - `venv/`, `.venv/`, `__pycache__/`, `*.pyc`
   - `.env`, `.env.*`, `!.env.example`
   - `*.db`, `*.sqlite3`, `*.log`
   - `node_modules/`, `dist/`, `build/`
   - `.DS_Store`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
   - Plus ignore rules for runtime auth/history/discussions/reports paths
2. **`.env.example`** created with placeholders only (`OPENROUTER_API_KEY`, `DEFAULT_MODEL`, `MAX_TOKENS`, `LOG_LEVEL`, `SECRET_KEY`)
3. **`backend/config.py`** updated so secrets/config come from environment:
   - `OPENROUTER_API_KEY`, `LOG_LEVEL`, `SECRET_KEY`
   - `DEFAULT_MODEL` / `MAX_TOKENS` aliases applied to model settings
   - Removed hardcoded weak `secret_key` default value
   - App display name set to “AI Decision Council API”
4. **Working-tree credential files cleared** to empty JSON `{}`:
   - `backend/user_accounts.json`
   - `backend/user_sessions.json`
   - `backend/user_history.json`

---

## What the maintainer still needs to do manually

1. **Assume the committed password hash and session token are compromised** (they exist in git history even after this working-tree cleanup).
   - Change / retire that account password if reused anywhere else.
   - Do **not** reuse the old session token.
2. On the next commit (Phase 6), untrack runtime files that are now gitignored:
   ```bash
   git rm --cached backend/user_accounts.json backend/user_sessions.json backend/user_history.json
   git rm -r --cached backend/discussions backend/reports
   ```
3. Copy `.env.example` → `.env` and set a real `OPENROUTER_API_KEY` and a strong `SECRET_KEY` locally (never commit `.env`).
4. Optional but recommended: if this repo was ever public with those JSON files, treat history as leaked and consider rotating any related credentials; rewriting git history is a separate, explicit decision (not done in this phase).
5. Confirm whether discussions/reports should remain as local-only demo artifacts or be replaced later with sanitized fixtures for documentation.

---

## Config loading confirmation

- `backend/config.py` — `pydantic_settings.BaseSettings` with `env_file=".env"`
- `backend/models/direct_hf_manager.py` — `os.getenv("OPENROUTER_API_KEY")` / `os.getenv("HF_TOKEN")`
- No hardcoded API keys found in application code
