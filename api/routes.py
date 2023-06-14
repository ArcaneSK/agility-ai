from fastapi import APIRouter

from database import session
from database.models import *

from .schemas import *


router = APIRouter()

@router.get('/prompt', response_model=list[PromptSchema])
async def get_all_prompts():
    with session:
        prompts = Prompt.select(role="system")
        print(prompts)
        
    return PromptSchema.from_orm(prompts)

@router.get('/conversation/{cid}')
async def read_conversation(cid: int):
    with session:
        conversation = Conversation[cid]
        return ConversationSchema.from_orm(conversation)

@router.post('/conversation')
async def create_conversation(conversation: ConversationSchema):
    return conversation

@router.put('/conversation/{cid}')
async def update_conversation(cid: int, message: MessageSchema):
    with session:
        c = Conversation[cid]
        m = Message(conversation=c, origin=message.origin, role=message.role, text=message.text)
        return MessageSchema.from_orm(m)