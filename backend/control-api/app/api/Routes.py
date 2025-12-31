from fastapi import APIRouter, HTTPException, Request

# App dependencies
from app.clients.WorkerClient import WorkerClient
from app.schemas import WhitelistRequestIn, CreateRequestResponse, ServerInfoResponse, StatusResponse
from app.core.Config import settings
from app.core.HTTP import is_lan_client, build_steam_join_url

router = APIRouter()
worker = WorkerClient(settings.WORKER_BASE_URL)

@router.get("/health")
def health():
    return {"ok": True}


# Keep your existing endpoint shape for the frontend
@router.post("/whitelist/request", response_model=CreateRequestResponse)
async def create_request(payload: WhitelistRequestIn):
    try:
        return await worker.post("/whitelist/request", json=payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WorkerClient error: {e}")


@router.get("/whitelist/requests")
async def list_requests(status: str | None = None):
    try:
        return await worker.get("/whitelist/requests", params={"status": status} if status else None)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WorkerClient error: {e}")


@router.post("/whitelist/requests/{request_id}/approve")
async def approve(request_id: str):
    try:
        return await worker.post(f"/whitelist/requests/{request_id}/approve", json={})
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WorkerClient error: {e}")


@router.post("/whitelist/requests/{request_id}/reject")
async def reject(request_id: str):
    try:
        return await worker.post(f"/whitelist/requests/{request_id}/reject", json={})
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WorkerClient error: {e}")


@router.get("/status", response_model=StatusResponse)
async def status():
    try:
        return await worker.get("/status")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WorkerClient error: {e}")


@router.get("/server/info", response_model=ServerInfoResponse)
def server_info(request: Request):
    # If client is on LAN, return LAN host. Other-wise return PUBLIC host (DDNS/public IP).
    host = settings.PZ_LAN_HOST if is_lan_client(request) else (settings.PZ_PUBLIC_HOST or settings.PZ_LAN_HOST)
    port = settings.PZ_GAME_PORT
    pw = settings.PZ_SERVER_PASSWORD.strip() or None
    steam_url = build_steam_join_url(host, port, pw)
    return {
        "ok": True,
        "host": host,
        "port": port,
        "steam_url": steam_url,
        "password_required": pw is not None,
    }
