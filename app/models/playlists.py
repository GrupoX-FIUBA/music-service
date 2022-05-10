from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .songs import Song  # noqa: F401


song_table = Table(
    "playlists_songs",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id")),
    Column("playlist_id", ForeignKey("playlists.id"))
)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    description = Column(Text)

    owner_id = Column(String)
    collaborative = Column(Boolean)

    songs = relationship("Song", secondary = song_table)
