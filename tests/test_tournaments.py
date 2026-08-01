"""Tests for the /tournaments endpoints."""


def test_create_tournament(client):
    response = client.post(
        "/tournaments/",
        json={
            "title": "Winter Cup",
            "description": "Indoor season",
            "start_date": "2026-01-10T09:00:00",
            "end_date": "2026-01-20T20:00:00",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] > 0
    assert body["title"] == "Winter Cup"


def test_optional_fields_may_be_omitted(client):
    """Only title and start_date are required by the Tournament schema."""
    response = client.post(
        "/tournaments/",
        json={"title": "Minimal Cup", "start_date": "2026-03-01T00:00:00"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Minimal Cup"


def test_start_date_is_required(client):
    assert client.post("/tournaments/", json={"title": "No Date"}).status_code == 422


def test_malformed_start_date_is_rejected(client):
    response = client.post(
        "/tournaments/", json={"title": "Bad Date", "start_date": "yesterday"}
    )

    assert response.status_code == 422


def test_list_tournaments(client):
    client.post(
        "/tournaments/",
        json={"title": "Cup A", "start_date": "2026-01-01T00:00:00"},
    )
    client.post(
        "/tournaments/",
        json={"title": "Cup B", "start_date": "2026-02-01T00:00:00"},
    )

    body = client.get("/tournaments/").json()

    assert {t["title"] for t in body} == {"Cup A", "Cup B"}


def test_list_is_empty_before_anything_is_created(client):
    assert client.get("/tournaments/").json() == []
