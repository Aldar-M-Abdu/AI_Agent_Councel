"""Consensus manager unit tests (no LLM calls)."""

from backend.agents.consensus_manager import (
    AgentVote,
    ProfessionalConsensusManager,
)


def test_calculate_response_confidence_in_unit_interval():
    manager = ProfessionalConsensusManager()
    score = manager.calculate_response_confidence(
        "We strongly recommend a phased rollout with clear metrics and governance."
    )
    assert 0.0 <= score <= 1.0


def test_consensus_aggregates_agent_outputs_with_confidence():
    manager = ProfessionalConsensusManager()

    class _StubAgent:
        def __init__(self, name: str) -> None:
            self.agent_name = name
            self.agent_type = "Advisor"

    agents = [_StubAgent("Neutral Agent"), _StubAgent("Skeptic Agent")]
    agent_responses = [
        {
            "agent_name": "Neutral Agent",
            "text_response": "Proceed with a pilot. Confident this is the right path.",
        },
        {
            "agent_name": "Skeptic Agent",
            "text_response": "Proceed carefully after risk review. Certain mitigations required.",
        },
    ]
    alternatives = ["proceed", "wait", "reject"]

    result = manager.build_professional_consensus(
        question="Should we expand into a new market next year?",
        agents=agents,
        agent_responses=agent_responses,
        discussion_history=[],
        alternatives=alternatives,
    )

    assert result.final_recommendation
    assert 0.0 <= result.consensus_strength <= 1.0
    assert 0.0 <= result.confidence_interval[0] <= 1.0
    assert 0.0 <= result.confidence_interval[1] <= 1.0


def test_weighted_consensus_score_between_0_and_1():
    manager = ProfessionalConsensusManager()
    votes = [
        AgentVote(
            agent_name="A",
            agent_type="Advisor",
            vote="proceed",
            confidence=0.8,
            reasoning="ok",
            weight=1.0,
        ),
        AgentVote(
            agent_name="B",
            agent_type="Advisor",
            vote="proceed",
            confidence=0.6,
            reasoning="ok",
            weight=1.0,
        ),
    ]
    score = manager.calculate_weighted_consensus(votes)
    assert 0.0 <= score <= 1.0
