from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class WhitelistRequestIn(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    discord_id: str = Field(min_length=15, max_length=20, pattern=r"^\d{15,20}$")


class CreateRequestResponse(BaseModel):
    ok: bool
    message: str
    login_password: Optional[str] = None


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
