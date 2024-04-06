from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Model.Exceptions.RepositoryException import RepositoryException
from Model.Movie import Movie
from Repository.MemoryRepository import MemoryRepository
from Service.Service import Service

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = MemoryRepository()
service = Service(repository)


@app.on_event("startup")
async def loadData():
    repository.loadData()


@app.on_event("shutdown")
async def saveData():
    repository.saveData()


@app.get("/items", response_model=list[Movie])
async def getAll():
    return service.getAll()


@app.post("/items", status_code=201)
async def addMovie(movie: Movie):
    try:
        return service.addMovie(movie)
    except RepositoryException:
        raise HTTPException(status_code=404, detail="Id already used.")


@app.get("/items/{movieId}")
async def getItem(movieId: UUID):
    try:
        return service.getMovie(movieId)
    except RepositoryException:
        raise HTTPException(status_code=404, detail="Item not found.")


@app.put("/items/{movieId}")
async def updateMovie(movieId: UUID, movie: Movie):
    try:
        movie.id = movieId
        return service.updateMovie(movie)
    except RepositoryException:
        raise HTTPException(status_code=404, detail="Id not found.")


@app.delete("/items/{movieId}", status_code=204)
async def deleteMovie(movieId: UUID):
    try:
        service.deleteMovie(movieId)
    except RepositoryException:
        raise HTTPException(status_code=404, detail="Id not found.")
