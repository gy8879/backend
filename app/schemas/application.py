from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    status: str  # accepted, rejected, pending 등

    model_config = ConfigDict(from_attributes=True)


class ApplicationResponse(BaseModel):
    id: int
    group_id: int
    applicant_id: int
    status: str
    message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
