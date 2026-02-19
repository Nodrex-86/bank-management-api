import os
from json_storage import JSONStorage
from sqlite_storage import SQLiteStorage
from logger_config import logger
from dotenv import load_dotenv
load_dotenv()

def get_storage(overridden_type: str = None):
    """
    Factory-Methode: Entscheidet basierend auf Umgebungsvariablen, 
    welcher Storage-Provider instanziiert wird.
    """
    storage_type = (overridden_type or os.getenv("STORAGE_TYPE", "json")).lower()

    if storage_type == "sql":
        db_path = os.getenv("DB_FILE", "bank_data.db")
        logger.info(f"Factory: Nutze SQLite.Storage ({db_path})")
        return SQLiteStorage(db_path)
    else:
        json_path = os.getenv("JSON_FILE", "konten.json")
        logger.info(f"Factory: Nutze JSON-Storage ({json_path})")
        return JSONStorage(json_path)