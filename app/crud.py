from sqlalchemy.orm import Session
from app import models
import datetime


def create_verification_request(db: Session, phone_number: str, payload: str | None = None, request_id: str | None = None, expires_at: datetime.datetime | None = None, raw_response: dict | None = None):
    vr = models.VerificationRequest(phone_number=phone_number, payload=payload, request_id=request_id, expires_at=expires_at, raw_response=raw_response, status="sent")
    db.add(vr)
    db.commit()
    db.refresh(vr)
    return vr


def get_latest_by_phone(db: Session, phone_number: str):
    return db.query(models.VerificationRequest).filter(models.VerificationRequest.phone_number == phone_number).order_by(models.VerificationRequest.created_at.desc()).first()


def mark_verified(db: Session, vr: models.VerificationRequest):
    vr.status = "verified"
    db.commit()
    db.refresh(vr)
    return vr


def update_status_by_request_id(db: Session, request_id: str, status: str):
    vr = db.query(models.VerificationRequest).filter(models.VerificationRequest.request_id == request_id).first()
    if not vr:
        return None
    vr.status = status
    db.commit()
    db.refresh(vr)
    return vr


