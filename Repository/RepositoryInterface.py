from abc import abstractmethod, ABC


class RepositoryInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getAll(self, orderType):
        pass

    @abstractmethod
    def getEntity(self, id):
        pass

    @abstractmethod
    def addEntity(self, entity):
        pass

    @abstractmethod
    def updateEntity(self, entity):
        pass

    @abstractmethod
    def deleteEntity(self, id):
        pass

    @abstractmethod
    def loadData(self):
        pass

    @abstractmethod
    def saveData(self):
        pass

    def getGenres(self):
        pass

    def addGenre(self, entity):
        pass

    def deleteGenre(self, id):
        pass

    def upsertEntity(self, movie):
        pass

    def getPage(self, page, orderType):
        pass

    def getGenrePage(self, page):
        pass

    def getGenreById(self, genreId):
        pass

    def getMultipleGenres(self, genresId):
        pass