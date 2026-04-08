from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.repositories import application_repo, group_repo
from app.schemas.application import ApplicationCreate, ApplicationStatusUpdate
from app.services.group_service import get_group


def apply_for_group(db: Session, current_user: User, group_id: int, request: ApplicationCreate):
    group = get_group(db, group_id)
    
    if group.leader_id == current_user.id:
        raise ValueError("자신의 모집글에는 신청할 수 없습니다")
        
    if group.status != "모집중":
        raise ValueError("모집이 마감되었습니다")
        
    if group.current_members >= group.max_members:
        raise ValueError("인원이 가득 찼습니다")
        
    existing = application_repo.get_application_by_group_and_user(db, group_id, current_user.id)
    if existing:
        raise ValueError("이미 신청하셨습니다")

    try:
        application = application_repo.create_application(db, group_id, current_user.id, request)
        return application
    except IntegrityError:
        db.rollback()
        raise ValueError("이미 신청하셨습니다")


def get_applications(db: Session, current_user: User, group_id: int):
    group = get_group(db, group_id)
    
    if group.leader_id != current_user.id:
        raise PermissionError("조장만 신청 목록을 볼 수 있습니다")
        
    return application_repo.get_applications_by_group(db, group_id)


def update_application_status(db: Session, current_user: User, application_id: int, request: ApplicationStatusUpdate):
    application = application_repo.get_application_by_id(db, application_id)
    if not application:
        raise ValueError("신청 내역을 찾을 수 없습니다")
        
    group = get_group(db, application.group_id)
    if group.leader_id != current_user.id:
        raise PermissionError("조장만 신청 상태를 변경할 수 있습니다")

    # 상태 전이 로직
    old_status = application.status
    new_status = request.status
    
    if old_status == new_status:
        return application
        
    # 수락하는 경우
    if new_status == "accepted":
        if group.status != "모집중" or group.current_members >= group.max_members:
            raise ValueError("더 이상 수락할 수 없습니다 (인원 초과 또는 모집완료)")
        
        # 인원 증가
        group_repo.increment_current_members(db, group)
        
    # 취소/거절로 인해 기존 'accepted' 상태를 되돌리는 경우
    elif old_status == "accepted" and new_status in ["rejected", "pending", "canceled"]:
        # 인원 감소 (모집중으로 복원 처리도 repo에서 됨)
        group_repo.decrement_current_members(db, group)
        
    # 상태 업데이트
    return application_repo.update_application_status(db, application, new_status)
