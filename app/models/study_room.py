"""
StudyRoom 모델 — study_rooms 테이블
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class StudyRoom(Base):
    __tablename__ = "study_rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
