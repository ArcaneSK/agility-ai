import json

from fastapi import APIRouter, HTTPException

from database import session
from database.models import *
from config import Config
from llm.chat import Chat

from .schemas import *

cfg = Config()
router = APIRouter()

@router.get('/prompt', response_model=list[PromptSchema])
async def get_all_system_prompts():
    with session:
        prompts = Prompt.select(role="system") 
        return [PromptSchema.from_orm(pmpt) for pmpt in prompts]

@router.get('/conversation/{cid}')
async def read_conversation(cid: int):
    with session:
        conversation = Conversation[cid]
        return ConversationSchema.from_orm(conversation)

@router.put('/conversation/{cid}')
async def update_conversation(cid: int, message: MessageSchema):
    with session:
        c = Conversation[cid]
        m = Message(conversation=c, origin=message.origin, role=message.role, text=message.text)
        return MessageSchema.from_orm(m)
    
@router.post('/complete', response_model=MessageSchema)
async def complete(completion: Completion):
    chat = Chat()
    
    if completion.cid:
        chat.load(completion.cid)
    else:
        chat.create()
        chat.add_message("system", "You are a helpfule AI chat bot, named Carl.")

    chat.add_message("user", completion.message.text)
    resp = chat.complete(model=cfg.smart_cli_model)
    chat.add_message("assistant", resp)

    resp_obj = {
        'role': 'assistant',
        'text': resp
    }

    return MessageSchema(**resp_obj)