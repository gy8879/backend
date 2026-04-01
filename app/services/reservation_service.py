"""
Reservation Service — 예약 비즈니스 로직

규칙:
- 같은 방에 시간이 겹치는 예약은 불가
- 예약 취소는 본인만 가능
- 시작 시간이 종료 시간보다 앞이어야 한다
"""

from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.repositories import reservation_repo, room_repo
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

    # 2. 시간 유효성
    if request.start_time >= request.end_time:
        raise ValueError("시작 시간은 종료 시간보다 앞이어야 합니다")

    # 3. 같은 방에 겹치는 예약이 있는지
    overlap = reservation_repo.get_overlapping_reservation(
        db, request.room_id, request.start_time, request.end_time
    )
    if overlap:
        raise ValueError("해당 시간에 이미 예약이 있습니다")

    # 4. 예약 생성
    new_reservation = Reservation(
        user_id=user_id,
        room_id=request.room_id,
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
