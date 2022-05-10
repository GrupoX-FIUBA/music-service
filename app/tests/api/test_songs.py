from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_get_all_songs(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/", headers = headers)
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_songs_without_auth(client: TestClient, db: Session) -> None:
    response = client.get("/songs/")
    assert response.status_code == 301


def test_get_songs_invalid_api_key(client: TestClient, db: Session) -> None:
    headers = get_invalid_api_key()
    response = client.get("/songs/", headers = headers)
    assert response.status_code == 301
