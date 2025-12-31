from uuid import uuid4
from datetime import datetime, timezone
from typing import Optional, List, Dict

# App dependencies
from app.repositories.WhitelistRepository import JsonWhitelistRepository

class WhitelistService:
    def __init__(self, repository: JsonWhitelistRepository):
        self._repository = repository

    def create_request(self, username: str, note: str) -> Dict:
        username = username.strip()
        if not username:
            return {"ok": False, "message": "Username is required", "request_id": None}

        rows = self._repository.load()

        if any(r["username"].lower() == username.lower() for r in rows):
            return {
                "ok": False,
                "message": f"Username '{username}' was already requested. Ping the admin if you need changes.",
                "request_id": None
            }

        request_id = str(uuid4())
        rows.append(
            {
                "request_id": request_id,
                "username": username,
                "note": (note or "").strip(),
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._repository.save(rows)

        return {"ok": True, "message": "Request received, whitelisting in progress.", "request_id": request_id}

    def list_requests(self, status: Optional[str] = None) -> List[Dict]:
        rows = self._repository.load()
        if status:
            rows = [r for r in rows if r.get("status") == status]

        return sorted(rows, key=lambda r: r.get("created_at", ""), reverse=True)

    def set_status(self, request_id: str, status: str) -> bool:
        rows = self._repository.load()
        changed = False
        for r in rows:
            if r.get("request_id") == request_id:
                r["status"] = status
                changed = True
                break

        if changed:
            self._repository.save(rows)

        return changed