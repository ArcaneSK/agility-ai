from database import session
from database.models import *
from api.schemas import *

from api import app

@app.get('/')
async def root():
    return {"status": "success"}

@app.get('/prompt', response_model=list[PromptSchema])
async def get_all_prompts():
    with session:
        prompts = Prompt.select(role="system")
        print(prompts)
        
    return PromptSchema.from_orm(prompts)

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