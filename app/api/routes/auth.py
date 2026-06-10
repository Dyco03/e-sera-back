from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import bearer_scheme, get_current_user, revoke_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.users import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService
from app.services.user_mapper import user_to_public

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> dict:
    result = AuthService(UserRepository(db)).register(payload)
    _set_auth_cookie(response, result["accessToken"])
    return result


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> dict:
    result = AuthService(UserRepository(db)).login(payload)
    _set_auth_cookie(response, result["accessToken"])
    return result


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    user = user_to_public(current_user)
    return {"user": user, "data": user}


@router.post("/logout")
def logout(
    response: Response,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    access_token: str | None = Cookie(default=None),
) -> dict:
    token = credentials.credentials if credentials is not None else access_token
    if token is not None:
        revoke_token(token)
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
    )
