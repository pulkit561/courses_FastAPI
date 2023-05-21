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

def test_get_course_overview(test_client):
    response =  test_client.get("/courses/getcourseoverview/1559ac7989494f9a871d9d6a917cf19f",
                                headers={"Authorization": f"Bearer pulkit"})
    assert response.status_code == 200
    assert response.json() == "Course lectures for MIT Introduction to Deep Learning."

def test_get_all_courses(test_client):
    response = test_client.get("/courses/getallcourses/sort/alphabetical?domain=artificial%20intelligence",
                                headers={"Authorization": f"Bearer pulkit"})
    response_data = response.json()
    assert response_data[0]["name"] == "Computer Vision Course"
    assert response_data[1]["name"] == "Introduction to Deep Learning"

