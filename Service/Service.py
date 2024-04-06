from uuid import UUID

from Model.Movie import Movie
from Repository.RepositoryInterface import RepositoryInterface


class Service:
    def __init__(self, repository: RepositoryInterface):
        self.__repository = repository

    def getAll(self):
        return self.__repository.getAll()

    def addMovie(self, movie: Movie):
        return self.__repository.addEntity(movie)

    def getMovie(self, movieId):
        return self.__repository.getEntity(movieId)

    def updateMovie(self, movie: Movie):
        return self.__repository.updateEntity(movie)

    def deleteMovie(self, movieId: UUID):
        return self.__repository.deleteEntity(movieId)
