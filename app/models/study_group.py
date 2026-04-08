from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class StudyGroup(Base):
    __tablename__ = "study_group"

    id = Column(Integer, primary_key=True)
    leader_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    max_members = Column(Integer, nullable=False)
    current_members = Column(Integer, default=1, nullable=False)
    status = Column(String(20), server_default="모집중", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
