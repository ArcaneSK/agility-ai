import json

from fastapi import APIRouter, Request, HTTPException

from database import session
from database.models import *
from config import Config

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
    
@router.post('/complete', response_model=Completion)
async def complete(request: Request, completion: Completion):
    chat = request.app.chat

    if completion.cid:
        chat.load(completion.cid)
    else:
        chat.create()
        chat.add_message("system", "You are a helpfule AI chat bot, named Carl.")

    chat.add_message("user", completion.message.text)
    resp = chat.complete()
    chat.add_message("assistant", resp)

    resp_message = {
        'role': 'assistant',
        'text': resp
    }

    resp_completion = {
        'cid': chat.conversation_id,
        'message': resp_message
    }

    chat.clear()

    return Completion(**resp_completion)