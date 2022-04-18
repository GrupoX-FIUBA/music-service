from typing import Optional

from sqlalchemy.orm import Session

from app.models import songs as models
from app.schemas import songs as schemas


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


def edit_song(db: Session, song: schemas.Song,
              updated_song: schemas.SongUpdate):
    for key, value in updated_song.dict(exclude_unset = True).items():
        setattr(song, key, value)

    db.commit()
    db.refresh(song)
    return song


def remove_song(db: Session, song_id: int):
    db_song = get_song(db, song_id)
    if db_song is None:
        return None

    db.delete(db_song)
    db.commit()

    return db_song
