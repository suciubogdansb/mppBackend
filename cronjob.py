import random
import string
import time
import uuid
import requests
import schedule


def addRandomItem():
    data = {
        "id": str(uuid.uuid4()),
        "title": "".join(random.choices(string.ascii_letters, k=10)),
        "year": random.randint(1900, 2022),
        "genre": "".join(random.choices(string.ascii_letters, k=10))
    }
    print(data)
    response = requests.post("http://localhost:8000/items", json=data)
    print(response.text)


def startCronJob():
    schedule.every(15).seconds.do(addRandomItem)
    while True:
        schedule.run_pending()
        time.sleep(1)


startCronJob()
