from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import genres as crud
from app.schemas import genres as schemas
from .base import get_db, response_codes


router = APIRouter(
    prefix = "/genres",
    tags = ["Genres"],
)


@router.get("/", response_model = list[schemas.Genre])
def get_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    genres = crud.get_genres(db, skip = skip, limit = limit)
    return genres


@router.get("/{genre_id}", response_model = schemas.Genre,
            responses = {404: response_codes[404]})
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = crud.get_genre(db, genre_id = genre_id)
    if genre is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Genre not found")

    return genre


@router.post("/", response_model = schemas.Genre, status_code = 201)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    return crud.create_genre(db, genre = genre)


@router.patch("/{genre_id}", response_model = schemas.Genre,
              responses = {404: response_codes[404]})
def edit_genre(genre_id: int, genre: schemas.GenreUpdate,
               db: Session = Depends(get_db)):
    db_genre = get_genre(genre_id, db)

    return crud.edit_genre(db, genre = db_genre, updated_genre = genre)


@router.delete("/{genre_id}", response_model = schemas.Genre,
               responses = {404: response_codes[404]})
def remove_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = crud.remove_genre(db, genre_id)
    if genre is None:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND,
                            detail = "Genre not found")

    return genre
