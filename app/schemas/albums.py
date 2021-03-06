from typing import Optional

from pydantic import BaseModel

from .songs import Song


class AlbumBase(BaseModel):
    title: str
    description: Optional[str]

    genre_id: int
    subscription: int


class AlbumCreate(AlbumBase):
    artist_id: str


class AlbumUpdate(AlbumBase):
    title: Optional[str]
    genre_id: Optional[int]

    subscription: Optional[int]
    blocked: Optional[bool]


class Album(AlbumBase):
    id: int
    artist_id: str
    blocked: bool
    songs: list[Song] = []

    class Config:
        orm_mode = True
