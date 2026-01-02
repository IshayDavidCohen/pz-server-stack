import os
import re
import hmac
import hashlib

from typing import Dict

# App dependencies
from app.core.Rcon import SourceRconClient
from app.core.Config import settings

_USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")

def _parse_allowlist(raw: str) -> set[str]:
    return {x.strip() for x in (raw or "").split(",") if x.strip()}


class WhitelistService:
    def __init__(self):
        self._allowed_ids = _parse_allowlist(os.getenv("ALLOWED_DISCORD_IDS", ""))

    def auto_whitelist(self, username: str, discord_id: str) -> Dict:
        username = (username or "").strip()
        discord_id = (discord_id or "").strip()

        if not _USERNAME_RE.match(username):
            raise PermissionError("Invalid username format.")
        if not re.fullmatch(r"\d{15,20}", discord_id):
            raise PermissionError("Invalid Discord ID format.")
        if discord_id not in self._allowed_ids:
            raise PermissionError("Discord ID is not allowed to auto-whitelist.")

        login_password = "5533"

        c = SourceRconClient(
            host=settings.PZ_RCON_HOST,
            port=settings.PZ_RCON_PORT,
            password=settings.PZ_RCON_PASSWORD,
            timeout=3.0,
        )
        try:
            c.connect()
        except Exception as e:
            raise RuntimeError(
                f"RCON connect failed to {settings.PZ_RCON_HOST}:{settings.PZ_RCON_PORT}: {repr(e)}"
            )

        try:
            auth_res = c.auth()
        except Exception as e:
            c.close()
            raise RuntimeError(f"RCON auth call crashed: {repr(e)}")

        if not auth_res.ok:
            c.close()
            raise RuntimeError("RCON auth failed (check PZ_RCON_PASSWORD).")

        # Some servers expect "adduser", some accept "/adduser". We try both.
        cmd_variants = [
            f'adduser "{username}" "{login_password}"',
            f'/adduser "{username}" "{login_password}"',
        ]

        last = None
        ok = False
        for cmd in cmd_variants:
            try:
                last = c.exec(cmd)
            except Exception as e:
                c.close()
                raise RuntimeError(f"RCON exec crashed on cmd={cmd!r}: {repr(e)}")

            if last.ok:
                c.close()
                return {
                    "ok": True,
                    "message": f"Whitelisted {username}",
                    "login_password": login_password
                }

        c.close()
        raise RuntimeError(f"RCON adduser failed, last={getattr(last, 'data', None)}")
