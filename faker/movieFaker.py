import os
import random
import time
import uuid

import dotenv
import schedule
from faker import Faker
from sqlalchemy import create_engine, insert, MetaData, Table, Column, UUID, String, Integer, select

from Model.DatabaseModels.models import GenreModel

fake = Faker()
dotenv.load_dotenv()

genresId = []

metadata = MetaData()
my_table = Table('movies', metadata,
                 Column('movieId', UUID, primary_key=True),
                 Column('title', String),
                 Column('year', Integer),
                 Column('genreId', UUID),
                 )

genreTable = Table('genres', metadata,
                   Column('genreId', UUID, primary_key=True),
                   Column('name', String))


def generateMockData(count: int) -> list:
    global genresId
    movies = []
    for _ in range(count):
        movies.append({
            "movieId": uuid.uuid4(),
            "title": fake.word(),
            "year": random.randint(1900, 2023),
            "genreId": random.choice(genresId)
        })
    return movies


def addMockMovies():
    mockData = generateMockData(10000)
    engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI_FAKER"))
    with engine.connect() as connection:
        connection.execute(insert(my_table), mockData)
        connection.commit()
        connection.close()
    engine.dispose()


def getGenres():
    global genresId
    engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI_FAKER"))
    with engine.connect() as connection:
        result = connection.execute(select(genreTable.c.genreId))
        genresId = [row[0] for row in result]
        connection.close()
    engine.dispose()


def startCronJob():
    getGenres()
    schedule.every(3).seconds.do(addMockMovies)
    while True:
        schedule.run_pending()
        time.sleep(1)


startCronJob()
