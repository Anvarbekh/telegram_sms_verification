import requests
from app.config import settings
from typing import Any, Optional


BASE_URL = "https://gatewayapi.telegram.org/"


def _headers() -> dict:
    return {"Authorization": f"Bearer {settings.telegram_api_token}", "Content-Type": "application/json"}


def send_verification_message(phone_number: str, ttl: int = 60, callback_url: Optional[str] = None, code_length: int = 6) -> dict:
    payload = {"phone_number": phone_number, "ttl": ttl, "code_length": code_length}
    if callback_url:
        payload["callback_url"] = callback_url

    url = f"{BASE_URL}sendVerificationMessage"
    resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # Gateway responses are of the form { "ok": true, "result": { ... } }
    if isinstance(data, dict) and data.get("ok"):
        return data.get("result", {})
    return data


def check_verification_status(request_id: Optional[str] = None, phone_number: Optional[str] = None, code: Optional[str] = None) -> dict:
    payload: dict[str, Any] = {}
    if request_id:
        payload["request_id"] = request_id
    if phone_number:
        payload["phone_number"] = phone_number
    if code:
        payload["code"] = code

    url = f"{BASE_URL}checkVerificationStatus"
    resp = requests.post(url, json=payload, headers=_headers(), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get("ok"):
        return data.get("result", {})
    return data


