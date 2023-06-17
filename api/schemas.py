from pydantic import BaseModel, Field, validator
from datetime import datetime

class MessageSchema(BaseModel):
    id: int
    role: str
    text: str
    created: datetime = Field(default_factory=datetime.now, read_only=True)

    class Config:
        orm_mode = True

class ConversationSchema(BaseModel):
    id: int
    name: str
    messages: list[MessageSchema]
    created: datetime = Field(default_factory=datetime.now, read_only=True)

    @validator('messages', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, values):
        return [v if isinstance(v, dict) else v.to_dict() for v in values]

    class Config:
        orm_mode = True

class PromptSchema(BaseModel):
    id: int
    role: str
    name: str
    text: str

    class Config:
        orm_mode = True