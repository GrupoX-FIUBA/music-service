from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_songs():
    response = client.get("/songs/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_albums():
    response = client.get("/albums/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_playlists():
    response = client.get("/playlists/")
    assert response.status_code == 200
    assert type(response.json()) == list
