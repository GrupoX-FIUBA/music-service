from .base import client


def test_get_songs():
    response = client.get("/songs/")
    assert response.status_code == 200
    assert type(response.json()) == list
