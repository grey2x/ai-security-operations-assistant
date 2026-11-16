
from app import create_app


def test_homepage():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "online"


def test_analyse_samples_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/api/analyse-samples")

    assert response.status_code == 200

    data = response.get_json()

    assert data["total_events"] == 6
    assert data["total_alerts"] == 1
    assert data["alerts"][0]["severity"] == "high"


def test_ai_analysis_without_api_key(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.post(
        "/api/ai-analysis",
        json={"rule_id": "AUTH-001"}
    )

    assert response.status_code == 503
    assert "Gemini API key is not configured" in response.get_json()["error"]


def test_ai_analysis_success(monkeypatch):
    import app.routes

    monkeypatch.setattr(
        app.routes,
        "analyse_alert",
        lambda alert: "Five failed login attempts were detected."
    )

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.post(
        "/api/ai-analysis",
        json={"rule_id": "AUTH-001"}
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "success"
    assert "Five failed login attempts" in response.get_json()["analysis"]
