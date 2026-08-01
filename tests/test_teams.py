"""Tests for the /team endpoints."""


def test_create_team(client):
    response = client.post("/team/", json={"name": "Falcons"})

    assert response.status_code == 200
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == "Falcons"
    assert body["members"] == []


def test_team_name_is_required(client):
    assert client.post("/team/", json={}).status_code == 422


def test_list_teams(client):
    client.post("/team/", json={"name": "Falcons"})
    client.post("/team/", json={"name": "Eagles"})

    body = client.get("/team/").json()

    assert {t["name"] for t in body} == {"Falcons", "Eagles"}


def test_get_single_team(client, team):
    response = client.get(f"/team/{team['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == team["name"]


def test_get_unknown_team_returns_404(client):
    response = client.get("/team/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_team_exposes_its_members(client, team):
    """Team.members is the reverse side of User.team — it must be populated."""
    for name in ("Alice", "Bob"):
        client.post(
            "/users/",
            json={
                "name": name,
                "email": f"{name.lower()}@example.com",
                "password": "secret",
                "team_id": team["id"],
            },
        )

    body = client.get(f"/team/{team['id']}").json()

    assert {member["name"] for member in body["members"]} == {"Alice", "Bob"}
    assert all(member["team_id"] == team["id"] for member in body["members"])
