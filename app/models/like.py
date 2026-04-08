"""
Like 모델 — likes 테이블

UniqueConstraint("user_id", "post_id"):
한 사용자가 같은 게시글에 좋아요를 두 번 누를 수 없다.
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Like(Base):
    __tablename__ = "like"

    # UniqueConstraint를 __table_args__에 넣는다
    # → (user_id, post_id) 조합이 중복되면 DB가 에러를 낸다
    # 예: user_id=1, post_id=3 이 이미 있으면 또 넣을 수 없다
    __table_args__ = (
        UniqueConstraint("user_id", "post_id"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
