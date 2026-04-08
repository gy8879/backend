"""
Auth Service — 회원가입/로그인 비즈니스 로직

Repository는 "DB에서 꺼내고 넣기"만 하고,
Service는 "규칙을 적용"한다.

예: "이메일이 중복이면 가입 불가" -> 이건 비즈니스 규칙이니까 여기서 처리

Phase 1:
- 비밀번호는 평문으로 저장/비교한다
- JWT 토큰 발급/검증은 Session 2에서 추가
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.repositories import user_repo
from app.schemas.auth import LoginRequest, SignupRequest
from app.services import jwt_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup(db: Session, request: SignupRequest):
    """
    회원가입

    1. 이메일 중복 체크 (비즈니스 규칙)
    2. DB에 저장 (Repository 호출)

    주의: 비밀번호를 평문으로 저장한다 (Session 2에서 bcrypt 해싱 추가 예정)
    """
    # 1. 이미 가입된 이메일인지 확인
    existing = user_repo.get_user_by_email(db, request.email)
    if existing:
        raise ValueError("이미 존재하는 이메일입니다")

    # 2. User 모델 생성 후 DB에 저장 (비밀번호 평문 저장 — Session 2에서 해싱 추가)
    hashed_password = pwd_context.hash(request.password)
    new_user = User(
        username=request.username,
        nickname=request.nickname,
        email=request.email,
        password=hashed_password,
    )
    return user_repo.create_user(db, new_user)


def login(db: Session, request: LoginRequest):
    """
    로그인

    1. email로 유저 조회
    2. password 평문 비교
    3. 맞으면 user_id 반환
    """
    user = user_repo.get_user_by_email(db, request.email)

    if not user or not pwd_context.verify(request.password, user.password):
        raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다")

    token = jwt_service.create_access_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}
