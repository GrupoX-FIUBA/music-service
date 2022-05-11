from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .songs import Song  # noqa: F401
from .genres import Genre  # noqa: F401


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    description = Column(Text)

    artist_id = Column(String)

    genre_id = Column(Integer, ForeignKey("genres.id"))
    genre = relationship("Genre", back_populates = "albums")

    subscription = Column(Integer)
    blocked = Column(Boolean)

    songs = relationship("Song", back_populates = "album")
