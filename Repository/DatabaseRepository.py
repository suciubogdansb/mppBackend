from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from Model.DatabaseModels.models import GenreModel, MovieModel
from Model.Exceptions.RepositoryException import RepositoryException
from Model.Schemas.Genre import Genre
from Model.Schemas.Movie import Movie
from Repository.RepositoryInterface import RepositoryInterface
from database import SessionLocal


class DatabaseRepository(RepositoryInterface):
    def __init__(self, database: Session):
        self.__database = database

    def getAll(self):
        self.__database = SessionLocal()
        return self.__database.query(MovieModel).all()

    def getEntity(self, id: UUID):
        self.__database = SessionLocal()
        movie = self.__database.query(MovieModel).filter(MovieModel.movieId == id).first()
        if movie is None:
            raise RepositoryException("Movie not found")
        return movie

    def addEntity(self, entity: Movie):
        self.__database = SessionLocal()
        try:
            movie = MovieModel(**entity.dict())
            self.__database.add(movie)
            self.__database.commit()
            self.__database.refresh(movie)
            return movie
        except IntegrityError as e:
            raise RepositoryException("Key constraints violated")

    def updateEntity(self, entity: Movie):
        self.__database = SessionLocal()
        movie = self.__database.query(MovieModel).filter(MovieModel.movieId == entity.movieId).first()
        if movie is None:
            raise RepositoryException("Movie not found")
        movie.title = entity.title
        movie.year = entity.year
        movie.genreId = entity.genreId
        self.__database.commit()
        self.__database.refresh(movie)
        return movie

    def deleteEntity(self, id: UUID):
        self.__database = SessionLocal()
        if self.__database.query(MovieModel).filter(MovieModel.movieId == id).delete(synchronize_session="fetch") == 0:
            raise RepositoryException("Movie not found")
        self.__database.commit()

    def upsertEntity(self, entity: Movie):
        self.__database = SessionLocal()
        movie = self.__database.query(MovieModel).filter(MovieModel.movieId == entity.movieId).first()
        if movie is None:
            try:
                movie = MovieModel(**entity.dict())
                self.__database.add(movie)
                self.__database.commit()
                self.__database.refresh(movie)
                return movie
            except IntegrityError as e:
                raise RepositoryException("Key constraints violated")
        movie.title = entity.title
        movie.year = entity.year
        movie.genreId = entity.genreId
        self.__database.commit()
        self.__database.refresh(movie)
        return movie

    def loadData(self):
        pass

    def saveData(self):
        pass

    def getGenres(self):
        self.__database = SessionLocal()
        return self.__database.query(GenreModel).all()

    def addGenre(self, entity: Genre):
        self.__database = SessionLocal()
        try:
            genre = GenreModel(**entity.dict())
            self.__database.add(genre)
            self.__database.commit()
            self.__database.refresh(genre)
            return genre
        except IntegrityError as e:
            raise RepositoryException("Key constraints violated")

    def deleteGenre(self, id: UUID):
        self.__database = SessionLocal()
        if self.__database.query(GenreModel).filter(GenreModel.genreId == id).delete(synchronize_session="fetch") == 0:
            raise RepositoryException("Genre not found")
        self.__database.commit()

