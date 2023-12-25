from fastapi import FastAPI

from llm.chat import Chat
from utils.tts import TextToSpeech

from .routes import router

app = FastAPI()
app.chat = Chat()
app.tts = TextToSpeech()

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "success"}