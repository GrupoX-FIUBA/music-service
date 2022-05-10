from sqlalchemy.orm import Session

from app.models import playlists as models
from app.schemas import playlists as schemas
from app.schemas.songs import Song


def get_playlists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Playlist).offset(skip).limit(limit).all()


def get_playlist(db: Session, playlist_id: int):
    return db.query(models.Playlist)\
             .filter(models.Playlist.id == playlist_id).first()


def create_playlist(db: Session, playlist: schemas.PlaylistCreate):
    db_playlist = models.Playlist(**playlist.dict(), collaborative = False)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def edit_playlist(db: Session, playlist: schemas.Playlist,
                  updated_playlist: schemas.PlaylistUpdate):
    for key, value in updated_playlist.dict(exclude_unset = True).items():
        setattr(playlist, key, value)

    db.commit()
    db.refresh(playlist)
    return playlist


def remove_playlist(db: Session, playlist_id: int):
    db_playlist = get_playlist(db, playlist_id)
    if db_playlist is None:
        return None

    db.delete(db_playlist)
    db.commit()

    return db_playlist


def add_playlist_song(db: Session, song: Song,
                      playlist: schemas.Playlist):
    playlist.songs.append(song)
    db.commit()
    db.refresh(playlist)
    return song


def remove_playlist_song(db: Session, song: Song,
                         playlist: schemas.Playlist):
    playlist.songs.remove(song)
    db.commit()
    db.refresh(playlist)
    return song
