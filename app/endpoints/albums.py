from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cruds import albums as crud
from app.schemas import albums as schemas
from app.schemas.songs import Song
from .base import get_db
from .songs import get_song


router = APIRouter(
    prefix = "/albums",
    tags = ["Albums"],
)


@router.get("/", response_model = list[schemas.Album])
def get_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = crud.get_albums(db, skip = skip, limit = limit)
    return albums


@router.get("/{album_id}", response_model = schemas.Album)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id = album_id)
    if album is None:
        raise HTTPException(status_code = 404, detail = "Album not found")

    return album


@router.post("/{album_id}/songs/{song_id}", response_model = Song)
def add_song_to_album(album_id: int, song_id: int,
                      db: Session = Depends(get_db)):
    album = get_album(album_id, db)
    song = get_song(song_id, db)

    return crud.add_album_song(db, song = song, album = album)


@router.delete("/{album_id}/songs/{song_id}", response_model = Song)
def remove_song_from_album(album_id: int, song_id: int,
                           db: Session = Depends(get_db)):
    album = get_album(album_id, db)
    song = get_song(song_id, db)

    if song.album_id != album_id:
        raise HTTPException(status_code = 404, detail = "Song not in album")

    return crud.remove_album_song(db, album = album, song = song)


@router.post("/", response_model = schemas.Album, status_code = 201)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    return crud.create_album(db, album = album)


@router.patch("/{album_id}", response_model = schemas.Album)
def edit_album(album_id: int, album: schemas.AlbumUpdate,
               db: Session = Depends(get_db)):
    db_album = get_album(album_id, db)

    return crud.edit_album(db, album = db_album, updated_album = album)


@router.delete("/{album_id}", response_model = schemas.Album)
def remove_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.remove_album(db, album_id)
    if album is None:
        raise HTTPException(status_code = 404, detail = "Album not found")

    return album
