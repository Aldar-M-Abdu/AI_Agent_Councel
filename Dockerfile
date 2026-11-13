# AI Decision Council — backend image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app:/app/backend

WORKDIR /app

# Minimal system deps (curl for healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Non-root user and writable runtime dirs
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/backend/discussions /app/backend/reports \
    && chown -R appuser:appuser /app

COPY --chown=appuser:appuser backend ./backend

USER appuser

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://127.0.0.1:8001/api/health || exit 1

CMD ["uvicorn", "backend.main_api:app", "--host", "0.0.0.0", "--port", "8001"]
