from sqlalchemy import Column, Integer, Time, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class RoomSetting(Base):
    __tablename__ = "room_setting"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("studyroom.id"), unique=True, nullable=False)
    open_time = Column(Time, nullable=False, server_default="09:00")
    close_time = Column(Time, nullable=False, server_default="22:00")
    slot_duration = Column(Integer, nullable=False, server_default="60")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
