from pydantic import BaseModel, Field
from typing import Optional, Literal, List


class WhitelistRequestIn(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    discord_id: str = Field(min_length=15, max_length=20, pattern=r"^\d{15,20}$")
    password: str = Field(min_length=3, max_length=5)

class WhitelistRequestRow(BaseModel):
    request_id: str
    username: str
    status: Literal["pending", "approved", "rejected"]
    created_at: str


class CreateRequestResponse(BaseModel):
    ok: bool
    message: str
    login_password: Optional[str] = None



class StatusResponse(BaseModel):
    ok: bool
    online: bool
    rcon_ok: bool
    player_count: int
    players: List[str]
    raw: Optional[str] = None
