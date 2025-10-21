from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
import jwt
import uuid
from ..models.models import User
from ..models.schemas import UserCreate, UserResponse, UserLogin
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings


class AuthService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        """Cria um novo usuário"""
        # Verificar se usuário já existe
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("Usuário já existe com este email")

        # Criar hash da senha
        hashed_password = get_password_hash(user_data.password)

        # Criar usuário
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password=hashed_password,
            name=user_data.name
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return UserResponse.model_validate(db_user)

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Optional[User]:
        """Autentica usuário"""
        user = db.query(User).filter(User.email == login_data.email).first()

        if not user:
            return None

        if not verify_password(login_data.password, user.password):
            return None

        return user

    @staticmethod
    def create_access_token(email: str) -> str:
        """Cria token de acesso"""
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode = {"sub": email, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def get_current_user(db: Session, token: str) -> Optional[User]:
        """Obtém usuário atual a partir do token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None

        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[UserResponse]:
        """Busca usuário por ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return UserResponse.model_validate(user)
        return None
