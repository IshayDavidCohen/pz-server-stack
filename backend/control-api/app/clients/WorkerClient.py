import os
import httpx
from typing import Union

from app.core.Config import settings


class WorkerClient:
    def __init__(self, base_url: Union[str, None] = None):
        self.base_url = (base_url or os.getenv("WORKER_BASE_URL", "http://control-worker:8001")).rstrip("/")

    async def post(self, path: str, json: dict):
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(url, json=json)
            r.raise_for_status()
            return r.json()

    async def request_whitelist(self, username: str, note: str | None):
        return await self.post(
            "/whitelist/request",
            {"username": username, "note": note},
        )

    async def get(self, path: str, params: dict | None = None):
        url = f"{self.base_url}{path}"

        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, params=params)
            r.raise_for_status()
            return r.json()


worker = WorkerClient()
