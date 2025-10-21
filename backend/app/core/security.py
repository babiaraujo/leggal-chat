from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
import os
from .config import settings


def get_password_hash(password: str) -> str:
    salt = os.urandom(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwdhash.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt = bytes.fromhex(hashed_password[:64])
        stored_hash = bytes.fromhex(hashed_password[64:])
        pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return pwdhash == stored_hash
    except:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
