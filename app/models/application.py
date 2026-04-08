from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("study_group.id", ondelete="CASCADE"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), server_default="pending", nullable=False)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("group_id", "applicant_id", name="uq_group_applicant"),
    )
