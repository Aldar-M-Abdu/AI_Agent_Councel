"""Decision-with-discussion endpoint tests (mocked LLM only)."""


def test_decision_with_discussion_returns_expected_schema(client, mock_openrouter):
    response = client.post(
        "/api/decision-with-discussion",
        json={"user_text": "Should we expand into a new market next year?"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert "request_id" in payload
    assert payload["request_id"]

    # recommendation / analysis field
    assert "final_recommendation" in payload
    assert isinstance(payload["final_recommendation"], str)
    assert len(payload["final_recommendation"].strip()) > 0

    assert "confidence_score" in payload
    assert 0.0 <= float(payload["confidence_score"]) <= 1.0

    assert payload.get("question")
    assert isinstance(payload.get("initial_responses"), list)
    assert len(payload["initial_responses"]) >= 1
