from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import albums as crud
from app.models import albums as models
from app.schemas import albums as schemas
from app.schemas.songs import Song
from .base import get_db, response_codes
from .songs import get_song


router = APIRouter(
    prefix = "/albums",
    tags = ["Albums"],
)


@router.get("/", response_model = list[schemas.Album])
def get_albums(skip: int = 0, limit: int = 100,
               artist_id: str = None, subscription: int = None,
               subscription__lt: int = None, subscription__lte: int = None,
               subscription__gt: int = None, subscription__gte: int = None,
               db: Session = Depends(get_db)):
    filters = []
    if artist_id:
        filters += [lambda: models.Album.artist_id == artist_id]
    if subscription:
        filters += [lambda: models.Album.subscription == subscription]
    if subscription__lt:
        filters += [lambda: models.Album.subscription < subscription__lt]
    if subscription__lte:
        filters += [lambda: models.Album.subscription <= subscription__lte]
    if subscription__gt:
        filters += [lambda: models.Album.subscription > subscription__gt]
    if subscription__gte:
        filters += [lambda: models.Album.subscription >= subscription__gte]

    albums = crud.get_albums(db, skip = skip, limit = limit,
                             filters = filters)
    return albums


@router.get("/{album_id}", response_model = schemas.Album,
            responses = {404: response_codes[404]})
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id = album_id)
    if album is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Album not found")

    return album


@router.post("/{album_id}/songs/{song_id}", response_model = Song,
             responses = {404: response_codes[404], 409: response_codes[409]})
def add_song_to_album(album_id: int, song_id: int,
                      db: Session = Depends(get_db)):
    album = get_album(album_id, db)
    song = get_song(song_id, db)

    if song in album.songs:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail = "The album already has that song")

    return crud.add_album_song(db, song = song, album = album)


@router.delete("/{album_id}/songs/{song_id}", response_model = Song,
               responses = {404: response_codes[404],
                            409: response_codes[409]})
def remove_song_from_album(album_id: int, song_id: int,
                           db: Session = Depends(get_db)):
    album = get_album(album_id, db)
    song = get_song(song_id, db)

    if song.album_id != album_id:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail = "The song is not in the album")

    return crud.remove_album_song(db, album = album, song = song)


@router.post("/", response_model = schemas.Album, status_code = 201)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    return crud.create_album(db, album = album)


@router.patch("/{album_id}", response_model = schemas.Album,
              responses = {404: response_codes[404]})
def edit_album(album_id: int, album: schemas.AlbumUpdate,
               db: Session = Depends(get_db)):
    db_album = get_album(album_id, db)

    return crud.edit_album(db, album = db_album, updated_album = album)


@router.delete("/{album_id}", response_model = schemas.Album,
               responses = {404: response_codes[404]})
def remove_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.remove_album(db, album_id)
    if album is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Album not found")

    return album
