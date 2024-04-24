import random
import string
import time
import uuid
import requests
import schedule
import socketio

backendServer = "http://localhost:8000"

backendSocketIo = socketio.Client()


def addRandomItem():
    data = {
        "id": str(uuid.uuid4()),
        "title": "".join(random.choices(string.ascii_letters, k=10)),
        "year": random.randint(1900, 2022),
        "genre": "".join(random.choices(string.ascii_letters, k=10))
    }

    response = requests.post("http://localhost:8000/items", json=data)
    if (response.status_code == 201):
        print(f"Added item with id {data['id']}")
        backendSocketIo.emit("mockAdded", {"movie": data, "event": "add"})


@backendSocketIo.event
def connect():
    print("Connected to frontend server")


@backendSocketIo.event
def disconnect():
    print("Disconnected from frontend server")


backendSocketIo.connect(backendServer)

def startCronJob():
    schedule.every(15).seconds.do(addRandomItem)
    while True:
        schedule.run_pending()
        time.sleep(1)


startCronJob()
