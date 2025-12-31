from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class WhitelistRequestIn(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    note: Optional[str] = Field(default=None, max_length=200)


class CreateRequestResponse(BaseModel):
    ok: bool
    message: str
    request_id: Optional[str]


class ServerInfoResponse(BaseModel):
    ok: bool
    host: str
    port: int
    steam_url: str
    password_required: bool


class StatusResponse(BaseModel):
    ok: bool
    online: bool
    rcon_ok: bool
    player_count: int
    players: List[str]
    raw: Optional[str] = None
