from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_get_all_genres(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/genres/", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_genres_without_auth(client: TestClient, db: Session) -> None:
    response = client.get("/genres/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_genres_invalid_api_key(client: TestClient, db: Session) -> None:
    headers = get_invalid_api_key()
    response = client.get("/genres/", headers = headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_non_existing_genre(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/genres/400", headers = headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
