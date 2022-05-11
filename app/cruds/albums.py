from sqlalchemy.orm import Session

from app.models import albums as models
from app.schemas import albums as schemas
from app.schemas.songs import Song


def get_albums(db: Session, skip: int = 0, limit: int = 100,
               filters: list = []):
    query = db.query(models.Album)
    if len(filters) > 0:
        query = query.filter(*filters)

    return query.offset(skip).limit(limit).all()


def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()


def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(**album.dict(), blocked = False)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def edit_album(db: Session, album: schemas.Album,
               updated_album: schemas.AlbumUpdate):
    for key, value in updated_album.dict(exclude_unset = True).items():
        setattr(album, key, value)

    db.commit()
    db.refresh(album)
    return album


def remove_album(db: Session, album_id: int):
    db_album = get_album(db, album_id)
    if db_album is None:
        return None

    db.delete(db_album)
    db.commit()

    return db_album


def add_album_song(db: Session, song: Song, album: schemas.Album):
    song.album_id = album.id
    album.songs.append(song)
    db.commit()
    db.refresh(song)
    db.refresh(album)
    return song


def remove_album_song(db: Session, song: Song, album: schemas.Album):
    song.album_id = None
    album.songs.remove(song)
    db.commit()
    db.refresh(song)
    db.refresh(album)

    return song
