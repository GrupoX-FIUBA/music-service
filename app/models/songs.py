from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    artist_id = Column(Integer)
    album_id = Column(Integer, ForeignKey("albums.id"))

    album = relationship("Album", back_populates = "songs")
