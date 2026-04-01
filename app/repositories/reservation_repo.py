"""
Reservation Repository — 예약 DB 조작
"""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation


def get_reservations_by_room(db: Session, room_id: int):
    """
    특정 스터디룸의 예약 목록

    SQL: SELECT * FROM reservations WHERE room_id = ? ORDER BY start_time;
    """
    return db.query(Reservation).filter(Reservation.room_id == room_id).order_by(Reservation.start_time.asc()).all()


def get_reservations_by_user(db: Session, user_id: int):
    """
    특정 유저의 예약 목록

    SQL: SELECT * FROM reservations WHERE user_id = ? ORDER BY start_time;
    """
    return db.query(Reservation).filter(Reservation.user_id == user_id).order_by(Reservation.start_time.asc()).all()


def get_overlapping_reservation(db: Session, room_id: int, start_time: datetime, end_time: datetime):
    """
    시간 겹침 체크 — 같은 방에 겹치는 예약이 있는지 조회

    겹치는 조건: 기존 예약의 시작 < 새 예약의 끝 AND 기존 예약의 끝 > 새 예약의 시작
    예: 기존 10:00~12:00, 새로 11:00~13:00 → 겹침!

    and_(): 여러 조건을 AND로 묶는다

    SQL: SELECT * FROM reservations
         WHERE room_id = ?
         AND start_time < ? AND end_time > ?
         LIMIT 1;
    """
    return db.query(Reservation).filter(
        and_(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time,
        )
    ).first()


def create_reservation(db: Session, reservation: Reservation):
    """예약 생성"""
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def delete_reservation(db: Session, reservation: Reservation):
    """예약 취소"""
    db.delete(reservation)
    db.commit()
