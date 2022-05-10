from typing import Optional

from pydantic import BaseModel

from .songs import Song


class PlaylistBase(BaseModel):
    title: str
    description: Optional[str]


class PlaylistCreate(PlaylistBase):
    owner_id: str


class PlaylistUpdate(PlaylistBase):
    title: Optional[str]
    collaborative: Optional[bool]


class Playlist(PlaylistBase):
    id: int
    owner_id: str
    collaborative: bool
    songs: list[Song] = []

    class Config:
        orm_mode = True
