from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import user_repo
from app.services import jwt_service

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = jwt_service.decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="인증 토큰이 올바르지 않습니다")

    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="존재하지 않는 사용자입니다")
    return user
