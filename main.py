import os
from contextlib import asynccontextmanager
from uuid import UUID
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Model.Exceptions.RepositoryException import RepositoryException
from Model.Movie import Movie
from Repository.MemoryRepository import MemoryRepository
from Service.Service import Service
import dotenv
import socketio

dotenv.load_dotenv()
backendPort = int(os.getenv("BACKEND_PORT"))
frontendPort = int(os.getenv("FRONTEND_PORT"))

repository = MemoryRepository()
service = Service(repository)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    repository.loadData()
    yield
    # Clean up the ML models and release the resources
    repository.saveData()

origins = [
    "http://localhost",
    f"http://localhost:{frontendPort}",
]

socketIo = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def loadData():
#     repository.loadData()
#
#
# @app.on_event("shutdown")
# async def saveData():
#     repository.saveData()
@socketIo.event
async def connect(sid, environ):
    print(f"connect {sid}")

@socketIo.event
async def mockAdded(sid, data):
    print(f"mockAdded {sid} {data}")
    await socketIo.emit("dataModified", data)

@socketIo.event
async def disconnect(sid):
    print(f"disconnect {sid}")


@app.get("/items", response_model=list[Movie])
async def getAll():
    return service.getAll()


@app.post("/items", status_code=201)
async def addMovie(movie: Movie):
    try:
        result = service.addMovie(movie)
        # await socketIo.emit("dataModified", {"event": "add"})
        return result
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
        result = service.updateMovie(movie)
        # await socketIo.emit("dataModified", {"event": "update"})
        return result
    except RepositoryException:
        raise HTTPException(status_code=404, detail="Id not found.")


@app.delete("/items/{movieId}", status_code=204)
async def deleteMovie(movieId: UUID):
    try:
        service.deleteMovie(movieId)
        # await socketIo.emit("dataModified", {"event": "delete"})
    except RepositoryException:
        raise HTTPException(status_code=404, detail="Id not found.")


socketApp = socketio.ASGIApp(socketIo, app)

if __name__ == "__main__":
    uvicorn.run(socketApp, host="0.0.0.0", port=backendPort)

# To run cronjob.py, execute the following command:
# python cronjob.py
