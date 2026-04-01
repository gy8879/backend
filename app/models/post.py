"""
Post 모델 — posts 테이블
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(200), nullable=False)

    # Text: 길이 제한 없는 문자열 (게시글 본문처럼 긴 텍스트용)
    # String(200)과 차이: String은 최대 길이 지정, Text는 무제한
    content = Column(Text, nullable=False)

    # 조회수: 기본값 0, 글 열 때마다 +1
    view_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # updated_at: 글 수정 시 갱신되는 시간
    # onupdate=func.now(): UPDATE 쿼리 실행 시 자동으로 현재 시각으로 변경
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
