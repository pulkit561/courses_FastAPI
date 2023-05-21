import sys
sys.path.append("../../src")
sys.path.append("../..")
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

def test_get_chapter(test_client):
    response =  test_client.get("/chapters/getchapter/3ba5dd0b2cae4653b58e2adb70a40048", 
                                headers={"Authorization": f"Bearer pulkit"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {
                                "name": "Big Picture of Calculus",
                                "text": "Highlights of Calculus",
                                "rating": 0
                            }

def test_rate_chapter(test_client):
    response = test_client.post("/chapters/ratechapter/1e090ec3129f4e548c9072c026f261a2/rating/1",
                                headers={"Authorization": f"Bearer pulkit"})
    assert response.status_code == 200
    get_chapter_response = test_client.get("/chapters/getchapter/1e090ec3129f4e548c9072c026f261a2",
                                            headers={"Authorization": f"Bearer pulkit"})
    get_chapter_data = get_chapter_response.json()
    assert get_chapter_data["rating"] == 1

