import httpx
from app.core.Config import settings


class WorkerClient:
    def __init__(self):
        self._base = settings.WORKER_BASE_URL.rstrip("/")

    async def post(self, path: str, json: dict):
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.post(f"{self._base}{path}", json=json)
            r.raise_for_status()
            return r.json()

    async def get(self, path: str, params: dict | None = None):
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(f"{self._base}{path}", params=params)
            r.raise_for_status()
            return r.json()


worker = WorkerClient()
