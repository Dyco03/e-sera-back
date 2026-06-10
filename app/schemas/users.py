from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserPublic(BaseModel):
    uid: str
    email: EmailStr
    name: str


class ProfilePublic(UserPublic):
    bio: str = ""
    profileImageUrl: str = ""
    followers: list[str] = Field(default_factory=list)
    following: list[str] = Field(default_factory=list)


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user: UserPublic
    data: UserPublic
    accessToken: str
    tokenType: str = "bearer"


class ProfileResponse(BaseModel):
    profile: ProfilePublic
    data: ProfilePublic


class ProfileUpdateRequest(BaseModel):
    uid: str
    email: EmailStr | None = None
    name: str | None = None
    bio: str = ""
    profileImageUrl: str = ""
    followers: list[str] = Field(default_factory=list)
    following: list[str] = Field(default_factory=list)


class FollowToggleRequest(BaseModel):
    currentUid: str


class UserModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
