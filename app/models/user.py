"""
User 모델 — users 테이블을 파이썬 클래스로 정의한 것

Supabase(DB)에 이미 만들어둔 users 테이블이 있다.
SQLAlchemy가 이 클래스를 보고 "아, users 테이블은 이렇게 생겼구나"를 이해한다.

즉, DB 테이블의 '설계도'를 파이썬 코드로 옮긴 것.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    users 테이블 정의

    Base를 상속받으면 SQLAlchemy가 이 클래스를 DB 테이블로 인식한다.
    """

    # 이 클래스가 어떤 테이블에 매핑되는지 지정
    # 이걸 안 쓰면 SQLAlchemy가 어떤 테이블인지 모른다
    __tablename__ = "user"

    # ── 컬럼 정의 ──
    # Column(타입, 옵션) 형태로 쓴다
    # 파이썬 변수명 = DB 컬럼명 (같으면 자동 매핑)

    # primary_key=True: 이 컬럼이 각 행을 구분하는 고유 번호 (PK)
    # DB에서 자동으로 1, 2, 3... 증가한다 (SERIAL)
    id = Column(Integer, primary_key=True)

    # String(50): 최대 50자까지 저장 가능 (VARCHAR(50))
    # nullable=False: 빈 값(NULL) 허용 안 함 → 반드시 입력해야 함
    username = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(20), nullable=False, server_default="user")

    # DateTime(timezone=True): 시간대 정보 포함 (TIMESTAMPTZ)
    # server_default=func.now(): DB에서 INSERT할 때 자동으로 현재 시각 입력
    # → 코드에서 created_at을 안 넣어도 DB가 알아서 채워준다
    created_at = Column(DateTime(timezone=True), server_default=func.now())
