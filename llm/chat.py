import string
import random
import openai
from pony.orm import select

from .memory import format_memory, MemoryScheme

from config import Config

from database import session
from database.models import *

class Chat():

    def __init__(self) -> None:
        """ 
        Initialize the Chat class
        """
        self.cfg = Config()

        if not self.cfg.open_api_key:
            raise ValueError("OpenAI API Key enviroment variable (OPENAI_API_KEY) is not set.")
        
        openai.api_key = self.cfg.open_api_key

        self.messages = []
        self.shadow_messages = []

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

    def complete(self, model="gpt-4", max_tokens=800, temperature=1.2, memory_type=MemoryScheme.FULL) -> str:
        """
        Send messages to GPT and wait for response.
        """
        
        # Format messages to send to completion based on memory scheme
        formatted_messages = format_memory(self.messages, memory_type)

        resp = openai.ChatCompletion.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages = formatted_messages+self.shadow_messages
        )

        self.shadow_messages = [] # clear shadow messages

        return resp['choices'][0]['message']['content']
    
    def summarize(self) -> str:
        """
        Ask GPT to summarize the chat into a single paragraph
        """
        self.add_shadow_message("user", self.cfg.summarize_prompt)

        resp = openai.ChatCompletion.create(
            model=self.cfg.dumb_cli_model,
            max_tokens=500,
            temperature=1.2,
            messages = self.messages+self.shadow_messages
        )

        self.shadow_messages = [] # clear shadow messages

        return resp['choices'][0]['message']['content']
