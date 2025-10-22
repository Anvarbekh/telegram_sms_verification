from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import crud

router = APIRouter(prefix="/api/v1/webhook")


@router.post("/report")
async def webhook_report(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print(f"Webhook received: {body}")
    # expected: { "request_id": "...", "delivery_status": {"status": "..."} }
    request_id = body.get("request_id")
    delivery_status = body.get("delivery_status", {})
    status = delivery_status.get("status") if isinstance(delivery_status, dict) else None
    print(f"request_id: {request_id}, status: {status}")
    if not request_id or not status:
        raise HTTPException(status_code=400, detail="missing request_id or status")

    updated = crud.update_status_by_request_id(db, request_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="request_id not found")
    return {"ok": True}


