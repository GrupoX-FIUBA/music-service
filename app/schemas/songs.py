from typing import Optional

from pydantic import BaseModel


class SongBase(BaseModel):
    title: str
    description: Optional[str]

    subscription: int
    file_uri: str


class SongCreate(SongBase):
    artist_id: str
    genre_id: int

    album_id: Optional[int]


class SongUpdate(SongBase):
    title: Optional[str]
    album_id: Optional[int]
    genre_id: Optional[int]
    subscription: Optional[int]
    blocked: Optional[bool]
    file_uri: Optional[str]


class Song(SongBase):
    id: int
    artist_id: str
    album_id: Optional[int] = None
    genre_id: int
    blocked: bool

    class Config:
        orm_mode = True
