from typing import Union
from uuid import UUID

from pydantic import BaseModel


class Movie(BaseModel):
    id: UUID
    title: str
    year: int
    genre: str

    def __init__(self, id: Union[str, UUID], title: str, year: int, genre: str):
        super().__init__(id=(id if type(id) is UUID else UUID(id)), title=title, year=year, genre=genre)

    def toJSON(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "year": self.year,
            "genre": self.genre
        }
