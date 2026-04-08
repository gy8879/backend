"""
Like 스키마 — 좋아요 응답 형태
"""

from datetime import datetime
from pydantic import BaseModel


class LikeResponse(BaseModel):
    """좋아요 응답"""
    user_id: int
    post_id: int
    created_at: datetime
