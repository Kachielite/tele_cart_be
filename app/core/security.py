from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
EXPIRATION_TIME = settings.access_token_expire_minutes

bcrypt_password = CryptContext(schemes="bcrypt", deprecated="auto")

def encrypt_password(password: str):
    return bcrypt_password.hash(password)

def validate_password(password: str, hash_password: str):
    return bcrypt_password.verify(password, hash_password)

def create_token(business_id: int,):
    encoded = {"id": business_id}
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME)
    encoded.update({"exp": expires_at})
    return jwt.encode(encoded, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        business_id = payload.get("id")
        expires_at = payload.get("exp")
        return {"id": business_id, "expires_at": expires_at}
    except (JWTError, ValidationError) as e:
        raise ValueError("Invalid token") from e