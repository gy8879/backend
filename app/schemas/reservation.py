"""
Reservation 스키마 — 예약 요청/응답 형태
"""

from datetime import datetime
from pydantic import BaseModel


class ReservationCreate(BaseModel):
    """예약 생성 요청 (어떤 방에, 언제부터 언제까지)"""
    room_id: int
    start_time: datetime
    end_time: datetime


class ReservationResponse(BaseModel):
    """예약 응답"""
    id: int
    user_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime
