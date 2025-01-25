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
    # sizes: List[SizedPhoto]
    # text: str
    orig_photo: SizedPhoto

@dataclass
class Attachment:
    type: str
    photo: Optional[Photo]

@dataclass
class VKPost:
    id: int
    date: int
    attachments: List[Attachment]
    shortText: Optional[str]
    text: str

@dataclass
class GroupPostsResponse:
    count: int
    items: List[VKPost]

