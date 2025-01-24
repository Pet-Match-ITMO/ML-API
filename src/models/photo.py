from pydantic import BaseModel


class UserPhoto(BaseModel):
    user_id: int
    next_token: int

class NextPet(BaseModel):
    url: str
    next_token: int

class Contact(BaseModel):
    info: str
