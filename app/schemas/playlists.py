from typing import Optional

from pydantic import BaseModel

from .songs import Song


class PlaylistBase(BaseModel):
    title: str


class PlaylistCreate(PlaylistBase):
    owner_id: int


class PlaylistUpdate(PlaylistBase):
    title: Optional[str]


class Playlist(PlaylistBase):
    id: int
    owner_id: int
    songs: list[Song] = []

    class Config:
        orm_mode = True
