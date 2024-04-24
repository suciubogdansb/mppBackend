from typing import Union, List
from uuid import UUID

from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    year: int
    genreId: UUID

    def toJSON(self):
        return {
            "title": self.title,
            "year": self.year,
            "genre": str(self.genreId)
        }


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    movieId: UUID

    def __init__(self, movieId: UUID, title: str, year: int, genreId: UUID):
        super().__init__(movieId=movieId, title=title, year=year, genreId=genreId)

    def toJSON(self):
        return {
            "id": str(self.movieId),
            "title": self.title,
            "year": self.year,
            "genre": str(self.genreId)
        }

    class Config:
        orm_mode = True
