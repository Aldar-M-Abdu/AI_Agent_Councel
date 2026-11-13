"""Health endpoint smoke tests."""


def test_health_returns_200_and_status(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert "message" in payload
    assert "AI Decision Council" in payload["message"]
