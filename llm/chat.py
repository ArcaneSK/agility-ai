import string
import random
from pony.orm import select

from .memory import format_memory, MemoryScheme

from config import Config

from database import session
from database.models import *

from llm.modules.openai_module import OpenAIModule
from llm.modules.huggingface_module import HuggingFaceModule

class Chat():

    def __init__(self) -> None:
        """ 
        Initialize the Chat class
        """
        self.cfg = Config()

        self.conversation_id = None

        self.messages = []
        self.shadow_messages = []

        if self.cfg.module_type == 'huggingface':
            self.module = HuggingFaceModule(self.cfg)
        else:
            self.module = OpenAIModule(self.cfg)

        print("Loading Model")
        self.module.load_model()

    def create(self) -> None:
        self.conversation_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

        with session:
            c = Conversation(name=self.conversation_name)

        if c:
            self.conversation_id = c.id

    def load(self, conversation_id) -> bool:
        with session:
            c = Conversation[conversation_id]

            if c:
                self.conversation_id = c.id
                self.conversation_name = c.name
                
                message_set = select(m for m in c.messages).order_by(Message.created)
                self.messages = [dict(role=obj.role, content=obj.text) for obj in message_set]

                return True

        return False
    
    def clear(self):
        self.conversation_id = None
        self.messages = []
        self.shadow_messages = []

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the message history
        """
        self.messages.append({
            "role": role,
            "content": content
        })

        if self.conversation_id:
            with session:
                c = Conversation[self.conversation_id]
                Message(role=role, text=content, conversation=c)

    def add_shadow_message(self, role: str, content: str) -> None:
        """
        Add a message to the shadow message history.
        Shadow messages are cleared after GPT is prompted.
        """
        self.shadow_messages.append({
            "role": role,
            "content": content
        })

    def complete(self, memory_type=MemoryScheme.FULL) -> str:
        """
        Send messages to chat module and wait for response.
        """
        
        # Format messages to send to completion based on memory scheme
        formatted_messages = format_memory(self.messages, memory_type)
        resp = self.module.get_response(formatted_messages+self.shadow_messages)
        self.shadow_messages = [] # clear shadow messages

        return resp
    
    def summarize(self) -> str:
        """
        Ask chat module to summarize the chat into a single paragraph
        """
        self.add_shadow_message("user", self.cfg.summarize_prompt)

        if isinstance(self.module, OpenAIModule):
            resp = self.module.get_response(self.messages+self.shadow_messages, mode=OpenAIModule.MODE_DUMB)
        else:
            resp = self.module.get_response(self.messages+self.shadow_messages)

        self.shadow_messages = [] # clear shadow messages

        return resp
