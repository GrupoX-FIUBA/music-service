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


class AlbumBase(BaseModel):
    title: str


class AlbumCreate(AlbumBase):
    artist_id: int


class AlbumUpdate(AlbumBase):
    title: Optional[str]


class Album(AlbumBase):
    id: int
    artist_id: int
    songs: list[Song] = []

    class Config:
        orm_mode = True


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
