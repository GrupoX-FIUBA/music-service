from .base import client


def test_get_playlists():
    response = client.get("/playlists/")
    assert response.status_code == 200
    assert type(response.json()) == list
