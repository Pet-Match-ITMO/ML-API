import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.images import load_db
from src.models.photo import Contact, NextPet, UserPhoto


images_db = load_db()
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
    info = "г. Москва, 5112-й Проектируемый пр-д, стр. 1-3, 109383, +7 903 103 20 02"
    return Contact(info=info)


@app.post("/get_next_pet", response_model=NextPet)
async def get_next_pet(user_photo: UserPhoto) -> NextPet:
    next_url = images_db['Image'][user_photo.next_token]
    return NextPet(url=next_url, next_token=(user_photo.next_token+1) % len(images_db["Image"]))


@app.get("/")
async def root_handler():
    return {"message":"Just another scar for the collection"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=13175, reload=True)
