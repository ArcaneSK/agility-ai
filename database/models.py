from datetime import datetime
from pony.orm import Set, Required, Optional, LongStr 

from database import db

class Prompt(db.Entity):
    role = Required(str, default="system")
    name = Optional(str)
    text = Required(str)

class Conversation(db.Entity):
    name = Required(str)
    messages = Set('Message')
    created = Required(datetime, default=datetime.now())

class Message(db.Entity):
    conversation = Required(Conversation)
    role = Required(str)
    text = Required(str)
    created = Required(datetime, default=datetime.now())
