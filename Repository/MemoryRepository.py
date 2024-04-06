import json
from uuid import UUID

from Model.Exceptions.RepositoryException import RepositoryException
from Model.Movie import Movie
from Repository.RepositoryInterface import RepositoryInterface


class MemoryRepository(RepositoryInterface):
    def __init__(self):
        super().__init__()
        self.__entities: dict[UUID, Movie] = {}

    def getAll(self) -> list[Movie]:
        return list(self.__entities.values())

    def getEntity(self, movieId: UUID) -> Movie:
        if movieId not in self.__entities:
            raise RepositoryException("Id not found.")
        return self.__entities[movieId]

    def addEntity(self, movie: Movie) -> dict[str, str]:
        if movie.id in self.__entities:
            raise RepositoryException("Id already used.")
        self.__entities[movie.id] = movie
        return {"message": f"{movie.id} added successfully"}

    def updateEntity(self, movie: Movie) -> dict[str, str]:
        if movie.id not in self.__entities:
            raise RepositoryException("Id not found.")
        self.__entities[movie.id] = movie
        return {"message": f"{movie.id} updated successfully"}

    def deleteEntity(self, movieId: UUID) -> dict[str, str]:
        if movieId not in self.__entities:
            raise RepositoryException("Id not found.")
        del self.__entities[movieId]
        return {"message": f"{movieId} removed successfully"}

    def loadData(self):
        try:
            with open("data.json", "r") as file:
                jsonContents = json.load(file)
                self.__entities = {UUID(key): Movie(**value) for key, value in jsonContents.items()}
        except FileNotFoundError:
            pass

    def saveData(self):
        with open("data.json", "w") as file:
            entitiesWithStringKeys = {str(key): value for key, value in self.__entities.items()}
            json.dump(entitiesWithStringKeys, file, default=lambda o: o.toJSON(), indent=4)
