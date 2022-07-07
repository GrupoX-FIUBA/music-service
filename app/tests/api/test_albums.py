from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_get_all_albums(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_albums_without_auth(client: TestClient, db: Session) -> None:
    response = client.get("/albums/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_albums_invalid_api_key(client: TestClient, db: Session) -> None:
    headers = get_invalid_api_key()
    response = client.get("/albums/", headers = headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_albums_by_artist(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/?artist_id=abc123", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_albums_by_subscription(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/?subscription=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_albums_by_subscription_lt(client: TestClient,
                                       db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/?subscription__lt=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_albums_by_subscription_lte(client: TestClient,
                                        db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/?subscription__lte=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_albums_by_subscription_gt(client: TestClient,
                                       db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/?subscription__gt=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_albums_by_subscription_gte(client: TestClient,
                                        db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/?subscription__gte=2", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_inexisting_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/albums/40000", headers = headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    client.post("/genres/", headers = headers, json = {
        "title": "Rock"
    })
    response = client.post("/albums/", headers = headers, json = {
        "title": "Fuerza Natural",
        "genre_id": 1,
        "subscription": 1,
        "artist_id": "abc123"
    })

    json = response.json()
    del json["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert json == {
        "title": "Fuerza Natural",
        "description": None,
        "genre_id": 1,
        "subscription": 1,
        "artist_id": "abc123",
        "blocked": False,
        "songs": []
    }


def test_get_existing_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.post("/albums/", headers = headers, json = {
        "title": "Fuerza Natural",
        "genre_id": 1,
        "subscription": 1,
        "artist_id": "abc123"
    })

    id = response.json()["id"]

    response = client.get("/albums/{}".format(id), headers = headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": id,
        "title": "Fuerza Natural",
        "description": None,
        "genre_id": 1,
        "subscription": 1,
        "artist_id": "abc123",
        "blocked": False,
        "songs": []
    }


def test_edit_existing_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.patch("/albums/1", headers = headers, json = {
        "title": "Otro titulo",
        "description": "Una desc",
        "genre_id": 1,
        "subscription": 0
    })

    json = response.json()
    del json["songs"]

    assert response.status_code == status.HTTP_200_OK
    assert json == {
        "title": "Otro titulo",
        "description": "Una desc",
        "genre_id": 1,
        "subscription": 0,
        "id": 1,
        "artist_id": "abc123",
        "blocked": False
    }


def test_edit_inexisting_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.patch("/albums/40000", headers = headers, json = {
        "title": "Otro titulo",
        "description": "Una desc",
        "genre_id": 1,
        "subscription": 0
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_block_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.patch("/albums/1", headers = headers, json = {
        "blocked": True
    })

    json = response.json()
    del json["songs"]

    assert response.status_code == status.HTTP_200_OK
    assert json == {
        "title": "Otro titulo",
        "description": "Una desc",
        "genre_id": 1,
        "subscription": 0,
        "id": 1,
        "artist_id": "abc123",
        "blocked": True
    }


def test_unblock_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.patch("/albums/1", headers = headers, json = {
        "blocked": False
    })

    json = response.json()
    del json["songs"]

    assert response.status_code == status.HTTP_200_OK
    assert json == {
        "title": "Otro titulo",
        "description": "Una desc",
        "genre_id": 1,
        "subscription": 0,
        "id": 1,
        "artist_id": "abc123",
        "blocked": False
    }


def test_remove_existing_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    last_id = client.get("/albums/", headers = headers).json()[-1]["id"]

    response = client.delete("/albums/{}".format(last_id), headers = headers)

    assert response.status_code == status.HTTP_200_OK


def test_remove_inexisting_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.delete("/albums/40000", headers = headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
