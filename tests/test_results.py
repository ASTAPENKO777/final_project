"""Tests for the /result endpoints, including the /result/best ranking."""
import pytest


def _post_result(client, team_id, tournament_id, score):
    return client.post(
        "/result/",
        json={"score": score, "team_id": team_id, "tournament_id": tournament_id},
    )


def test_create_result(client, team, tournament):
    response = _post_result(client, team["id"], tournament["id"], 42)

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 42
    assert body["team_id"] == team["id"]
    assert body["tournament_id"] == tournament["id"]


def test_negative_score_is_rejected(client, team, tournament):
    """Result.score is declared with ge=0."""
    response = _post_result(client, team["id"], tournament["id"], -1)

    assert response.status_code == 422


def test_zero_score_is_allowed(client, team, tournament):
    assert _post_result(client, team["id"], tournament["id"], 0).status_code == 200


def test_score_is_required(client, team, tournament):
    response = client.post(
        "/result/",
        json={"team_id": team["id"], "tournament_id": tournament["id"]},
    )

    assert response.status_code == 422


def test_list_results(client, team, tournament):
    for score in (10, 20, 30):
        _post_result(client, team["id"], tournament["id"], score)

    body = client.get("/result/").json()

    assert sorted(r["score"] for r in body) == [10, 20, 30]


def test_best_returns_the_highest_score(client, team, tournament):
    for score in (10, 99, 55):
        _post_result(client, team["id"], tournament["id"], score)

    response = client.get("/result/best")

    assert response.status_code == 200
    assert response.json()["score"] == 99


def test_best_on_empty_table_returns_404(client):
    response = client.get("/result/best")

    assert response.status_code == 404
    assert response.json()["detail"] == "not found"


@pytest.mark.parametrize("scores", [(1, 2), (2, 1)], ids=["ascending", "descending"])
def test_best_is_independent_of_insertion_order(client, team, tournament, scores):
    for score in scores:
        _post_result(client, team["id"], tournament["id"], score)

    assert client.get("/result/best").json()["score"] == 2
