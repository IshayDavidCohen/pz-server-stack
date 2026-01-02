import logging
from fastapi import APIRouter, HTTPException

from app.schemas import (
    WhitelistRequestIn,
    CreateRequestResponse,
    WhitelistRequestRow,
    StatusResponse
)

from app.services.WhitelistService import WhitelistService
from app.services.StatusService import StatusService

router = APIRouter()

whitelist_svc = WhitelistService()
status_svc = StatusService()
logger = logging.getLogger("control-worker")


@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/whitelist/request", response_model=CreateRequestResponse)
def whitelist(payload: WhitelistRequestIn):
    try:
        return whitelist_svc.auto_whitelist(payload.username, payload.discord_id, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Whitelist worker error: {e}")


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