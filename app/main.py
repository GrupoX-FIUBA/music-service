from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind = engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/songs/", response_model = list[schemas.Song])
def get_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_songs(db, skip = skip, limit = limit)
    return songs


@app.get("/songs/{song_id}", response_model = schemas.Song)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db, song_id = song_id)
    if song is None:
        raise HTTPException(status_code = 404, detail = "Song not found")

    return song


@app.post("/songs/", response_model = schemas.Song)
def create_song(song: schemas.SongCreate,
                artist_id: int,
                album_id: Optional[int] = None,
                db: Session = Depends(get_db)):
    return crud.create_song(db, song = song,
                            artist_id = artist_id, album_id = album_id)


@app.delete("/songs/{song_id}", response_model = schemas.Song)
def remove_song(song_id, db: Session = Depends(get_db)):
    song = crud.remove_song(db, song_id)
    if song is None:
        raise HTTPException(status_code = 404, detail = "Song not found")

    return song


@app.get("/albums/", response_model = list[schemas.Album])
def get_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = crud.get_albums(db, skip = skip, limit = limit)
    return albums


@app.get("/albums/{album_id}", response_model = schemas.Album)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id = album_id)
    if album is None:
        raise HTTPException(status_code = 404, detail = "Album not found")

    return album


@app.post("/albums/", response_model = schemas.Album)
def create_album(album: schemas.AlbumCreate,
                 artist_id: int, db: Session = Depends(get_db)):
    return crud.create_album(db, album = album, artist_id = artist_id)


@app.delete("/albums/{album_id}", response_model = schemas.Album)
def remove_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.remove_album(db, album_id)
    if album is None:
        raise HTTPException(status_code = 404, detail = "Album not found")

    return album


@app.get("/playlists/", response_model = list[schemas.Playlist])
def get_playlists(skip: int = 0, limit: int = 0,
                  db: Session = Depends(get_db)):
    playlists = crud.get_playlists(db, skip = skip, limit = limit)
    return playlists


@app.get("/playlists/{playlist_id}", response_model = schemas.Playlist)
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = crud.get_playlist(db, playlist_id = playlist_id)
    if playlist is None:
        return HTTPException(status_code = 404, detail = "Playlist not found")

    return playlist


@app.post("/playlists/", response_model = schemas.Playlist)
def create_playlist(playlist: schemas.PlaylistCreate,
                    owner_id: int, db: Session = Depends(get_db)):
    return crud.create_playlist(db, playlist = playlist, owner_id = owner_id)


@app.delete("/playlists/{playlist_id}", response_model = schemas.Playlist)
def remove_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = crud.remove_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code = 404, detail = "Playlist not found")

    return playlist
