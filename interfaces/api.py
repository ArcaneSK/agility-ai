import uvicorn

def run() -> None:
    """
    Launch the API using Uvicorn
    """
    uvicorn.run("api:app", host="127.0.0.1", port=8000)