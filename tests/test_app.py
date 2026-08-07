from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert "description" in data[expected_activity]
    assert "participants" in data[expected_activity]


def test_signup_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "new_student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    data = activities_response.json()
    assert email in data[activity_name]["participants"]


def test_duplicate_signup_returns_error():
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate_student@example.com"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student_to_remove@example.com"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    delete_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    data = activities_response.json()
    assert email not in data[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_error():
    # Arrange
    activity_name = "Gym Class"
    email = "not_signed_up@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
