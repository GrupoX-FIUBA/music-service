from sqlalchemy.orm import Session

from app.models import songs as models
from app.schemas import songs as schemas


def get_songs(db: Session, skip: int = 0, limit: int = 100,
              filters: list = []):
    query = db.query(models.Song)
    if len(filters) > 0:
        query = query.filter(*filters)

    return query.offset(skip).limit(limit).all()


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()


def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.dict(), blocked = False)
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
