"""
Reservation 모델 — reservations 테이블

user_id, room_id는 외래키(FK)다.
FK = "이 값은 다른 테이블의 id를 참조한다"는 뜻.
예: user_id=3 → users 테이블에서 id=3인 사용자
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)

    # ForeignKey("테이블명.컬럼명"): 이 값은 users 테이블의 id를 참조한다
    # → 존재하지 않는 user_id를 넣으면 DB가 에러를 낸다
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("studyroom.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("study_group.id", ondelete="SET NULL"), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    group = relationship("StudyGroup")
