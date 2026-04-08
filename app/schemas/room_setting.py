from datetime import time, datetime
from typing import Optional

from pydantic import BaseModel


class RoomSettingResponse(BaseModel):
    id: int
    room_id: int
    open_time: time
    close_time: time
    slot_duration: int
    created_at: datetime
    updated_at: datetime


class RoomSettingUpdate(BaseModel):
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    slot_duration: Optional[int] = None
