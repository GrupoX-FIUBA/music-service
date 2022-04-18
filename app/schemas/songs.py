from typing import Optional

from pydantic import BaseModel


class SongBase(BaseModel):
    title: str


class SongCreate(SongBase):
    artist_id: int


class SongUpdate(SongBase):
    title: Optional[str]
    album_id: Optional[int]


class Song(SongBase):
    id: int
    artist_id: int
    album_id: Optional[int] = None

    class Config:
        orm_mode = True
