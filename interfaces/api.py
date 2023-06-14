from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from database import session
from database.models import *
from api.schemas import *

app = FastAPI()

@app.get('/')
async def root():
    return {"status": "success"}

@app.get('/prompt')
async def get_all_prompts():
    with session:
        return Prompt.select(role="system")

@app.get('/conversation/{cid}')
async def read_conversation(cid: int):
    with session:
        conversation = Conversation[cid]
        return ConversationSchema.from_orm(conversation)

@app.post('/conversation')
async def create_conversation(conversation: ConversationSchema):
    return conversation

@app.put('/conversation/{cid}')
async def update_conversation(cid: int, message: MessageSchema):
    with session:
        c = Conversation[cid]
        m = Message(conversation=c, origin=message.origin, role=message.role, text=message.text)
        return MessageSchema.from_orm(m)