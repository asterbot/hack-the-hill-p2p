# hack-the-hill-p2p

pip install -r requirements.txt

### To run central server
uvicorn central:app --reload
default port is 8000

Route map:
- /             -> ping the server, gets a message if alive
- /publish_id   -> publish the id of the file
Example request (json):
```
{
"id": "block123",
"ip": "192.168.1.1"
}
```
