from datetime import datetime
from pony.orm import Set, Required, Optional 

from database import db

class Prompt(db.Entity):
    role = Required(str, default="system")
    name = Optional(str)
    text = Required(str)
    skip_user_prompt = Optional(bool, default=0)

class Conversation(db.Entity):
    name = Required(str)
    messages = Set('Message')
    created = Required(datetime, default=datetime.now())

class Message(db.Entity):
    conversation = Required(Conversation)
    role = Required(str)
    text = Required(str)
    created = Required(datetime, default=datetime.now())
