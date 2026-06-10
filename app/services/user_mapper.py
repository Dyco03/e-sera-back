from app.models.user import User


def user_to_public(user: User) -> dict:
    return {
        "uid": user.id,
        "email": user.email,
        "name": user.name,
    }


def user_to_profile(user: User) -> dict:
    return {
        **user_to_public(user),
        "bio": user.bio,
        "profileImageUrl": user.profile_image_url,
        "followers": user.followers or [],
        "following": user.following or [],
    }
