from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cruds import songs as crud
from app.db.session import SessionLocal
from app.schemas import songs as schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix = "/songs",
    tags = ["Song"],
)


@router.get("/", response_model = list[schemas.Song])
def get_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_songs(db, skip = skip, limit = limit)
    return songs


@router.get("/{song_id}", response_model = schemas.Song)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db, song_id = song_id)
    if song is None:
        raise HTTPException(status_code = 404, detail = "Song not found")

    return song


@router.post("/", response_model = schemas.Song)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    return crud.create_song(db, song = song)


@router.patch("/{song_id}", response_model = schemas.Song)
def edit_song(song_id: int, song: schemas.SongUpdate,
              db: Session = Depends(get_db)):
    db_song = get_song(song_id, db)

    return crud.edit_song(db, song = db_song, updated_song = song)


@router.delete("/{song_id}", response_model = schemas.Song)
def remove_song(song_id, db: Session = Depends(get_db)):
    song = crud.remove_song(db, song_id)
    if song is None:
        raise HTTPException(status_code = 404, detail = "Song not found")

    return song
