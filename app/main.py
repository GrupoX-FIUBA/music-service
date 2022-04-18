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


@app.patch("/songs/{song_id}", response_model = schemas.Song)
def edit_song(song_id: int, song: schemas.SongUpdate,
              db: Session = Depends(get_db)):
    db_song = get_song(song_id, db)

    return crud.edit_song(db, song = db_song, updated_song = song)


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


@app.post("/albums/{album_id}/songs/{song_id}", response_model = schemas.Song)
def add_song_to_album(album_id: int, song_id: int,
                      db: Session = Depends(get_db)):
    album = get_album(album_id, db)
    song = get_song(song_id, db)

    return crud.add_album_song(db, song = song, album = album)


@app.delete("/albums/{album_id}/songs/{song_id}",
            response_model = schemas.Song)
def remove_song_from_album(album_id: int, song_id: int,
                           db: Session = Depends(get_db)):
    album = get_album(album_id, db)
    song = get_song(song_id, db)

    if song.album_id != album_id:
        raise HTTPException(status_code = 404, detail = "Song not in album")

    return crud.remove_album_song(db, album = album, song = song)


@app.post("/albums/", response_model = schemas.Album)
def create_album(album: schemas.AlbumCreate,
                 artist_id: int, db: Session = Depends(get_db)):
    return crud.create_album(db, album = album, artist_id = artist_id)


@app.patch("/albums/{album_id}", response_model = schemas.Album)
def edit_album(album_id: int, album: schemas.AlbumUpdate,
               db: Session = Depends(get_db)):
    db_album = get_album(album_id, db)

    return crud.edit_album(db, album = db_album, updated_album = album)


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


@app.post("/playlists/{playlist_id}/songs/{song_id}",
          response_model = schemas.Song)
def add_song_to_playlist(playlist_id: int, song_id: int,
                         db: Session = Depends(get_db)):
    playlist = get_playlist(playlist_id, db)
    song = get_song(song_id, db)

    return crud.add_playlist_song(db, song = song, playlist = playlist)


@app.delete("/playlists/{playlist_id}/songs/{song_id}",
            response_model = schemas.Song)
def remove_song_from_playlist(playlist_id: int, song_id: int,
                              db: Session = Depends(get_db)):
    playlist = get_playlist(playlist_id, db)
    song = get_song(song_id, db)
    if song not in playlist.songs:
        raise HTTPException(status_code = 404, detail = "Song not in playlist")

    return crud.remove_playlist_song(db, song = song, playlist = playlist)


@app.post("/playlists/", response_model = schemas.Playlist)
def create_playlist(playlist: schemas.PlaylistCreate,
                    owner_id: int, db: Session = Depends(get_db)):
    return crud.create_playlist(db, playlist = playlist, owner_id = owner_id)


@app.patch("/playlist/{playlist_id}", response_model = schemas.Playlist)
def edit_playlist(playlist_id: int, playlist: schemas.PlaylistUpdate,
                  db: Session = Depends(get_db)):
    db_playlist = get_playlist(playlist_id, db)

    return crud.edit_playlist(db, playlist = db_playlist, updated_playlist = playlist)


@app.delete("/playlists/{playlist_id}", response_model = schemas.Playlist)
def remove_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = crud.remove_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code = 404, detail = "Playlist not found")

    return playlist
