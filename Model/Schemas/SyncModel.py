from typing import List
from uuid import UUID

from pydantic import BaseModel

from Model.Schemas.Genre import Genre
from Model.Schemas.Movie import Movie


class SyncModel(BaseModel):
    modifiedMovies: List[Movie]
    removedMovies: List[UUID]
    modifiedGenres: List[Genre]
    removedGenres: List[UUID]
