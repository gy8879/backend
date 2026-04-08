"""
PostImage 모델 — post_images 테이블
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class PostImage(Base):
    __tablename__ = "post_image"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    image_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
