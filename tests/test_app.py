from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert delete_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    data = activities_response.json()
    assert email not in data[activity_name]["participants"]
