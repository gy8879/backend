from sqlalchemy.orm import Session

from app.models.room_setting import RoomSetting


def get_by_room_id(db: Session, room_id: int):
    return db.query(RoomSetting).filter(RoomSetting.room_id == room_id).first()


def create_default(db: Session, room_id: int):
    setting = RoomSetting(room_id=room_id)
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def update(db: Session, setting: RoomSetting):
    db.commit()
    db.refresh(setting)
    return setting
