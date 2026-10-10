

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "secure-multimodal-rag",
    }


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Secure Multimodal RAG API"
    assert data["docs"] == "/docs"
def test_search_requires_api_key():
    response = client.get("/search", params={"query": "employee onboarding"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing API key"
def test_search_with_valid_hr_key_returns_results():
    response = client.get(
        "/search",
        params={"query": "employee onboarding"},
        headers={"X-API-Key": "dev-hr-key"},
    )

    assert response.status_code == 200
    assert "results" in response.json()
def test_finance_search_only_returns_finance_results():
    response = client.get(
        "/search",
        params={"query": "employee onboarding"},
        headers={"X-API-Key": "dev-finance-key"},
    )

    assert response.status_code == 200
    for result in response.json()["results"]:
        assert result["department"] == "finance"