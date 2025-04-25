from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr

class Meeting(BaseModel):
    id: str
    meeting_name: str
    uploaded_at: str
    status: str

class TranscriptionBlock(BaseModel):
    speaker: str
    start: float
    end: float
    text: str