from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import songs as crud
from app.cruds.albums import album_exists
from app.cruds.genres import genre_exists
from app.models import songs as models
from app.schemas import songs as schemas
from .base import get_db, response_codes


router = APIRouter(
    prefix = "/songs",
    tags = ["Song"],
)


@router.get("/", response_model = list[schemas.Song])
def get_songs(skip: int = 0, limit: int = 100,
              artist_id: str = None, subscription: int = None,
              subscription__lt: int = None, subscription__lte: int = None,
              subscription__gt: int = None, subscription__gte: int = None,
              db: Session = Depends(get_db)):
    filters = []
    if artist_id:
        filters += [lambda: models.Song.artist_id == artist_id]
    if subscription:
        filters += [lambda: models.Song.subscription == subscription]
    if subscription__lt:
        filters += [lambda: models.Song.subscription < subscription__lt]
    if subscription__lte:
        filters += [lambda: models.Song.subscription <= subscription__lte]
    if subscription__gt:
        filters += [lambda: models.Song.subscription > subscription__gt]
    if subscription__gte:
        filters += [lambda: models.Song.subscription >= subscription__gte]

    songs = crud.get_songs(db, skip = skip, limit = limit, filters = filters)
    return songs


@router.get("/{song_id}", response_model = schemas.Song,
            responses = {404: response_codes[404]})
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db, song_id = song_id)
    if song is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Song not found")

    return song


@router.post("/", response_model = schemas.Song, status_code = 201)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    if not album_exists(db, song.album_id):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Album doesn't exists")

    if not genre_exists(db, song.genre_id):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Genre doesn't exists")

    return crud.create_song(db, song = song)


@router.patch("/{song_id}", response_model = schemas.Song,
              responses = {404: response_codes[404]})
def edit_song(song_id: int, song: schemas.SongUpdate,
              db: Session = Depends(get_db)):
    if song.album_id and not album_exists(db, song.album_id):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Album doesn't exists")

    if song.genre_id and not genre_exists(db, song.genre_id):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Genre doesn't exists")

    db_song = get_song(song_id, db)

    return crud.edit_song(db, song = db_song, updated_song = song)


@router.delete("/{song_id}", response_model = schemas.Song,
               responses = {404: response_codes[404]})
def remove_song(song_id, db: Session = Depends(get_db)):
    song = crud.remove_song(db, song_id)
    if song is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Song not found")

    return song
