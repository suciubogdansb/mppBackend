from uuid import UUID

from sqlalchemy import desc
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

    def getAll(self, orderType) -> list[Movie]:
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
            except (IntegrityError, RepositoryException) as e:
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
        except (IntegrityError, RepositoryException) as e:
            raise RepositoryException("Key constraints violated")

    def deleteGenre(self, id: UUID):
        self.__database = SessionLocal()
        if self.__database.query(GenreModel).filter(GenreModel.genreId == id).delete(synchronize_session="fetch") == 0:
            raise RepositoryException("Genre not found")
        self.__database.commit()

    def getPage(self, page, orderType):
        self.__database = SessionLocal()
        if orderType == "ASC":
            return self.__database.query(MovieModel).order_by(MovieModel.title).limit(50).offset(page * 50).all()
        if orderType == "DESC":
            return self.__database.query(MovieModel).order_by(desc(MovieModel.title)).limit(50).offset(page * 50).all()
        return self.__database.query(MovieModel).limit(50).offset(page * 50).all()

    def getGenreByName(self, name: str):
        self.__database = SessionLocal()
        genre = self.__database.query(GenreModel).filter(GenreModel.name == name).first()
        if genre is None:
            raise RepositoryException("Genre not found")
        return genre

    def getGenrePage(self, page):
        self.__database = SessionLocal()
        return self.__database.query(GenreModel).limit(50).offset(page * 50).all()

    def getGenreById(self, genreId: UUID):
        self.__database = SessionLocal()
        genre = self.__database.query(GenreModel).filter(GenreModel.genreId == genreId).first()
        if genre is None:
            raise RepositoryException("Genre not found")
        return genre

    def getMultipleGenres(self, genresId):
        self.__database = SessionLocal()
        return self.__database.query(GenreModel).filter(GenreModel.genreId.in_(genresId)).all()