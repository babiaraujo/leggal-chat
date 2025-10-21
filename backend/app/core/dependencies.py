from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import SessionLocal
from .security import verify_token
from ..models.models import User
from ..services.auth_service import AuthService

security = HTTPBearer()


def get_db() -> Generator:
    """Dependency para obter sessão do banco de dados"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency para obter usuário autenticado"""
    token = credentials.credentials
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = AuthService.get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User | None:
    """Dependency opcional para obter usuário autenticado"""
    if not credentials:
        return None

    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            return None

        user = AuthService.get_current_user(db, token)
        return user
    except:
        return None
