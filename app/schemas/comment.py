"""
Comment 스키마 — 댓글 요청/응답 형태
"""

from datetime import datetime
from pydantic import BaseModel


class CommentCreate(BaseModel):
    """댓글 작성 요청 (본문만)"""
    content: str


class CommentResponse(BaseModel):
    """댓글 응답"""
    id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime
