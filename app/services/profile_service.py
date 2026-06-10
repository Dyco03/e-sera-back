from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.users import ProfileUpdateRequest
from app.services.user_mapper import user_to_profile


class ProfileService:
    def __init__(self, users: UserRepository):
        self.users = users

    def get_profile(self, uid: str) -> dict:
        user = self.users.get_by_id(uid)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        profile = user_to_profile(user)
        return {"profile": profile, "data": profile}

    def update_profile(self, uid: str, payload: ProfileUpdateRequest) -> dict:
        user = self.users.get_by_id(uid)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        user = self.users.update_profile(
            user,
            bio=payload.bio,
            profile_image_url=payload.profileImageUrl,
        )
        profile = user_to_profile(user)
        return {"profile": profile, "data": profile}

    def toggle_follow(self, current_uid: str, target_uid: str) -> dict:
        current_user = self.users.get_by_id(current_uid)
        target_user = self.users.get_by_id(target_uid)
        if current_user is None or target_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        current_following = list(current_user.following or [])
        target_followers = list(target_user.followers or [])

        if target_uid in current_following:
            current_following.remove(target_uid)
            if current_uid in target_followers:
                target_followers.remove(current_uid)
        else:
            current_following.append(target_uid)
            if current_uid not in target_followers:
                target_followers.append(current_uid)

        current_user.following = current_following
        target_user.followers = target_followers
        self.users.save(current_user)
        self.users.save(target_user)

        profile = user_to_profile(target_user)
        return {"profile": profile, "data": profile}
