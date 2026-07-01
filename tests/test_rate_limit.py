from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_rate_limit():
    """El 6º intento de login en la misma ventana debe devolver 429."""
    payload = {"username": "fake@fake.com", "password": "wrong"}

    for _ in range(5):
        response = client.post("/api/v1/users/login", data=payload)
        assert response.status_code == 401

    response = client.post("/api/v1/users/login", data=payload)
    assert response.status_code == 429
