from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.post_repository import PostRepository
from app.schemas.posts import CommentIn, PostIn, ToggleLikeRequest
from app.services.post_service import PostService

router = APIRouter(tags=["posts"])


@router.get("/posts")
def fetch_all_posts(db: Session = Depends(get_db)) -> dict:
    return PostService(PostRepository(db)).list_all()


@router.post("/posts", status_code=201)
def create_post(payload: PostIn, db: Session = Depends(get_db)) -> dict:
    return PostService(PostRepository(db)).create(payload)


@router.delete("/posts/{post_id}")
def delete_post(post_id: str, db: Session = Depends(get_db)) -> dict:
    return PostService(PostRepository(db)).delete(post_id)


@router.get("/users/{user_id}/posts")
def fetch_posts_by_user_id(user_id: str, db: Session = Depends(get_db)) -> dict:
    return PostService(PostRepository(db)).list_by_user_id(user_id)


@router.post("/posts/{post_id}/likes/toggle")
def toggle_like(
    post_id: str,
    payload: ToggleLikeRequest,
    db: Session = Depends(get_db),
) -> dict:
    return PostService(PostRepository(db)).toggle_like(post_id, payload.userId)


@router.post("/posts/{post_id}/comments", status_code=201)
def add_comment(
    post_id: str,
    payload: CommentIn,
    db: Session = Depends(get_db),
) -> dict:
    return PostService(PostRepository(db)).add_comment(post_id, payload)


@router.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(
    post_id: str,
    comment_id: str,
    db: Session = Depends(get_db),
) -> dict:
    return PostService(PostRepository(db)).delete_comment(post_id, comment_id)
