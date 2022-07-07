from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_get_all_songs(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_songs_without_auth(client: TestClient, db: Session) -> None:
    response = client.get("/songs/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_songs_invalid_api_key(client: TestClient, db: Session) -> None:
    headers = get_invalid_api_key()
    response = client.get("/songs/", headers = headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_songs_by_artist(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/?artist_id=abc123", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_songs_by_subscription(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/?subscription=1", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_songs_by_subscription_lt(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/?subscription__lt=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_songs_by_subscription_lte(client: TestClient,
                                       db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/?subscription__lte=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_songs_by_subscription_gt(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/?subscription__gt=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_songs_by_subscription_gte(client: TestClient,
                                       db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/?subscription__gte=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_non_existing_song(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/songs/400", headers = headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
