from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import ApplicationCreate


def get_applications_by_group(db: Session, group_id: int) -> List[Application]:
    return db.query(Application).filter(Application.group_id == group_id).order_by(Application.created_at.desc()).all()


def get_application_by_id(db: Session, application_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == application_id).first()


def get_application_by_group_and_user(db: Session, group_id: int, applicant_id: int) -> Optional[Application]:
    return db.query(Application).filter(
        Application.group_id == group_id,
        Application.applicant_id == applicant_id
    ).first()


def create_application(db: Session, group_id: int, applicant_id: int, request: ApplicationCreate) -> Application:
    new_application = Application(
        group_id=group_id,
        applicant_id=applicant_id,
        message=request.message,
        status="pending"
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


def update_application_status(db: Session, application: Application, status: str) -> Application:
    application.status = status
    db.commit()
    db.refresh(application)
    return application
