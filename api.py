import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.pets import load_db
from src.models.pet import Contact, NextPet, UserRequest, PetInfo
from typing import List


pets_db = load_db()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_pet_contact", response_model=Contact)
async def get_pet_contact():
    info = """Контакты:
☎8 9З7 719 06 08 Ева
📩vk.com/id_ewa"""
    return Contact(info=info)


@app.post("/get_next_pet", response_model=NextPet)
async def get_next_pet(user_photo: UserRequest) -> NextPet:
    pet = pets_db.iloc[user_photo.next_token]
    
    # Создаем структурированные данные
    pet_info = PetInfo(**pet["pet_info"]) if pet["pet_info"] is not None else None
    
    return NextPet(
        id=pet["id"],
        attachments=pet["attachments"],
        description=pet["shortText"][:4096],
        next_token=(user_photo.next_token+1) % len(pets_db),
        pet_info=pet_info
    )


@app.get("/pets", response_model=List[NextPet])
async def get_all_pets(limit: int = 50) -> List[NextPet]:
    """Получить список питомцев с ограничением по количеству"""
    pets_list = []
    
    # Ограничиваем количество для производительности
    max_limit = min(limit, len(pets_db))
    
    for index in range(max_limit):
        pet = pets_db.iloc[index]
        # Создаем структурированные данные
        pet_info = PetInfo(**pet["pet_info"]) if pet["pet_info"] is not None else None
        
        pets_list.append(NextPet(
            id=pet["id"],
            attachments=pet["attachments"],
            description=pet["shortText"][:4096] if pet["shortText"] else "",
            next_token=index,  # Используем индекс как next_token
            pet_info=pet_info
        ))
    
    return pets_list


@app.get("/")
async def root_handler():
    return {"message":"Just another scar for the collection"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=13175, reload=True)
