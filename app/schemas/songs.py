from typing import Optional

from pydantic import BaseModel


class SongBase(BaseModel):
    title: str


class SongCreate(SongBase):
    artist_id: str
    album_id: Optional[int]
    genre_id: int


class SongUpdate(SongBase):
    title: Optional[str]
    album_id: Optional[int]
    genre_id: Optional[int]
    blocked: Optional[bool]


class Song(SongBase):
    id: int
    artist_id: str
    album_id: Optional[int] = None
    genre_id: int
    blocked: bool

    class Config:
        orm_mode = True
