from abc import abstractmethod, ABC


class RepositoryInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getAll(self):
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
