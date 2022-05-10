from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    description = Column(Text)

    artist_id = Column(String)

    album_id = Column(Integer, ForeignKey("albums.id"))
    album = relationship("Album", back_populates = "songs")

    genre_id = Column(Integer, ForeignKey("genres.id"))
    genre = relationship("Genre", back_populates = "songs")

    subscription = Column(Integer)
    blocked = Column(Boolean)

    file_uri = Column(String)
