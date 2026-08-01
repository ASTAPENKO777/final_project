"""Tests for the /users endpoints."""
import pytest


def test_create_user_returns_persisted_record(client):
    response = client.post(
        "/users/",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == "Alice"
    assert body["email"] == "alice@example.com"


def test_password_is_never_returned(client):
    """The read schema must not leak the password back to the client."""
    response = client.post(
        "/users/",
        json={"name": "Bob", "email": "bob@example.com", "password": "hunter2"},
    )

    assert "password" not in response.json()


def test_list_users_is_empty_before_anything_is_created(client):
    assert client.get("/users/").json() == []


def test_list_users_returns_every_created_user(client):
    for name in ("Alice", "Bob", "Carol"):
        client.post(
            "/users/",
            json={
                "name": name,
                "email": f"{name.lower()}@example.com",
                "password": "secret",
            },
        )

    body = client.get("/users/").json()

    assert len(body) == 3
    assert {user["name"] for user in body} == {"Alice", "Bob", "Carol"}


def test_get_single_user_by_id(client):
    created = client.post(
        "/users/",
        json={"name": "Dave", "email": "dave@example.com", "password": "secret"},
    ).json()

    response = client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_unknown_user_returns_404(client):
    response = client.get("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_user_can_be_assigned_to_a_team(client, team):
    response = client.post(
        "/users/",
        json={
            "name": "Eve",
            "email": "eve@example.com",
            "password": "secret",
            "team_id": team["id"],
        },
    )

    assert response.status_code == 200
    assert response.json()["team_id"] == team["id"]


@pytest.mark.parametrize(
    "password",
    ["abc", "a" * 17],
    ids=["too-short", "too-long"],
)
def test_password_length_is_validated(client, password):
    """UserCreate declares min_length=4, max_length=16."""
    response = client.post(
        "/users/",
        json={"name": "Mallory", "email": "m@example.com", "password": password},
    )

    assert response.status_code == 422


def test_malformed_email_is_rejected(client):
    response = client.post(
        "/users/",
        json={"name": "Trent", "email": "not-an-email", "password": "secret"},
    )

    assert response.status_code == 422


def test_name_is_required(client):
    response = client.post(
        "/users/", json={"email": "nobody@example.com", "password": "secret"}
    )

    assert response.status_code == 422
