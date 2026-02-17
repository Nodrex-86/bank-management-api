import os
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from logger_config import logger
from dotenv import load_dotenv

# Lädt die Variablen aus der .env Datei in das System (os.environ)
load_dotenv()

# Nur diese Funktionen erscheinen in der Dokumentation:
__all__ = ["verify_password", "create_access_token"]
# Konfiguration
SECRET_KEY = os.getenv("BANK_SECRET_KEY", "fallback_local_only_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In einem echten System käme dieser Hash aus der SQL-Datenbank
USERS_DB = {
    "admin": {
        "hash": os.getenv("ADMIN_HASH", "$2b$12$DEFAULT_HASH_ONLY_FOR_DEV"),
        "role": "admin"
    },
    "DEMO_USER": {
        "hash": os.getenv("DEMO_HASH", "$2b$12$DEFAULT_DEMO_HASH"),
        "role": "viewer"
    }
}

def verify_password(plain_password: str, hached_password: str) -> bool:
    """
    Vergleicht ein eingegebenes Klartext-Passwort mit dem gespeicherten Bcrypt-Hash.

    Args:
        plain_password (str): Das vom Benutzer eingegebene Passwort im Klartext.
        hashed_password (str): Der aus der Datenbank oder Konfiguration stammende Passwort-Hash.

    Returns:
        bool: True, wenn die Passwörter übereinstimmen, andernfalls False.
    """
    return pwd_context.verify(plain_password, hached_password)

def create_access_token(data: dict) -> str:
    """
    Erstellt einen signierten JSON Web Token (JWT) für die Authentifizierung.

    Args:
        data (dict): Die Nutzdaten (Payload), die im Token kodiert werden sollen (z. B. {"sub": "admin"}).

    Returns:
        str: Der fertig kodierte und mit dem SECRET_KEY signierte JWT-String.
    """
    try:
        to_encode = data.copy()
        jetzt_utc = datetime.now(timezone.utc)
        expire = jetzt_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # --- LOGGER INFO ---
        logger.info(f"JWT-Token erstellt für User: {data.get('sub')} | Rolle: {data.get('role')}")
        
        return encoded_jwt
    except Exception as e:
        # --- LOGGER ERROR ---
        logger.error(f"Fehler bei der JWT-Erstellung: {e}")
        raise e


