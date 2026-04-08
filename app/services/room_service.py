"""
Room Service — 스터디룸 비즈니스 로직

Phase 1에서는 단순 조회만.
"""

from sqlalchemy.orm import Session
from app.models.study_room import StudyRoom
from app.repositories import room_repo, room_setting_repo
from app.schemas.room_setting import RoomSettingUpdate
from app.schemas.studyroom import RoomCreate, RoomUpdate


def get_rooms(db: Session):
    """스터디룸 전체 목록"""
    return room_repo.get_rooms(db)


def get_room(db: Session, room_id: int):
    """스터디룸 1개 조회"""
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    return room


def _assert_admin(current_user):
    if current_user.role != "admin":
        raise PermissionError("관리자만 접근할 수 있습니다")


def create_room(db: Session, current_user, request: RoomCreate):
    """스터디룸 생성 (관리자 전용)"""
    _assert_admin(current_user)
    if request.capacity < 1:
        raise ValueError("capacity는 1 이상이어야 합니다")

    new_room = StudyRoom(
        name=request.name,
        capacity=request.capacity,
        description=request.description,
    )
    created_room = room_repo.create_room(db, new_room)
    room_setting_repo.create_default(db, created_room.id)
    return created_room


def update_room(db: Session, current_user, room_id: int, request: RoomUpdate):
    """스터디룸 수정 (관리자 전용)"""
    _assert_admin(current_user)
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")

    if request.name is not None:
        room.name = request.name
    if request.capacity is not None:
        if request.capacity < 1:
            raise ValueError("capacity는 1 이상이어야 합니다")
        room.capacity = request.capacity
    if request.description is not None:
        room.description = request.description

    return room_repo.update_room(db, room)


def delete_room(db: Session, current_user, room_id: int):
    """스터디룸 삭제 (관리자 전용)"""
    _assert_admin(current_user)
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    room_repo.delete_room(db, room)


def get_room_setting(db: Session, current_user, room_id: int):
    _assert_admin(current_user)
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")

    setting = room_setting_repo.get_by_room_id(db, room_id)
    if not setting:
        setting = room_setting_repo.create_default(db, room_id)
    return setting


def update_room_setting(db: Session, current_user, room_id: int, request: RoomSettingUpdate):
    _assert_admin(current_user)
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")

    setting = room_setting_repo.get_by_room_id(db, room_id)
    if not setting:
        setting = room_setting_repo.create_default(db, room_id)

    if request.open_time is not None:
        setting.open_time = request.open_time
    if request.close_time is not None:
        setting.close_time = request.close_time
    if request.slot_duration is not None:
        if request.slot_duration <= 0:
            raise ValueError("slot_duration은 1 이상이어야 합니다")
        setting.slot_duration = request.slot_duration
    if setting.open_time >= setting.close_time:
        raise ValueError("open_time은 close_time보다 빨라야 합니다")

    return room_setting_repo.update(db, setting)
