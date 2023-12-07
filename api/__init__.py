from fastapi import FastAPI

from llm.chat import Chat

from .routes import router

app = FastAPI()
app.chat = Chat()

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "success"}