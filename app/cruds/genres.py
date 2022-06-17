from sqlalchemy.orm import Session

from app.models import genres as models
from app.schemas import genres as schemas


def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()


def get_genre(db: Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def genre_exists(db: Session, genre_id: int):
    return get_genre(db, genre_id) is not None


def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def edit_genre(db: Session, genre: schemas.Genre,
               updated_genre: schemas.GenreUpdate):
    for key, value in updated_genre.dict(exculde_unset = True).items():
        setattr(genre, key, value)

    db.commit()
    db.refresh(genre)
    return genre


def remove_genre(db: Session, genre_id: int):
    db_genre = get_genre(db, genre_id)
    if db_genre is None:
        return None

    db.delete(db_genre)
    db.commit()

    return db_genre
