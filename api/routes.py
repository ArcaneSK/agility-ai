import io

from fastapi import APIRouter, Request, File, UploadFile

from database import session
from database.models import *
from config import Config
from utils.stt import do_stt
from utils.tts import do_tts

from .schemas import *

cfg = Config()
router = APIRouter()
    
@router.get('/prompt', response_model=list[PromptSchema])
async def get_all_system_prompts():
    with session:
        prompts = Prompt.select(role="system") 
        return [PromptSchema.from_orm(pmpt) for pmpt in prompts]
    
@router.post('/prompt', response_model=list[PromptSchema])
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
        chat.add_message("system", "You are a helpful AI chat bot.")

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

@router.post('/speech-to-text')
async def speach_to_text(file: UploadFile = File(...)):
    text = ''
    
    audio_stream = io.BytesIO(await file.read())

    text = do_stt(audio_stream)

    print(f'Audio file processed -- Result: {text}')

    return { 'text': text }

@router.post('/text-to-speech')
async def text_to_speech(text: str):

    audio_data = do_tts(text)

    return { 'text': text }