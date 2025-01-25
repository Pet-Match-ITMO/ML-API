import pandas as pd
from decouple import config

database_path = config('PETS_DATABASE_PATH')

def load_db() -> pd.DataFrame:
    data_df = pd.read_json(database_path)
    return data_df
