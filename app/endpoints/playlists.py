from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cruds import playlists as crud
from app.db.session import SessionLocal
from app.schemas import playlists as schemas
from .songs import get_song


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix = "/playlists",
    tags = ["Playlist"],
)


@router.get("/", response_model = list[schemas.Playlist])
def get_playlists(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db)):
    playlists = crud.get_playlists(db, skip = skip, limit = limit)
    return playlists


@router.get("/{playlist_id}", response_model = schemas.Playlist)
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = crud.get_playlist(db, playlist_id = playlist_id)
    if playlist is None:
        return HTTPException(status_code = 404, detail = "Playlist not found")

    return playlist


@router.post("/{playlist_id}/songs/{song_id}", response_model = schemas.Song)
def add_song_to_playlist(playlist_id: int, song_id: int,
                         db: Session = Depends(get_db)):
    playlist = get_playlist(playlist_id, db)
    song = get_song(song_id, db)

    return crud.add_playlist_song(db, song = song, playlist = playlist)


@router.delete("/{playlist_id}/songs/{song_id}", response_model = schemas.Song)
def remove_song_from_playlist(playlist_id: int, song_id: int,
                              db: Session = Depends(get_db)):
    playlist = get_playlist(playlist_id, db)
    song = get_song(song_id, db)
    if song not in playlist.songs:
        raise HTTPException(status_code = 404, detail = "Song not in playlist")

    return crud.remove_playlist_song(db, song = song, playlist = playlist)


@router.post("/", response_model = schemas.Playlist)
def create_playlist(playlist: schemas.PlaylistCreate,
                    db: Session = Depends(get_db)):
    return crud.create_playlist(db, playlist = playlist)


@router.patch("/{playlist_id}", response_model = schemas.Playlist)
def edit_playlist(playlist_id: int, playlist: schemas.PlaylistUpdate,
                  db: Session = Depends(get_db)):
    db_playlist = get_playlist(playlist_id, db)

    return crud.edit_playlist(db, playlist = db_playlist,
                              updated_playlist = playlist)


@router.delete("/{playlist_id}", response_model = schemas.Playlist)
def remove_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = crud.remove_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code = 404, detail = "Playlist not found")

    return playlist
