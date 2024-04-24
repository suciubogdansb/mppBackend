from typing import Union
from uuid import UUID

from Model.Schemas.Movie import Movie
from Model.Schemas.SyncModel import SyncModel
from Repository.RepositoryInterface import RepositoryInterface


class Service:
    def __init__(self, repository: RepositoryInterface):
        self.__repository = repository

    def getAll(self, orderType: str, page: Union[int, None]):
        if page is None:
            listOfMovies = self.__repository.getAll(orderType)
        else:
            listOfMovies = self.__repository.getPage(page, orderType)
        return listOfMovies

    def addMovie(self, movie: Movie):
        return self.__repository.addEntity(movie)

    def getMovie(self, movieId):
        return self.__repository.getEntity(movieId)

    def updateMovie(self, movie: Movie):
        return self.__repository.updateEntity(movie)

    def deleteMovie(self, movieId: UUID):
        return self.__repository.deleteEntity(movieId)

    def getGenres(self, page: Union[int, None]):
        if page is None:
            return self.__repository.getGenres()
        return self.__repository.getGenrePage(page)

    def addGenre(self, genre):
        return self.__repository.addGenre(genre)

    def deleteGenre(self, genreId: UUID):
        return self.__repository.deleteGenre(genreId)

    def sync(self, syncBatch: SyncModel):
        count, failedCount = 0, 0
        modifiedGenres = syncBatch.modifiedGenres
        for genre in modifiedGenres:
            count += 1
            try:
                self.__repository.addGenre(genre)
            except Exception as e:
                failedCount += 1
        removedGenres = syncBatch.removedGenres
        for genreId in removedGenres:
            count += 1
            try:
                self.__repository.deleteGenre(genreId)
            except Exception as e:
                failedCount += 1
        modifiedMovies = syncBatch.modifiedMovies
        for movie in modifiedMovies:
            count += 1
            try:
                self.__repository.upsertEntity(movie)
            except Exception as e:
                failedCount+= 1
        removedMovies = syncBatch.removedMovies
        for movieId in removedMovies:
            count += 1
            try:
                self.__repository.deleteEntity(movieId)
            except Exception as e:
                failedCount += 1
        return {"message": f"{count - failedCount} out of {count} operations successful."}

    def getGenreById(self, genreId):
        return self.__repository.getGenreById(genreId)

    def getMultipleGenres(self, genresId: list[UUID]):
        return self.__repository.getMultipleGenres(genresId)

