from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GroupCreate(BaseModel):
    title: str
    description: Optional[str] = None
    max_members: int

    model_config = ConfigDict(from_attributes=True)


class GroupUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    max_members: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class GroupResponse(BaseModel):
    id: int
    leader_id: int
    title: str
    description: Optional[str] = None
    max_members: int
    current_members: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
