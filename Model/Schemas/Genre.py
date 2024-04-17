from typing import Union
from uuid import UUID

from pydantic import BaseModel


class Genre(BaseModel):
    genreId: UUID
    name: str

    def __init__(self, genreId: Union[str, UUID], name: str):
        super().__init__(genreId=(genreId if type(genreId) is UUID else UUID(genreId)), name=name)

    def toJSON(self):
        return {
            "genreId": str(self.genreId),
            "name": self.name
        }

    class Config:
        orm_mode = True
