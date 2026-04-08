"""
Post Service — 게시글 비즈니스 로직

규칙:
- 게시글 수정/삭제는 작성자 본인만 가능
- 게시글 조회 시 조회수 +1
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.models.post import Post
from app.models.post_image import PostImage
from app.repositories import post_repo, comment_repo, post_image_repo
from app.schemas.post import PostCreate, PostUpdate
from app.services import storage_service


def get_posts(db: Session):
    """게시글 전체 목록"""
    return post_repo.get_posts(db)


def get_post(db: Session, post_id: int):
    """
    게시글 상세 조회 + 조회수 증가

    조회할 때마다 view_count를 1 올린다.
    """
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")

    # 조회수 +1
    post.view_count += 1
    post_repo.update_post(db, post)
    comments = comment_repo.get_comments_by_post(db, post_id)
    images = post_image_repo.get_images_by_post_id(db, post_id)
    serialized_comments = [
        {
            "id": comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "content": comment.content,
            "created_at": comment.created_at,
        }
        for comment in comments
    ]
    serialized_images = [
        {
            "id": image.id,
            "image_url": image.image_url,
            "created_at": image.created_at,
        }
        for image in images
    ]
    return {
        "id": post.id,
        "user_id": post.user_id,
        "title": post.title,
        "content": post.content,
        "view_count": post.view_count,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "comments": serialized_comments,
        "images": serialized_images,
    }


def create_post(db: Session, user_id: int, request: PostCreate):
    """게시글 작성"""
    new_post = Post(
        user_id=user_id,
        title=request.title,
        content=request.content,
    )
    return post_repo.create_post(db, new_post)


def update_post(db: Session, user_id: int, post_id: int, request: PostUpdate):
    """
    게시글 수정

    규칙: 작성자 본인만 수정 가능
    """
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글만 수정할 수 있습니다")

    # None이 아닌 필드만 수정 (보낸 것만 바꾼다)
    if request.title is not None:
        post.title = request.title
    if request.content is not None:
        post.content = request.content

    return post_repo.update_post(db, post)


def delete_post(db: Session, user_id: int, post_id: int):
    """
    게시글 삭제

    규칙: 작성자 본인만 삭제 가능
    """
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글만 삭제할 수 있습니다")

    post_repo.delete_post(db, post)


def upload_post_image(
    db: Session,
    user_id: int,
    post_id: int,
    file_bytes: bytes,
    filename: str,
    content_type: Optional[str],
):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글에만 이미지를 업로드할 수 있습니다")

    image_url = storage_service.upload_post_image(file_bytes, filename, content_type)
    image = PostImage(post_id=post_id, image_url=image_url)
    return post_image_repo.create_image(db, image)


def delete_post_image(db: Session, user_id: int, post_id: int, image_id: int):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글 이미지에만 접근할 수 있습니다")

    image = post_image_repo.get_image_by_id(db, image_id)
    if not image or image.post_id != post_id:
        raise ValueError("이미지를 찾을 수 없습니다")

    storage_service.delete_post_image(image.image_url)
    post_image_repo.delete_image(db, image)
