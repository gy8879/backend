"""
Auth 스키마 — 회원가입/로그인 요청·응답 형태 정의

Model(SQLAlchemy)은 DB 테이블 구조,
Schema(Pydantic)는 API 요청/응답 구조.

역할: 들어오는 데이터 검증 + 나가는 데이터 필터링
"""

from pydantic import BaseModel


# ── 회원가입 ──

class SignupRequest(BaseModel):
    """
    회원가입 시 클라이언트가 보내는 데이터

    Phase 1에서는 이메일 형식까지는 검증하지 않고 문자열로 받는다.
    """
    username: str
    nickname: str
    email: str
    password: str


class SignupResponse(BaseModel):
    """
    회원가입 성공 시 돌려주는 데이터

    password는 절대 응답에 포함하지 않는다
    """
    id: int
    username: str
    nickname: str
    email: str
    role: str


# ── 로그인 ──

class LoginRequest(BaseModel):
    """
    로그인 시 클라이언트가 보내는 데이터

    Phase 1에서는 email + password를 평문 비교한다.
    """
    email: str
    password: str


class LoginResponse(BaseModel):
    """
    로그인 성공 시 돌려주는 데이터

    Phase 4에서는 JWT access token을 반환한다.
    """
    access_token: str
    token_type: str


class MeResponse(BaseModel):
    id: int
    email: str
    username: str
    nickname: str
    role: str
