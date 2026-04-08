from typing import List

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import group_repo
from app.schemas.group import GroupCreate, GroupUpdate, GroupResponse


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return group_repo.get_groups(db, skip=skip, limit=limit)


def get_group(db: Session, group_id: int):
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("모집글을 찾을 수 없습니다")
    return group


def create_group(db: Session, current_user: User, request: GroupCreate):
    if request.max_members < 2:
        raise ValueError("최대 인원은 2명 이상이어야 합니다")
        
    return group_repo.create_group(db, leader_id=current_user.id, request=request)


def update_group(db: Session, current_user: User, group_id: int, request: GroupUpdate):
    group = get_group(db, group_id)
    
    if group.leader_id != current_user.id:
        raise PermissionError("권한이 없습니다")
        
    if request.max_members is not None and request.max_members < group.current_members:
        raise ValueError("최대 인원이 현재 인원보다 적을 수 없습니다")
        
    return group_repo.update_group(db, group, request)


def delete_group(db: Session, current_user: User, group_id: int):
    group = get_group(db, group_id)
    
    if group.leader_id != current_user.id:
        raise PermissionError("권한이 없습니다")
        
    group_repo.delete_group(db, group)
    return True
