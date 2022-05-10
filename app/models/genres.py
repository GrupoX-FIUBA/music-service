from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)

    songs = relationship("Song", back_populates = "genre")
    albums = relationship("Album", back_populates = "genre")
