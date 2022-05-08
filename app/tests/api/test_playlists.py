from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_all_playlists(client: TestClient, db: Session) -> None:
    response = client.get("/playlists/")
    assert response.status_code == 200
    assert type(response.json()) == list
