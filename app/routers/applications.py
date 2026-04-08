from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.application import ApplicationResponse, ApplicationStatusUpdate
from app.services import application_service

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    request: ApplicationStatusUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return application_service.update_application_status(db, current_user, application_id, request)
    except ValueError as e:
        status_code = 404 if "찾을 수 없습니다" in str(e) else 400
        raise HTTPException(status_code=status_code, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
