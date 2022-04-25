from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_albums(client: TestClient, db: Session):
    response = client.get("/albums/")
    assert response.status_code == 200
    assert type(response.json()) == list
