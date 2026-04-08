from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.study_group import StudyGroup
from app.schemas.group import GroupCreate, GroupUpdate


def get_groups(db: Session, skip: int = 0, limit: int = 100) -> List[StudyGroup]:
    return db.query(StudyGroup).order_by(StudyGroup.created_at.desc()).offset(skip).limit(limit).all()


def get_group_by_id(db: Session, group_id: int) -> Optional[StudyGroup]:
    return db.query(StudyGroup).filter(StudyGroup.id == group_id).first()


def create_group(db: Session, leader_id: int, request: GroupCreate) -> StudyGroup:
    new_group = StudyGroup(
        leader_id=leader_id,
        title=request.title,
        description=request.description,
        max_members=request.max_members,
        current_members=1,
        status="모집중"
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def update_group(db: Session, group: StudyGroup, request: GroupUpdate) -> StudyGroup:
    if request.title is not None:
        group.title = request.title
    if request.description is not None:
        group.description = request.description
    if request.max_members is not None:
        group.max_members = request.max_members

        # 만약 max_members를 수정했는데 current_members보다 작다면? 에러는 service에서 잡기
        if group.current_members >= group.max_members:
            group.status = "모집완료"
        else:
            group.status = "모집중"
            
    db.commit()
    db.refresh(group)
    return group


def update_group_status(db: Session, group: StudyGroup, status: str) -> StudyGroup:
    group.status = status
    db.commit()
    db.refresh(group)
    return group


def increment_current_members(db: Session, group: StudyGroup) -> StudyGroup:
    group.current_members += 1
    if group.current_members >= group.max_members:
        group.status = "모집완료"
    db.commit()
    db.refresh(group)
    return group


def decrement_current_members(db: Session, group: StudyGroup) -> StudyGroup:
    if group.current_members > 1:
        group.current_members -= 1
    
    # 인원이 줄었으니 모집중으로 변경
    if group.current_members < group.max_members:
        if group.status == "모집완료":
            group.status = "모집중"
            
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group: StudyGroup) -> None:
    db.delete(group)
    db.commit()
