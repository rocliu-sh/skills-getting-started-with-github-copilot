from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# AAA: Arrange-Act-Assert pattern

def test_get_activities():
    # Arrange: No setup needed, activities are pre-populated in app
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Basketball Team"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result.get("message", "")
    # Confirm participant is added
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email in participants


def test_remove_participant():
    # Arrange
    email = "removeme@mergington.edu"
    activity = "Basketball Team"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result.get("message", "")
    # Confirm participant is removed
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email not in participants
