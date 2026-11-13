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
