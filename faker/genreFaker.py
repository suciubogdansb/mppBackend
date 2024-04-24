import os
import time
import uuid

import dotenv
import schedule
from faker import Faker
from sqlalchemy import create_engine, insert, MetaData, Table, Column, UUID, String

from Model.DatabaseModels.models import GenreModel

fake = Faker()
dotenv.load_dotenv()

metadata = MetaData()
my_table = Table('genres', metadata,
                 Column('genreId', UUID, primary_key=True),
                 Column('name', String),
                 )


def generateMockData(count: int) -> list:
    genres = []
    for _ in range(count):
        genres.append({
            "genreId": uuid.uuid4(),
            "name": fake.word()
        })
    return genres


def addMockGenres():
    mockData = generateMockData(100000)
    engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI_FAKER"))
    with engine.connect() as connection:
        connection.execute(insert(my_table), mockData)
        connection.commit()
        connection.close()
    engine.dispose()


def startCronJob():
    schedule.every(3).seconds.do(addMockGenres)
    while True:
        schedule.run_pending()
        time.sleep(1)

startCronJob()
