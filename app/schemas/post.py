"""
Post 스키마 — 게시글 요청/응답 형태
"""

from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    """게시글 작성 요청 (제목 + 본문만 받음, 작성자는 토큰에서 추출)"""
    title: str
    content: str


class PostUpdate(BaseModel):
    """
    게시글 수정 요청

    str | None = None: 안 보내면 None → 수정하지 않음
    제목만 바꾸고 싶으면 {"title": "새 제목"} 만 보내면 된다
    """
    title: str | None = None
    content: str | None = None


class PostResponse(BaseModel):
    """게시글 응답"""
    id: int
    user_id: int
    title: str
    content: str
    view_count: int
    created_at: datetime
    updated_at: datetime
