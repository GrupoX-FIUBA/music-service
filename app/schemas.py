from typing import Optional

from pydantic import BaseModel


class SongBase(BaseModel):
    title: str


class SongCreate(SongBase):
    pass


class Song(SongBase):
    id: int
    artist_id: int
    album_id: Optional[int] = None

    class Config:
        orm_mode = True


class AlbumBase(BaseModel):
    title: str


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int
    artist_id: int
    songs: list[Song] = []

    class Config:
        orm_mode = True


class PlaylistBase(BaseModel):
    title: str


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    id: int
    owner_id: int
    songs: list[Song] = []

    class Config:
        orm_mode = True
