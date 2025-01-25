from typing import List
from pydantic import BaseModel
from dataclasses import dataclass
from .vk_post import Attachment

class UserRequest(BaseModel):
    user_id: int
    next_token: int

class NextPet(BaseModel):
    id: int
    attachments: List[Attachment]
    next_token: int
    description: str

@dataclass
class Pet:
    id: int
    attachments: List[Attachment]
    next_token: int
    description: str

class Contact(BaseModel):
    info: str
