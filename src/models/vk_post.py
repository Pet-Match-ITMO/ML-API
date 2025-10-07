from typing import List, Optional, Any
from dataclasses import dataclass
from .attachment import Attachment
from .pet import PetInfo

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

