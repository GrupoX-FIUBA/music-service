from typing import Optional

from pydantic import BaseModel

from .songs import Song


class AlbumBase(BaseModel):
    title: str


class AlbumCreate(AlbumBase):
    artist_id: str
    genre_id: int


class AlbumUpdate(AlbumBase):
    title: Optional[str]
    genre_id: Optional[int]


class Album(AlbumBase):
    id: int
    artist_id: str
    blocked: bool
    genre_id: int
    songs: list[Song] = []

    class Config:
        orm_mode = True
