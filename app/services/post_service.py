from fastapi import HTTPException, status

from app.models.comment import Comment
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.posts import CommentIn, PostIn
from app.services.post_mapper import post_to_api


class PostService:
    def __init__(self, posts: PostRepository):
        self.posts = posts

    def list_all(self) -> dict:
        post_list = [post_to_api(post) for post in self.posts.list_all()]
        return {"posts": post_list, "data": post_list}

    def list_by_user_id(self, user_id: str) -> dict:
        post_list = [post_to_api(post) for post in self.posts.list_by_user_id(user_id)]
        return {"posts": post_list, "data": post_list}

    def create(self, payload: PostIn) -> dict:
        text = payload.text.strip()
        image_url = payload.imageUrl.strip()
        if not text and not image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A post needs a photo or a caption",
            )

        post = Post(
            id=payload.id,
            user_id=payload.userId,
            name=payload.name,
            text=text,
            image_url=image_url,
            timestamp=payload.timestamp,
            likes=payload.likes,
        )
        comments = [self._comment_from_payload(comment) for comment in payload.comments]
        post = self.posts.create(post, comments)
        return {"post": post_to_api(post), "data": post_to_api(post)}

    def delete(self, post_id: str) -> dict:
        post = self.posts.get_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        self.posts.delete(post)
        return {"message": "Post deleted"}

    def toggle_like(self, post_id: str, user_id: str) -> dict:
        post = self.posts.get_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        likes = list(post.likes or [])
        if user_id in likes:
            likes.remove(user_id)
        else:
            likes.append(user_id)
        post.likes = likes

        post = self.posts.save(post)
        return {"post": post_to_api(post), "data": post_to_api(post)}

    def add_comment(self, post_id: str, payload: CommentIn) -> dict:
        if self.posts.get_by_id(post_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        comment = self.posts.add_comment(self._comment_from_payload(payload))
        return {
            "comment": {
                "id": comment.id,
                "postId": comment.post_id,
                "userId": comment.user_id,
                "userName": comment.user_name,
                "text": comment.text,
                "timestamp": comment.timestamp.isoformat(),
            },
            "data": {"id": comment.id},
        }

    def delete_comment(self, post_id: str, comment_id: str) -> dict:
        comment = self.posts.get_comment(comment_id)
        if comment is None or comment.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        self.posts.delete_comment(comment)
        return {"message": "Comment deleted"}

    def _comment_from_payload(self, payload: CommentIn) -> Comment:
        return Comment(
            id=payload.id,
            post_id=payload.postId,
            user_id=payload.userId,
            user_name=payload.userName,
            text=payload.text,
            timestamp=payload.timestamp,
        )
