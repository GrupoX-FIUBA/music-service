from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_songs(client: TestClient, db: Session) -> None:
    response = client.get("/songs/")
    assert response.status_code == 200
    assert type(response.json()) == list
