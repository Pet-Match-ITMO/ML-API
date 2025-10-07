from typing import Optional
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
