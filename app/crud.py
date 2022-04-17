from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas


def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()


def create_song(db: Session, song: schemas.SongCreate,
                artist_id: int, album_id: Optional[int] = None):
    db_song = models.Song(**song.dict(),
                          artist_id = artist_id, album_id = album_id)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Album).offset(skip).limit(limit).all()


def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()


def create_album(db: Session, album: schemas.AlbumCreate, artist_id: int):
    db_album = models.Album(**album.dict(), artist_id = artist_id)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def get_playlists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Playlist).offset(skip).limit(limit).all()


def get_playlist(db: Session, playlist_id: int):
    return db.query(models.Playlist)\
             .filter(models.Playlist.id == playlist_id).first()


def create_playlist(db: Session, playlist: schemas.PlaylistCreate,
                    owner_id: Optional[int] = None):
    db_playlist = models.Playlist(**playlist, owner_id = owner_id)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist
