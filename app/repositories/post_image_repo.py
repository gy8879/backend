from sqlalchemy.orm import Session
from app.models.post_image import PostImage


def get_images_by_post_id(db: Session, post_id: int):
    return (
        db.query(PostImage)
        .filter(PostImage.post_id == post_id)
        .order_by(PostImage.created_at.asc())
        .all()
    )


def get_image_by_id(db: Session, image_id: int):
    return db.query(PostImage).filter(PostImage.id == image_id).first()


def create_image(db: Session, image: PostImage):
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def delete_image(db: Session, image: PostImage):
    db.delete(image)
    db.commit()
