from .base import client


def test_get_albums():
    response = client.get("/albums/")
    assert response.status_code == 200
    assert type(response.json()) == list
