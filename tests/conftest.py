"""
Shared pytest fixtures for AI Decision Council.

All tests use a mocked OpenRouter / DirectHFManager so no real API key is required.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
for path in (ROOT, BACKEND):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


MOCK_RESPONSE = (
    "Mocked analysis: recommend a phased approach with clear success metrics, "
    "stakeholder alignment, and risk controls. This response is long enough "
    "to pass quality checks used by the agent layer."
)


class MockOpenRouterManager:
    """Stand-in for DirectHFManager that never performs HTTP calls."""

    def __init__(self, *args, **kwargs) -> None:
        self._api_available = True
        self.api_token = "mock-token"

    def is_available(self) -> bool:
        return True

    def generate_response(self, prompt: str, **kwargs) -> str:
        return MOCK_RESPONSE

    def get_model_info(self) -> dict:
        return {
            "model_type": "openrouter",
            "model_name": "mock/model",
            "authenticated": True,
            "provider": "MockOpenRouter",
        }

    def query(self, payload):
        return [{"generated_text": MOCK_RESPONSE}]

    def set_token(self, token: str) -> None:
        self.api_token = token


@pytest.fixture
def mock_openrouter(monkeypatch: pytest.MonkeyPatch) -> MockOpenRouterManager:
    """Monkeypatch OpenRouter client so agents never call the real API."""
    mock = MockOpenRouterManager()

    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    # Patch both package paths used across the codebase
    monkeypatch.setattr(
        "backend.models.direct_hf_manager.DirectHFManager",
        lambda *a, **k: mock,
    )
    monkeypatch.setattr(
        "models.direct_hf_manager.DirectHFManager",
        lambda *a, **k: mock,
        raising=False,
    )

    import backend.agents.base_agent as base_agent_mod

    monkeypatch.setattr(base_agent_mod, "_global_model_manager", mock)
    monkeypatch.setattr(base_agent_mod, "MODEL_MANAGER_AVAILABLE", True)
    monkeypatch.setattr(base_agent_mod, "DirectHFManager", lambda *a, **k: mock, raising=False)

    return mock


@pytest.fixture
def client(mock_openrouter: MockOpenRouterManager, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    """FastAPI TestClient with mocked LLM and reset agent pool."""
    import backend.main_api as main_api

    monkeypatch.setattr(main_api, "_global_agents", None)

    with TestClient(main_api.app) as test_client:
        yield test_client

    # Reset after test so later suites do not reuse mocked agents unexpectedly
    main_api._global_agents = None
