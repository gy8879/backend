"""
Reservation Service — 예약 비즈니스 로직

규칙:
- 같은 방에 시간이 겹치는 예약은 불가
- 예약 취소는 본인만 가능
- 시작 시간이 종료 시간보다 앞이어야 한다
"""

from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.reservation import Reservation
from app.repositories import reservation_repo, room_repo, room_setting_repo, group_repo
from app.schemas.reservation import ReservationCreate


def get_reservations_by_room(db: Session, room_id: int):
    """특정 방의 예약 목록"""
    return reservation_repo.get_reservations_by_room(db, room_id)


def get_my_reservations(db: Session, user_id: int):
    """내 예약 목록"""
    return reservation_repo.get_reservations_by_user(db, user_id)


def create_reservation(db: Session, user_id: int, request: ReservationCreate):
    """
    예약 생성

    1. 스터디룸 존재 확인
    2. 시작 < 종료 시간 확인
    3. 시간 겹침 확인
    4. 예약 생성
    """
    # 1. 방이 존재하는지
    room = room_repo.get_room_by_id(db, request.room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    setting = room_setting_repo.get_by_room_id(db, request.room_id)
    if not setting:
        setting = room_setting_repo.create_default(db, request.room_id)

    # 1-1. 본인이 속한 그룹의 예약 권한 확인
    new_reservation_members = 1
    if getattr(request, 'group_id', None) is not None:
        group = group_repo.get_group_by_id(db, request.group_id)
        if not group:
            raise ValueError("그룹을 찾을 수 없습니다")
        if group.status != '모집완료':
            raise ValueError("모집이 완료된 그룹만 예약할 수 있습니다")
        if user_id != group.leader_id:
            raise PermissionError("조장만 그룹 예약을 할 수 있습니다")
        if group.current_members > room.capacity:
            raise ValueError("그룹 인원이 수용 인원을 초과합니다")
        new_reservation_members = group.current_members

    # 2. 시간 유효성
    if request.start_time >= request.end_time:
        raise ValueError("시작 시간은 종료 시간보다 앞이어야 합니다")
    if request.start_time.timetz().replace(tzinfo=None) < setting.open_time:
        raise ValueError("운영 시간 이전에는 예약할 수 없습니다")
    if request.end_time.timetz().replace(tzinfo=None) > setting.close_time:
        raise ValueError("운영 시간 이후에는 예약할 수 없습니다")

    duration = request.end_time - request.start_time
    duration_minutes = int(duration / timedelta(minutes=1))
    if duration_minutes <= 0 or duration_minutes % setting.slot_duration != 0:
        raise ValueError("예약 시간은 슬롯 단위의 배수여야 합니다")

    # 3. 같은 방에 겹치는 예약 총 인원이 수용 인원을 넘는지
    overlapping_reservations = reservation_repo.get_overlapping_reservations(
        db, request.room_id, request.start_time, request.end_time
    )
    
    total_occupancy = sum(
        1 if getattr(r, 'group_id', None) is None else r.group.current_members
        for r in overlapping_reservations
    )
    
    if total_occupancy + new_reservation_members > room.capacity:
        raise ValueError("해당 시간대 예약 가능 인원을 초과했습니다")

    # 4. 예약 생성
    new_reservation = Reservation(
        user_id=user_id,
        room_id=request.room_id,
        group_id=getattr(request, 'group_id', None),
        start_time=request.start_time,
        end_time=request.end_time,
    )
    return reservation_repo.create_reservation(db, new_reservation)


def cancel_reservation(db: Session, user_id: int, reservation_id: int):
    """
    예약 취소

    규칙: 본인 예약만 취소 가능
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise ValueError("예약을 찾을 수 없습니다")
    if reservation.user_id != user_id:
        raise PermissionError("본인의 예약만 취소할 수 있습니다")

    reservation_repo.delete_reservation(db, reservation)
