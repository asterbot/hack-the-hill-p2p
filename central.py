# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Block(BaseModel):
    id: str
    ip: str


# Dictionary to store id and associated IPs
central_authority = {}


@app.get("/")
def read_root():
    return {"message": "I'M ALIVE!"}


@app.post("/publish_id/")
def create_item(data: Block):
    # Check if the id already exists in central_authority
    if data.id not in central_authority:
        central_authority[data.id] = set()  # Initialize with an empty set

    # Append the new IP to the list
    central_authority[data.id].add(data.ip)

    # Print the central_authority dictionary to check the current state
    print(central_authority)

    return {"message": "ok"}
