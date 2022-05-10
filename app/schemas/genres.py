from typing import Optional

from pydantic import BaseModel

from .songs import Song
from .albums import Album


class GenreBase(BaseModel):
    title: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    title: Optional[str]


class Genre(GenreBase):
    id: int
    title: str
    songs: list[Song] = []
    albums: list[Album] = []

    class Config:
        orm_mode = True
