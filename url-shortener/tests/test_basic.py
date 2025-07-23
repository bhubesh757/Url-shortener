import pytest
from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_shorten_url_success(client):
    response = client.post("/api/shorten", json={"url": "https://www.google.com"})
    data = response.get_json()
    assert response.status_code == 201
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_url_missing_field(client):
    response = client.post("/api/shorten", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_redirect_success(client):
    # First, shorten a URL
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = res.get_json()["short_code"]

    # Then, follow the redirect
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 302  # HTTP Redirect

def test_redirect_not_found(client):
    response = client.get("/invalid123")
    assert response.status_code == 404



def test_analytics(client):
    # Step 1: Shorten a URL
    res = client.post("/api/shorten", json={"url": "https://google.com"})
    data = res.get_json()
    short_code = data["short_code"]

    print(short_code)

    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    response = client.get(f"/api/stats/{short_code}")
    stats = response.get_json()

    assert response.status_code == 200
    assert stats["url"] == "https://google.com"
    assert stats["clicks"] == 2
    assert "created_at" in stats
