from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.users import FollowToggleRequest, ProfileUpdateRequest
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{uid}")
def fetch_profile(uid: str, db: Session = Depends(get_db)) -> dict:
    return ProfileService(UserRepository(db)).get_profile(uid)


@router.put("/{uid}")
def update_profile(
    uid: str,
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
) -> dict:
    return ProfileService(UserRepository(db)).update_profile(uid, payload)


@router.post("/{target_uid}/follow-toggle")
def toggle_follow(
    target_uid: str,
    payload: FollowToggleRequest,
    db: Session = Depends(get_db),
) -> dict:
    return ProfileService(UserRepository(db)).toggle_follow(
        payload.currentUid,
        target_uid,
    )
