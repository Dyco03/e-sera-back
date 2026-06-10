from app.models.comment import Comment
from app.models.post import Post


def comment_to_api(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "postId": comment.post_id,
        "userId": comment.user_id,
        "userName": comment.user_name,
        "text": comment.text,
        "timestamp": comment.timestamp.isoformat(),
    }


def post_to_api(post: Post) -> dict:
    return {
        "id": post.id,
        "userId": post.user_id,
        "name": post.name,
        "text": post.text,
        "imageUrl": post.image_url,
        "timestamp": post.timestamp.isoformat(),
        "likes": post.likes or [],
        "comments": [comment_to_api(comment) for comment in post.comments],
    }
