from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db
from app import teleclient
from app.config import settings
import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/verification")


@router.post("/start", response_model=schemas.StartVerificationResponse)
def start_verification(req: schemas.StartVerificationRequest, db: Session = Depends(get_db)):
    try:
        callback_url = None
        if settings.webhook_host:
            callback_url = f"{settings.webhook_host}{settings.callback_path}"

        print(f"Sending verification message to phone: {req.phone_number}")
        resp = teleclient.send_verification_message(req.phone_number, ttl=settings.code_ttl_seconds, callback_url=callback_url, code_length=settings.code_length)
        print(f"Telegram API response: {resp}")

        # attempt to extract request_id
        request_id = resp.get("request_id") if isinstance(resp, dict) else None
        print(f"Extracted request_id: {request_id}")

        expires_at = None
        if isinstance(resp, dict) and resp.get("ttl"):
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(resp.get("ttl")))

        vr = crud.create_verification_request(db, phone_number=req.phone_number, payload=req.payload, request_id=request_id, expires_at=expires_at, raw_response=resp)
        print(f"Created verification request with ID: {vr.id}, request_id: {vr.request_id}")
        return {"status": "ok", "request_id": str(vr.request_id)}
    except Exception as e:
        logger.error(f"Error in start_verification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify", response_model=schemas.SimpleResponse)
def verify(req: schemas.VerifyRequest, db: Session = Depends(get_db)):
    try:
        print(f"Verifying code for phone: {req.phone_number}, code: {req.code}")

        # find latest request for this phone
        latest = crud.get_latest_by_phone(db, req.phone_number)
        if not latest:
            print(f"No verification request found for phone: {req.phone_number}")
            raise HTTPException(status_code=404, detail="No verification request found for this phone number")

        print(f"Found latest request: {latest.id}, request_id: {latest.request_id}, status: {latest.status}")

        resp = teleclient.check_verification_status(request_id=latest.request_id, phone_number=req.phone_number, code=req.code)
        print(f"Verification API response: {resp}")

        # Check for verification status in the response
        verification_status = None
        if isinstance(resp, dict):
            verification_status = resp.get("verification_status", {})

        print(f"Verification status: {verification_status}")

        if isinstance(verification_status, dict) and verification_status.get("status") == "code_valid":
            crud.mark_verified(db, latest)
            print("Code verified successfully")
            return {"status": "verified", "message": "Phone number verified"}

        print("Code verification failed")
        return {"status": "failed", "message": "Code not verified"}
    except Exception as e:
        print(f"Exception in verify endpoint: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


