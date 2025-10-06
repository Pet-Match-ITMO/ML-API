import pandas as pd
import requests
from decouple import config

database_path = config('PETS_DATABASE_PATH')

def load_db() -> pd.DataFrame:
    # Загружаем данные
    response = requests.get(database_path)
    data = response.json()
    
    # Объединяем все массивы питомцев из всех приютов
    all_pets = []
    for shelter_name, pets in data.items():
        for pet in pets:
            pet['shelter'] = shelter_name  # Добавляем информацию о приюте
            all_pets.append(pet)
    
    # Создаем DataFrame из объединенного списка
    data_df = pd.DataFrame(all_pets)
    return data_df
