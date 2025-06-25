from typing import List, Optional
from dataclasses import dataclass

@dataclass
class SizedPhoto:
    height: int
    type: str
    url: str
    width: int

@dataclass
class Photo:
    id: int
    date: int
    access_key: str
    orig_photo: SizedPhoto

@dataclass
class Attachment:
    type: str
    photo: Optional[Photo]

@dataclass
class PetInfo:
    age: int
    vaccinations: bool
    sterilization: bool
    health: str
    temperament: str
    name: str
    birth_place: str
    grow_up_with: str
    previous_owner: str
    attitude_to_people: str
    passport: bool
    owner_requirements: str
    photos: List[str]

@dataclass
class VKPost:
    id: int
    date: int
    attachments: List[Attachment]
    shortText: Optional[str]
    text: str
    pet_info: Optional[PetInfo] # Новое поле для JSON-данных

@dataclass
class GroupPostsResponse:
    count: int
    items: List[VKPost]

