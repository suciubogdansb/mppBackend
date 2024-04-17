from sqlalchemy import Column, UUID, String, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from database import Base


class GenreModel(Base):
    __tablename__ = "genres"

    genreId = Column(UUID, primary_key=True)
    name = Column(String)
    movies = relationship("MovieModel", back_populates="genre")


class MovieModel(Base):
    __tablename__ = "movies"

    movieId = Column(UUID, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    genreId = Column(UUID, ForeignKey("genres.genreId", onupdate="CASCADE", ondelete="CASCADE"))

    genre = relationship("GenreModel", back_populates="movies")
