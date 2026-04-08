from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.schemas.group import GroupCreate, GroupResponse, GroupUpdate
from app.services import application_service, group_service

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=List[GroupResponse])
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return group_service.get_groups(db, skip, limit)


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    try:
        return group_service.get_group(db, group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=GroupResponse)
def create_group(request: GroupCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.create_group(db, current_user, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, request: GroupUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return group_service.update_group(db, current_user, group_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{group_id}")
def delete_group(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        group_service.delete_group(db, current_user, group_id)
        return {"detail": "모집글이 삭제되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{group_id}/apply", response_model=ApplicationResponse)
def apply_for_group(group_id: int, request: ApplicationCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return application_service.apply_for_group(db, current_user, group_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{group_id}/applications", response_model=List[ApplicationResponse])
def get_group_applications(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return application_service.get_applications(db, current_user, group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
