from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from .attachment import Attachment

class Age(BaseModel):
    years: int
    months: int
    days: int

class Health(BaseModel):
    status: str
    diseases: List[str]
    vaccinations: List[str]

class Contact(BaseModel):
    number: str
    name: str

class PetInfo(BaseModel):
    age: Age
    vaccinations: Optional[bool] = None
    sterilization: Optional[bool] = None
    health: Health
    temperament: List[str]
    contact: Contact
    name: str
    birth_place: str
    grow_up_with: str
    previous_owner: str
    owner_requirements: List[str]

class UserRequest(BaseModel):
    user_id: int
    next_token: int

class NextPet(BaseModel):
    id: int
    attachments: List[Attachment]
    next_token: int
    description: str
    pet_info: Optional[PetInfo] = None

@dataclass
class Pet:
    id: int
    attachments: List[Attachment]
    next_token: int
    description: str

class Contact(BaseModel):
    info: str
