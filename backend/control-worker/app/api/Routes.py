from fastapi import APIRouter, HTTPException
from typing import Optional, List

from app.schemas import (
    WhitelistRequestIn,
    CreateRequestResponse,
    WhitelistRequestRow,
    StatusResponse
)

from app.core.Config import settings
from app.repositories.WhitelistRepository import JsonWhitelistRepository
from app.services.WhitelistService import WhitelistService
from app.services.StatusService import StatusService

router = APIRouter()

repository = JsonWhitelistRepository(settings.DATA_DIR)
whitelist_svc = WhitelistService(repository)
status_svc = StatusService()


@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/whitelist/request", response_model=CreateRequestResponse)
def create_request(payload: WhitelistRequestIn):
    res = whitelist_svc.create_request(payload.username, payload.note or "")
    if res["ok"] is False and res["message"] == "Username is required":
        raise HTTPException(status_code=400, detail=res["message"])
    return res

@router.get("/whitelist/requests", response_model=List[WhitelistRequestRow])
def list_requests(status: Optional[str] = None):
    return whitelist_svc.list_requests(status=status)


@router.post("/whitelist/requests/{request_id}/approve")
def approve(request_id: str):
    if not whitelist_svc.set_status(request_id, "approved"):
        raise HTTPException(status_code=404, detail="Request not found")
    return {"ok": True}

@router.post("/whitelist/requests/{request_id}/reject")
def reject(request_id: str):
    if not whitelist_svc.set_status(request_id, "rejected"):
        raise HTTPException(status_code=404, detail="Request not found")
    return {"ok": True}


@router.get("/status", response_model=StatusResponse)
def status():
    online, rcon_ok, player_count, players, raw = status_svc.get_status()
    return {
        "ok": True,
        "online": online,
        "rcon_ok": rcon_ok,
        "player_count": player_count,
        "players": players,
        "raw": raw,
    }