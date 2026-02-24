def test_get_activities_returns_known_activity(client):
    # Arrange: nothing to set up beyond fixture
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")

    # Verify participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "dupuser@example.com"

    # Act (first signup)
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200

    # Act (duplicate)
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r2.status_code == 400
    assert "already signed up" in r2.json().get("detail", "").lower()


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "NoSuchActivity"
    email = "someone@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    # pick an existing participant
    participants = client.get("/activities").json()[activity]["participants"]
    assert participants, "expected at least one participant"
    participant = participants[0]

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": participant})

    # Assert
    assert resp.status_code == 200
    assert participant in resp.json().get("message", "")

    # Verify removed
    activities = client.get("/activities").json()
    assert participant not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "nope@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "participant not found" in resp.json().get("detail", "").lower()


def test_remove_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "DoesNotExist"
    email = "someone@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "activity not found" in resp.json().get("detail", "").lower()
