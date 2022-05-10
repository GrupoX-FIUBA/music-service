from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .songs import Song  # noqa: F401
from .genres import Genre  # noqa: F401


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    artist_id = Column(String)
    blocked = Column(Boolean)

    genre_id = Column(Integer, ForeignKey("genres.id"))
    genre = relationship("Genre", back_populates = "albums")

    songs = relationship("Song", back_populates = "album")
