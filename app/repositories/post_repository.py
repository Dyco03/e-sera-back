from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment
from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Post]:
        statement = (
            select(Post)
            .options(selectinload(Post.comments))
            .order_by(Post.timestamp.desc())
        )
        return list(self.db.scalars(statement))

    def list_by_user_id(self, user_id: str) -> list[Post]:
        statement = (
            select(Post)
            .options(selectinload(Post.comments))
            .where(Post.user_id == user_id)
            .order_by(Post.timestamp.desc())
        )
        return list(self.db.scalars(statement))

    def get_by_id(self, post_id: str) -> Post | None:
        statement = (
            select(Post)
            .options(selectinload(Post.comments))
            .where(Post.id == post_id)
        )
        return self.db.scalar(statement)

    def create(self, post: Post, comments: list[Comment]) -> Post:
        self.db.add(post)
        for comment in comments:
            self.db.add(comment)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def save(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def add_comment(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comment(self, comment_id: str) -> Comment | None:
        return self.db.get(Comment, comment_id)

    def delete_comment(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()
