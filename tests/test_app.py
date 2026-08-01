"""Tests for the application root and the WebSocket chat endpoint."""


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Final project"}


def test_websocket_echoes_the_message(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("hello")

        assert websocket.receive_text() == "Message text was: hello"


def test_websocket_handles_several_messages_on_one_connection(client):
    with client.websocket_connect("/ws") as websocket:
        for message in ("first", "second", "third"):
            websocket.send_text(message)

            assert websocket.receive_text() == f"Message text was: {message}"


def test_openapi_schema_lists_every_router(client):
    paths = client.get("/openapi.json").json()["paths"]

    assert "/users/" in paths
    assert "/team/" in paths
    assert "/tournaments/" in paths
    assert "/result/" in paths


def test_chat_page_renders(client):
    response = client.get("/chat")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_websocket_disconnect_is_handled_cleanly(client):
    """Closing the socket must not raise out of the endpoint."""
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("bye")
        websocket.receive_text()
    # Leaving the context manager closes the socket; no exception may escape.
