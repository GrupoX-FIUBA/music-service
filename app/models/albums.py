from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .songs import Song  # noqa: F401


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    artist_id = Column(Integer)
    blocked = Column(Boolean)

    songs = relationship("Song", back_populates = "album")
