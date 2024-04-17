from uuid import UUID

from Model.Schemas.Movie import Movie
from Repository.RepositoryInterface import RepositoryInterface


class Service:
    def __init__(self, repository: RepositoryInterface):
        self.__repository = repository

    def getAll(self, orderType: str):
        listOfMovies = self.__repository.getAll()
        if orderType == "ASC":
            return sorted(listOfMovies, key=lambda x: x.title)
        elif orderType == "DESC":
            return sorted(listOfMovies, key=lambda x: x.title, reverse=True)
        return listOfMovies

    def addMovie(self, movie: Movie):
        return self.__repository.addEntity(movie)

    def getMovie(self, movieId):
        return self.__repository.getEntity(movieId)

    def updateMovie(self, movie: Movie):
        return self.__repository.updateEntity(movie)

    def deleteMovie(self, movieId: UUID):
        return self.__repository.deleteEntity(movieId)

    def getGenres(self):
        return self.__repository.getGenres()

    def addGenre(self, genre):
        return self.__repository.addGenre(genre)

    def deleteGenre(self, genreId: UUID):
        return self.__repository.deleteGenre(genreId)
