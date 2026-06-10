from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.users import LoginRequest, RegisterRequest
from app.services.user_mapper import user_to_public


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def register(self, payload: RegisterRequest) -> dict:
        existing = self.users.get_by_email(payload.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = self.users.create(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        token = create_access_token(user.id)
        public_user = user_to_public(user)
        return {
            "user": public_user,
            "data": public_user,
            "accessToken": token,
            "tokenType": "bearer",
        }

    def login(self, payload: LoginRequest) -> dict:
        user = self.users.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(user.id)
        public_user = user_to_public(user)
        return {
            "user": public_user,
            "data": public_user,
            "accessToken": token,
            "tokenType": "bearer",
        }
