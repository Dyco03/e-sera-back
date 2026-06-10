from datetime import datetime

from pydantic import BaseModel, Field


class CommentIn(BaseModel):
    id: str
    postId: str
    userId: str
    userName: str
    text: str
    timestamp: datetime


class CommentOut(CommentIn):
    pass


class PostIn(BaseModel):
    id: str
    userId: str
    name: str
    text: str
    imageUrl: str = ""
    timestamp: datetime
    likes: list[str] = Field(default_factory=list)
    comments: list[CommentIn] = Field(default_factory=list)


class PostOut(PostIn):
    comments: list[CommentOut] = Field(default_factory=list)


class PostsResponse(BaseModel):
    posts: list[PostOut]
    data: list[PostOut]


class ToggleLikeRequest(BaseModel):
    userId: str
