from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Set, List

app = FastAPI()


class Block(BaseModel):
    id: str
    ip: str


# Dictionary to store id and associated IPs as a set
central_authority: Dict[str, Set[str]] = {}


@app.get("/")
def read_root():
    return {"message": "I'M ALIVE!"}


@app.post("/publish_id/")
def create_item(data: Block):
    try:
        # Initialize with an empty set if the ID does not exist
        if data.id not in central_authority:
            central_authority[data.id] = set()

        # Add the new IP to the set
        central_authority[data.id].add(data.ip)

        # Convert sets to lists for JSON serialization
        return {"message": "ok"}
    except Exception as e:
        print(e)
        return {"error": e}


@app.get("/get_all/")
def get_all_data() -> Dict[str, List[str]]:
    try:
        """Returns the entire central_authority dictionary as key-value pairs."""
        return {key: list(value) for key, value in central_authority.items()}
    except Exception as e:
        print(e)
        return {}


@app.get("/get_ips/{block_id}")
def get_ips(block_id: str) -> Dict[str, List[str]]:
    """Returns the list of IPs associated with a specific ID."""
    if block_id not in central_authority:
        return {"error": "not found"}

    return {block_id: list(central_authority[block_id])}
