from pydantic import BaseModel, Field
from typing import Optional, Literal, List


class WhitelistRequestIn(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    note: Optional[str] = Field(default=None, max_length=200)


class WhitelistRequestRow(BaseModel):
    request_id: str
    username: str
    note: str
    status: Literal["pending", "approved", "rejected"]
    created_at: str


class CreateRequestResponse(BaseModel):
    ok: bool
    message: str
    request_id: Optional[str]


class StatusResponse(BaseModel):
    ok: bool
    online: bool
    rcon_ok: bool
    player_count: int
    players: List[str]
    raw: Optional[str] = None
