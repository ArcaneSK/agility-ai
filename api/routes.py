import io
import tempfile
import soundfile as sf

from fastapi import APIRouter, Request, File, UploadFile, Body
from fastapi.responses import FileResponse

from database import session
from database.models import *
from config import Config
from utils.stt import do_stt

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
        chat.add_message("system", "You are a helpful AI chat bot. Always keep your resonses short, maximum of 4 sentences. Always respond lovingly.")

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
async def speech_to_text(file: UploadFile = File(...)):
    text = ''
    audio_stream = io.BytesIO(await file.read())
    text = do_stt(audio_stream)

    return { 'text': text }

@router.post('/text-to-speech')
async def text_to_speech(request: Request, text: str = Body(..., embed=True), voice_name: str = Body(..., embed=True)):
    tts = request.app.tts

    audio_data = tts.do_tts(text, voice_name)

    wavefile_path = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    sf.write(wavefile_path, audio_data, 22050, format='WAV')

    return FileResponse(wavefile_path, media_type="audio/wav")