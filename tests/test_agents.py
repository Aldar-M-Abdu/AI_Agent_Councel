"""Agent instantiation and mocked response tests."""

import pytest

from backend.agents.neutral_agent import NeutralAgent
from backend.agents.positive_agent import PositiveAgent
from backend.agents.risk_expert_agent import RiskExpertAgent
from backend.agents.skeptic_agent import SkepticAgent

AGENT_CLASSES = [NeutralAgent, PositiveAgent, SkepticAgent, RiskExpertAgent]


@pytest.mark.parametrize("agent_cls", AGENT_CLASSES)
def test_agent_can_be_instantiated(agent_cls, mock_openrouter):
    agent = agent_cls()
    assert agent.agent_name
    assert agent.model_manager is mock_openrouter or agent.model_manager is not None


@pytest.mark.parametrize("agent_cls", AGENT_CLASSES)
def test_agent_returns_non_empty_response(agent_cls, mock_openrouter):
    agent = agent_cls()
    agent.model_manager = mock_openrouter
    result = agent.generate_response("Should we expand into a new market?")
    assert isinstance(result, str)
    assert len(result.strip()) > 0
