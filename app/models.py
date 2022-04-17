from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


playlist_song_table = Table(
    "association",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id")),
    Column("playlist_id", ForeignKey("playlists.id"))
)


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    artist_id = Column(Integer)
    album_id = Column(Integer, ForeignKey("albums.id"))

    album = relationship("Album", back_populates = "songs")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    artist_id = Column(Integer)

    songs = relationship("Song", back_populates = "album")


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    owner_id = Column(Integer)

    songs = relationship("Song", secondary = playlist_song_table)
