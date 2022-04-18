from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from .songs import Song  # noqa: F401


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    artist_id = Column(Integer)

    songs = relationship("Song", back_populates = "album")
