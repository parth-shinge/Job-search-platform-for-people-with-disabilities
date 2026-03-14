from api.app import app


def test_api_health_check_returns_200_and_status():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "healthy"
