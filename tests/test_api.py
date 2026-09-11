from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_findings_shape():
    response = client.post(
        "/analyze",
        json={"filename": "snippet.py", "code": "print('hello')"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "snippet.py"
    assert isinstance(body["findings"], list)
